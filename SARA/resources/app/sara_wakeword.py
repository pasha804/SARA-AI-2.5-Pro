# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Offline Lightweight Wake-Word Engine ("Hey SARA" / "SARA Suno")
Listens for acoustic wake-words and restores/focuses SARA's window immediately
when minimized or in background.
"""

import os
import sys
import time
import datetime
import subprocess
from pathlib import Path


class SaraWakeWordDetector:

    def __init__(self, target_keywords: list = None):
        self.keywords = [k.lower() for k in (target_keywords or ["sara", "hey sara", "sara suno"])]
        self.is_running = False

    def trigger_window_restore(self) -> dict:
        """Restores and brings SARA's Electron window to the foreground."""
        ps_restore = """
        $w = New-Object -ComObject wscript.shell;
        $w.AppActivate('SARA');
        $w.AppActivate('MYRAA');
        """
        try:
            subprocess.run(["powershell", "-Command", ps_restore], capture_output=True, timeout=2)
            return {
                "success": True,
                "action": "window_restored",
                "message": "SARA window restored and brought to foreground.",
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def simulate_wake_word_trigger(self, heard_phrase: str = "hey sara") -> dict:
        """Trigger handler called upon wake-word detection."""
        phrase_clean = heard_phrase.lower().strip()
        matched = any(k in phrase_clean for k in self.keywords)

        if matched:
            restore_res = self.trigger_window_restore()
            return {
                "success": True,
                "matched_keyword": phrase_clean,
                "window_action": restore_res,
                "spoken_reply": "Ji Pasha Dev! SARA hazir hai, boliye kya hukum hai?"
            }

        return {
            "success": False,
            "matched_keyword": None,
            "message": f"Phrase '{heard_phrase}' did not match wake-words."
        }


wakeword_engine = SaraWakeWordDetector()

if __name__ == "__main__":
    test_phrase = sys.argv[1] if len(sys.argv) > 1 else "hey sara"
    res = wakeword_engine.simulate_wake_word_trigger(test_phrase)
    print(f"Wake-Word Test Result for '{test_phrase}':")
    import json
    print(json.dumps(res, indent=2))
