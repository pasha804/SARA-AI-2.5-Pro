# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Autonomous Browser-Use Agent
Controls system browser using browser-use framework & Google Gemini.
Executes multi-step web research, button clicking, form filling, and scraping.
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

REPO_DIR = Path(r"D:\MARAA AI\repositories\browser-use").resolve()
if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))

APP_ENV = Path(r"D:\MARAA AI\SARA\resources\app\.env").resolve()
load_dotenv(APP_ENV)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

async def run_browser_task(task_instruction: str):
    from browser_use import Agent, ChatGoogle
    
    if not api_key:
        print("[BrowserUse] Error: GEMINI_API_KEY is not set.")
        return {"success": False, "error": "GEMINI_API_KEY missing."}
        
    print(f"[BrowserUse] Launching autonomous task: {task_instruction}")
    llm = ChatGoogle(model="gemini-3.5-flash", api_key=api_key)
    agent = Agent(
        task=task_instruction,
        llm=llm,
        flash_mode=True
    )
    result = await agent.run(max_steps=10)
    print(f"[BrowserUse] Task completed: {result}")
    return {"success": True, "result": str(result)}

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Go to google.com and search for Pasha Dev"
    try:
        asyncio.run(run_browser_task(task))
    except Exception as e:
        print(f"[BrowserUse] Execution error: {e}")

