# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\MARAA AI\sara_automation_suite.py")
text = p.read_text(encoding="utf-8")

start_marker = "# ============================================================================\n# Pipeline 6: Discord Autonomous Server & Channel Operator"
if start_marker not in text:
    start_marker = start_marker.replace("\n", "\r\n")

end_marker = "# ============================================================================\n# Pipeline 7: Browser First Link Navigation Operator"
if end_marker not in text:
    end_marker = end_marker.replace("\n", "\r\n")

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

if idx_start == -1 or idx_end == -1:
    raise RuntimeError(f"Could not find markers: idx_start={idx_start}, idx_end={idx_end}")

crlf = "\r\n" if "\r\n" in text else "\n"

new_code = r'''# ============================================================================
# Pipeline 6: Discord Autonomous Server & Channel Operator (Strictly Locked to NEXORA)
# ============================================================================
class DiscordAutonomousManager:
    """Manages Discord window focus, channel navigation, and engagement routines strictly locked to Pasha Jan's NEXORA server."""

    AUTHORIZED_SERVER = "NEXORA"

    # Exact channels cataloged from Pasha Jan's NEXORA server
    NEXORA_CHANNELS = {
        # Community
        "general": "-general-chat",
        "general-chat": "-general-chat",
        "-general-chat": "-general-chat",
        "random": "-random-chat",
        "random-chat": "-random-chat",
        "-random-chat": "-random-chat",
        "daily-wins": "-daily-wins",
        "-daily-wins": "-daily-wins",
        "help": "-help-and-support",
        "help-and-support": "-help-and-support",
        "-help-and-support": "-help-and-support",
        # Information
        "announcements": "-announcements",
        "-announcements": "-announcements",
        "rules": "-rules",
        "-rules": "-rules",
        "introductions": "-introductions",
        "-introductions": "-introductions",
        "server-goals": "-server-goals",
        "-server-goals": "-server-goals",
        # Development
        "python": "-python",
        "-python": "-python",
        "javascript": "-javascript",
        "-javascript": "-javascript",
        "typescript": "-typescript",
        "-typescript": "-typescript",
        "react": "-react",
        "-react": "-react",
        "nodejs": "-nodejs",
        "-nodejs": "-nodejs",
        "web-dev": "-web-development",
        "web-development": "-web-development",
        "-web-development": "-web-development",
        "app-dev": "-app-development",
        "app-development": "-app-development",
        "-app-development": "-app-development",
        "ai": "-ai-ml",
        "ai-ml": "-ai-ml",
        "-ai-ml": "-ai-ml",
        "data-science": "-data-science",
        "-data-science": "-data-science",
        "database": "-database",
        "-database": "-database",
        "backend": "-backend",
        "-backend": "-backend",
        "frontend": "-frontend",
        "-frontend": "-frontend",
        "devops": "-devops",
        "-devops": "-devops",
        "linux": "-linux",
        "-linux": "-linux",
        "cybersecurity": "-cybersecurity",
        "-cybersecurity": "-cybersecurity",
        "cpp": "-cpp",
        "-cpp": "-cpp",
        "csharp": "-csharp",
        "-csharp": "-csharp",
        # Projects
        "project-showcase": "-project-showcase",
        "-project-showcase": "-project-showcase",
        "portfolio-review": "-portfolio-review",
        "-portfolio-review": "-portfolio-review",
        "open-source": "-open-source",
        "-open-source": "-open-source",
        "build-in-public": "-build-in-public",
        "-build-in-public": "-build-in-public",
        # Learning Hub
        "study-resources": "-study-resources",
        "-study-resources": "-study-resources",
        "learning-roadmaps": "-learning-roadmaps",
        "-learning-roadmaps": "-learning-roadmaps",
        "coding-challenges": "-coding-challenges",
        "-coding-challenges": "-coding-challenges",
        "interview-prep": "-interview-prep",
        "-interview-prep": "-interview-prep",
        # Careers
        "job-opportunities": "-job-opportunities",
        "-job-opportunities": "-job-opportunities",
        "remote-jobs": "-remote-jobs",
        "-remote-jobs": "-remote-jobs",
        "internships": "-internships",
        "-internships": "-internships",
        # Voice Channels
        "general-vc": "General VC",
        "study-room": "-study-room",
        "-study-room": "-study-room",
        "coding-vc": "Coding VC",
        "pair-programming": "Pair Programming"
    }

    def __init__(self):
        import ctypes
        self.user32 = ctypes.windll.user32

    def validate_server_target(self, server_name: str) -> bool:
        """Strict security guard: Enforces that SARA interacts ONLY with the authorized server 'NEXORA'."""
        if not server_name:
            return True
        return server_name.strip().upper() == self.AUTHORIZED_SERVER

    def resolve_nexora_channel(self, target: str) -> str:
        """Maps user input to exact NEXORA channel names."""
        clean = target.strip().lower().lstrip("#").replace(" ", "-")
        if clean in self.NEXORA_CHANNELS:
            return self.NEXORA_CHANNELS[clean]
        clean_no_hyphen = clean.lstrip("-")
        if clean_no_hyphen in self.NEXORA_CHANNELS:
            return self.NEXORA_CHANNELS[clean_no_hyphen]
        return target.strip()

    def _get_window(self):
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        h_desk = user32.OpenDesktopW('default', 0, False, 0x01FF)
        if h_desk:
            user32.SetThreadDesktop(h_desk)

        found = []
        def cb(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value
                    if "discord" in title.lower():
                        found.append((hwnd, title))
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(cb), 0)
        return found[0] if found else (None, None)

    def is_in_nexora(self) -> bool:
        """Verifies whether the focused Discord client is currently inside NEXORA server."""
        hwnd, title = self._get_window()
        if hwnd and title:
            return "nexora" in title.lower()
        return False

    def focus_discord(self) -> dict:
        hwnd, title = self._get_window()
        if hwnd:
            self.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            self.user32.SetForegroundWindow(hwnd)
            in_nexora = "nexora" in (title or "").lower()
            return {
                "success": True,
                "message": f"Focused active Discord window: '{title}'",
                "title": title,
                "server": self.AUTHORIZED_SERVER if in_nexora else "OTHER",
                "in_nexora": in_nexora
            }
        
        disc_exe = os.path.expandvars(r"%LOCALAPPDATA%\Discord\Discord.exe")
        if os.path.exists(disc_exe):
            subprocess.Popen([disc_exe])
            return {"success": True, "message": "Launched Discord from AppData.", "server": self.AUTHORIZED_SERVER}
        return {"success": False, "error": "Discord is not running or installed."}

    def select_server(self, server_name: str = "NEXORA") -> dict:
        """Ensures Discord is actively on NEXORA by using Discord Quick Switcher (*NEXORA)."""
        if not self.validate_server_target(server_name):
            return {
                "success": False,
                "error": f"Security Guard: SARA is restricted to post ONLY on authorized server '{self.AUTHORIZED_SERVER}'. Attempt to switch to '{server_name}' was blocked."
            }

        hwnd, title = self._get_window()
        if not hwnd:
            self.focus_discord()
            time.sleep(2.0)
            hwnd, title = self._get_window()

        if not hwnd:
            return {"success": False, "error": "Could not access active Discord window."}

        self.user32.ShowWindow(hwnd, 9)
        self.user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)

        try:
            import pyautogui
            import pyperclip
            pyautogui.FAILSAFE = False
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(0.3)
            pyperclip.copy(f"*{self.AUTHORIZED_SERVER}")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.4)
            pyautogui.press('enter')
            time.sleep(0.5)
            return {"success": True, "server": self.AUTHORIZED_SERVER, "message": f"Switched to authorized server '{self.AUTHORIZED_SERVER}'"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def navigate_and_post(self, target_channel_or_user: str, message: str = "", target_type: str = "text", server_name: str = "NEXORA") -> dict:
        """Navigates to a specific channel inside NEXORA and sends a message, with strict foreign server blocking."""
        if not self.validate_server_target(server_name):
            return {
                "success": False,
                "error": f"Security Guard: SARA is restricted to post ONLY on authorized server '{self.AUTHORIZED_SERVER}'. Attempt to post on '{server_name}' was blocked."
            }

        hwnd, title = self._get_window()
        if not hwnd:
            self.focus_discord()
            time.sleep(2.5)
            hwnd, title = self._get_window()

        if not hwnd:
            return {"success": False, "error": "Could not access active Discord window."}

        self.user32.ShowWindow(hwnd, 9)
        self.user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)

        clean_target = self.resolve_nexora_channel(target_channel_or_user)

        import pyautogui
        import pyperclip
        pyautogui.FAILSAFE = False

        if not self.is_in_nexora():
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(0.3)
            pyperclip.copy(f"*{self.AUTHORIZED_SERVER}")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(0.5)

        if clean_target:
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(0.4)

            prefix = ""
            if target_type.lower() == "voice" and not clean_target.startswith("!"):
                prefix = "!"
            elif target_type.lower() == "text" and not clean_target.startswith("#") and not clean_target.startswith("@"):
                prefix = "#"
            elif target_type.lower() == "dm" and not clean_target.startswith("@"):
                prefix = "@"

            query = f"{prefix}{clean_target}"
            pyperclip.copy(query)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.6)

        if message:
            pyperclip.copy(message)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            pyautogui.press('enter')

        action_desc = f"Posted message to '{clean_target}' ({target_type}) in [{self.AUTHORIZED_SERVER}]" if message else f"Navigated to '{clean_target}' ({target_type}) in [{self.AUTHORIZED_SERVER}]"
        spoken = f"Pasha Jan, aapke server NEXORA par '{clean_target}' channel me message post kar diya hai!" if message else f"Pasha Jan, aapke server NEXORA par '{clean_target}' channel khol diya hai!"
        return {
            "success": True,
            "server": self.AUTHORIZED_SERVER,
            "action": action_desc,
            "target": clean_target,
            "type": target_type,
            "message": message,
            "spoken_reply": spoken
        }

    def run_server_engagement_routine(self, server_name: str = "NEXORA", routine_type: str = "daily_lively") -> dict:
        """Autonomously posts engaging updates, daily dev tips, and announcements strictly on the authorized NEXORA server."""
        if not self.validate_server_target(server_name):
            return {
                "success": False,
                "error": f"Security Guard: SARA is restricted to post ONLY on authorized server '{self.AUTHORIZED_SERVER}'. Attempt to post on '{server_name}' was blocked."
            }

        routines = [
            {
                "channel": "-general-chat",
                "type": "text",
                "message": "Salam everyone! 🚀 SARA AI 2.5 Pro active on duty in NEXORA with Pasha Jan today. What are you building or debugging right now? Drop your updates below! ✨"
            },
            {
                "channel": "-announcements",
                "type": "text",
                "message": "📢 **NEXORA Hub Update**: SARA AI 2.5 Pro autonomous multi-channel driver, Google Antigravity IDE bridge, and 415+ n8n workflow automations are fully active!"
            },
            {
                "channel": "-ai-ml",
                "type": "text",
                "message": "🤖 **NEXORA AI/ML Tip**: When structuring multi-agent architectures or asynchronous background tasks, decouple tool execution from UI polling to maintain high-frequency responsive event loops!"
            }
        ]

        results = []
        for r in routines:
            res = self.navigate_and_post(r["channel"], r["message"], r["type"], server_name=self.AUTHORIZED_SERVER)
            results.append(res)
            time.sleep(1.0)

        # Log activity
        log_file = DATA_DIR / "discord_activity_log.json"
        log_data = []
        if log_file.exists():
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    log_data = json.load(f)
            except Exception:
                pass
        log_data.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "server": self.AUTHORIZED_SERVER,
            "routine": routine_type,
            "dispatched_count": len(results),
            "status": "COMPLETED"
        })
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(log_data[-50:], f, indent=2)
        except Exception:
            pass

        spoken = f"Pasha Jan, aapke Discord server 'NEXORA' par -general-chat, -announcements aur -ai-ml channels me active engagement messages post kar diye hain! Server ab fully lively hai!"
        return {
            "success": True,
            "routine": routine_type,
            "server": self.AUTHORIZED_SERVER,
            "actions": results,
            "spoken_reply": spoken
        }

'''

updated_text = text[:idx_start] + new_code.replace("\n", crlf) + text[idx_end:]
p.write_text(updated_text, encoding="utf-8")
print("Pipeline 6 successfully rewritten for NEXORA.")
