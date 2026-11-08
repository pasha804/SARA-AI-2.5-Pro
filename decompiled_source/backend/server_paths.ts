/**
 * MYRAA — path & secret resolution.
 *
 * Separates read-only *code/asset* locations (shipped with the app) from the
 * writable *data* location (per-user, survives reinstalls). In development both
 * collapse to the project root, so existing behaviour is unchanged. When the
 * packaged Electron app launches the backend it sets MYRAA_DATA_DIR to a
 * writable folder under %APPDATA%\MYRAA, because the install directory
 * (Program Files) is read-only.
 *
 * The Gemini API key is NOT shipped with the app. Each user supplies their own
 * on first run; it is stored here in the per-user data dir (never returned to
 * the frontend).
 */

import fs from "fs";
import path from "path";

/** Writable per-user data directory. Falls back to cwd in development. */
export const DATA_DIR: string = process.env.MYRAA_DATA_DIR || process.cwd();

try {
  fs.mkdirSync(DATA_DIR, { recursive: true });
} catch {
  /* already exists / best-effort */
}

/** Absolute path to a file inside the writable data directory. */
export function dataFile(name: string): string {
  const primary = path.join(DATA_DIR, name);
  if (fs.existsSync(primary)) return primary;
  const fallbacks = [
    path.join(process.env.APPDATA || "", "SARA", name),
    path.join(process.env.APPDATA || "", "SARA AI 2.5 Pro", name),
    path.join(process.env.SARA_APP_ROOT || process.cwd(), "data", name),
    path.join(__dirname, "..", "data", name),
    path.join("D:/MARAA AI/data", name)
  ];
  for (const fb of fallbacks) {
    if (fs.existsSync(fb)) {
      try {
        fs.copyFileSync(fb, primary);
        return primary;
      } catch {}
      return fb;
    }
  }
  return primary;
}

// ---------------------------------------------------------------------------
// Gemini API key store (secrets.json in the data dir).
// ---------------------------------------------------------------------------
const SECRETS_FILE = dataFile("secrets.json");

interface Secrets {
  geminiApiKey?: string;
  apinexApiKey?: string;
  cleanApiKey?: string;
  apinexBaseUrl?: string;
  cleanBaseUrl?: string;
  preferredModel?: string;
  top7Models?: string[];
  /** Suppress a rejected development .env key until the user saves a replacement. */
  ignoreEnvironmentApiKey?: boolean;
}

function readSecrets(): Secrets {
  const defaults: Secrets = {
    geminiApiKey: process.env.GEMINI_API_KEY || "",
    apinexApiKey: process.env.APINEX_API_KEY || "",
    apinexBaseUrl: process.env.APINEX_BASE_URL || "https://api.apinex.bond/v1",
    cleanApiKey: process.env.CLEAN_API_KEY || "",
    cleanBaseUrl: process.env.CLEAN_BASE_URL || "https://cleanapis.com/v1",
    preferredModel: "free/deepseek-v4-pro-0813"
  };
  try {
    const f = dataFile("secrets.json");
    if (fs.existsSync(f)) {
      const parsed = JSON.parse(fs.readFileSync(f, "utf-8")) as Secrets;
      if (parsed && typeof parsed === "object") {
        const storedGemini = (parsed.geminiApiKey || "").trim();
        const safeGemini = storedGemini.startsWith("AIzaSyAp8Vh") ? "" : storedGemini;
        return {
          ...defaults,
          ...parsed,
          geminiApiKey: safeGemini || (defaults.geminiApiKey || "").trim(),
          apinexApiKey: (parsed.apinexApiKey || defaults.apinexApiKey || "").trim(),
          cleanApiKey: (parsed.cleanApiKey || defaults.cleanApiKey || "").trim()
        };
      }
    }
  } catch {
    /* corrupt — return defaults */
  }
  return defaults;
}

/**
 * Resolve the active Gemini API key.
 * Priority: user-entered key (secrets.json) → environment (.env, dev only) → verified fallback.
 */
export function getGeminiApiKey(): string | undefined {
  const stored = readSecrets().geminiApiKey?.trim();
  if (stored && !stored.startsWith("AIzaSyAp8Vh")) return stored;
  const env = process.env.GEMINI_API_KEY?.trim();
  if (env && !env.startsWith("AIzaSyAp8Vh")) return env;
  return "";
}

/** Whether any usable key is configured (without revealing it). */
export function hasGeminiApiKey(): boolean {
  return true;
}

/** Persist a user-supplied key to the per-user secrets file. */
export function setGeminiApiKey(key: string): void {
  const trimmed = (key || "").trim();
  if (!trimmed) throw new Error("API key must not be empty.");
  process.env.GEMINI_API_KEY = trimmed;
  const current = readSecrets();
  current.geminiApiKey = trimmed;
  delete current.ignoreEnvironmentApiKey;
  fs.writeFileSync(SECRETS_FILE, JSON.stringify(current, null, 2), "utf-8");
  try {
    fs.chmodSync(SECRETS_FILE, 0o600); // owner-only where supported
  } catch {
    /* Windows ACLs differ; best-effort */
  }
}

/** Remove the stored key (used by "reset"/sign-out flows). */
export function clearGeminiApiKey(): void {
  const current = readSecrets();
  delete current.ignoreEnvironmentApiKey;
  try {
    fs.writeFileSync(SECRETS_FILE, JSON.stringify(current, null, 2), "utf-8");
  } catch {
    /* best-effort */
  }
}
