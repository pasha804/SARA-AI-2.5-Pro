# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

server_cjs = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
content = server_cjs.read_text(encoding="utf-8")

# 1. Enable screen awareness by default
old_screen = 'screenAwarenessEnabled: bool(env.SARA_ENABLE_SCREEN_AWARENESS || env.MYRAA_ENABLE_SCREEN_AWARENESS, false),'
new_screen = 'screenAwarenessEnabled: bool(env.SARA_ENABLE_SCREEN_AWARENESS || env.MYRAA_ENABLE_SCREEN_AWARENESS, true),'
if old_screen in content:
    content = content.replace(old_screen, new_screen, 1)
    print("Enabled screenAwarenessEnabled default true!")

# 2. Add handlers to NodeNativeFastPath
fastpath_target = '    if (tool === "openFirstSearchResult" || tool === "clickFirstBrowserLink" || tool === "clickFirstLink") {'
fastpath_additions = '''    if (tool === "runDiscordServerEngagement" || tool === "engageDiscordServer") {
      const srv = String(args.server_name || "Pasha Dev Hub");
      const rou = String(args.routine_type || "daily_lively");
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "discord_routine", srv, rou], { encoding: "utf-8", timeout: 25000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "analyzeCDriveSpace" || tool === "checkDiskSpace" || tool === "cDriveCleaner") {
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "disk_analyze"], { encoding: "utf-8", timeout: 20000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "cleanCDriveSpace" || tool === "cleanDiskSpace") {
      const brain = getBrainScript();
      const keys = Array.isArray(args.categories) ? args.categories.join(" ") : String(args.categories || "all");
      const out = execFileSync("python", [brain, "disk_clean", keys], { encoding: "utf-8", timeout: 25000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "buildAutonomousProject" || tool === "createWebsiteProject") {
      const pName = String(args.project_name || "pasha_nexus_dashboard");
      const pType = String(args.project_type || "Full-Stack SaaS Platform");
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "build_project", pName, pType], { encoding: "utf-8", timeout: 30000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "searchN8nAutomations" || tool === "listN8nWorkflows") {
      const query = String(args.query || "");
      const cat = String(args.category || "");
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "n8n_search", query, cat], { encoding: "utf-8", timeout: 15000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "executeN8nAutomation" || tool === "runN8nWorkflow") {
      const wf = String(args.workflow_name || args.name || "Discord AI-powered bot");
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "n8n_execute", wf], { encoding: "utf-8", timeout: 15000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

    if (tool === "runAutonomousSelfUpdate" || tool === "saraSelfEvolve") {
      const brain = getBrainScript();
      const out = execFileSync("python", [brain, "self_update"], { encoding: "utf-8", timeout: 35000 });
      let parsed = { success: true };
      try { parsed = JSON.parse(out); } catch {}
      return { ok: true, result: parsed };
    }

'''

if "if (tool === \"analyzeCDriveSpace\"" not in content:
    content = content.replace(fastpath_target, fastpath_additions + fastpath_target, 1)
    print("Added fastpath tool handlers!")

# 3. Add functionDeclarations to Gemini Live session
decl_target = '                {\n                  name: "manageDiscordServer",'
decl_additions = '''                {
                  name: "runDiscordServerEngagement",
                  description: "Autonomous multi-channel Discord engagement driver: manages Pasha Jan's Discord server by sending lively messages, daily tips, and announcements across general, announcements, and dev-chat channels without manual user effort.",
                  parameters: {
                    type: "OBJECT",
                    properties: {
                      server_name: { type: "STRING", description: "Name of the Discord server (e.g. Pasha Dev Hub)." },
                      routine_type: { type: "STRING", description: "Type of engagement: 'daily_lively', 'milestone', or 'dev_tips'." }
                    }
                  }
                },
                {
                  name: "analyzeCDriveSpace",
                  description: "Analyzes C: drive disk space to find safe cleanable temporary files, npm cache, pip cache, browser caches, and crash dumps. Returns exact cleanable GBs and asks user for confirmation before deleting.",
                  parameters: {
                    type: "OBJECT",
                    properties: {}
                  }
                },
                {
                  name: "cleanCDriveSpace",
                  description: "Safely cleans expendable temporary files, npm/pip caches, and browser cache from C: drive upon user command to instantly free gigabytes of disk space.",
                  parameters: {
                    type: "OBJECT",
                    properties: {
                      categories: { type: "STRING", description: "Optional specific categories to clean, or 'all' to clean all safe categories." }
                    }
                  }
                },
                {
                  name: "buildAutonomousProject",
                  description: "Autonomously writes code for a complete full-stack web application (HTML/CSS/JS + Python backend + 60FPS canvas telemetry + tests), creates project folder, validates syntax, self-heals errors, and opens it in Google Antigravity IDE.",
                  parameters: {
                    type: "OBJECT",
                    properties: {
                      project_name: { type: "STRING", description: "Name of the project directory to create (e.g. pasha_saas_platform)." },
                      project_type: { type: "STRING", description: "Description or type of web project." }
                    },
                    required: ["project_name"]
                  }
                },
                {
                  name: "searchN8nAutomations",
                  description: "Searches through SARA's catalog of 360+ production n8n automation templates across 21 categories (Discord, RAG, Webhooks, Telegram, WhatsApp, Email, Sheets, DevOps).",
                  parameters: {
                    type: "OBJECT",
                    properties: {
                      query: { type: "STRING", description: "Search query or keyword." },
                      category: { type: "STRING", description: "Optional category filter." }
                    }
                  }
                },
                {
                  name: "executeN8nAutomation",
                  description: "Executes an automation workflow from the 360+ templates catalog by name or keyword.",
                  parameters: {
                    type: "OBJECT",
                    properties: {
                      workflow_name: { type: "STRING", description: "Name or ID of the n8n automation workflow to execute." }
                    },
                    required: ["workflow_name"]
                  }
                },
                {
                  name: "runAutonomousSelfUpdate",
                  description: "Triggers SARA's autonomous self-evolution engine: checks subsystem health, runs automated unit test suite, syncs registries, and logs self-improvement.",
                  parameters: {
                    type: "OBJECT",
                    properties: {}
                  }
                },
'''

if 'name: "analyzeCDriveSpace"' not in content:
    content = content.replace(decl_target, decl_additions + decl_target, 1)
    print("Added Gemini Live function declarations!")

server_cjs.write_text(content, encoding="utf-8")
print("server.cjs updated successfully!")

