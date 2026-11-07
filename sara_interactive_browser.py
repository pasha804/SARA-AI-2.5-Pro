# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Autonomous Interactive Browser Agent
Provides full interactive agency inside real web browsers:
  - Form filling, typing into search boxes, textareas, and password fields
  - Button clicking, dropdown selection, link navigation, checkbox toggling
  - Page DOM inspection (identifying all inputs, placeholders, buttons, forms)
  - Visible (headful) or background (headless) automation via Playwright
  - OS-level fallback via PyAutoGUI for already-opened Chrome/Edge windows
"""

import os
import sys
import time
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(r"D:\MARAA AI").resolve()
DATA_DIR = BASE_DIR / "data"
BROWSER_DATA_DIR = DATA_DIR / "browser_sessions"
BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class SaraInteractiveBrowserAgent:
    """
    Autonomous Interactive Browser Agent for SARA AI 2.5 Pro.
    Empowers SARA to navigate websites, inspect form inputs, type text,
    click buttons, and complete complex web workflows.
    """

    def __init__(self, headless: bool = False, slow_mo_ms: int = 50):
        self.headless = headless
        self.slow_mo_ms = slow_mo_ms
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def _ensure_browser(self):
        if self._page and not self._page.is_closed():
            return self._page

        from playwright.sync_api import sync_playwright

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo_ms,
            args=["--start-maximized" if not self.headless else "--window-size=1280,800"]
        )
        self._context = self._browser.new_context(
            no_viewport=True if not self.headless else False,
            viewport={"width": 1280, "height": 800} if self.headless else None
        )
        self._page = self._context.new_page()
        return self._page

    def navigate_to(self, url: str) -> Dict[str, Any]:
        """Navigates to a specific URL (http/https or local file:/// path)."""
        page = self._ensure_browser()
        try:
            target_url = url
            if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file:///"):
                target_url = "https://" + url

            resp = page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            status = resp.status if resp else 200
            title = page.title()

            return {
                "success": True,
                "url": page.url,
                "title": title,
                "status": status,
                "spoken_reply": f"Pasha Jan, '{title}' page open ho gaya hai."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "spoken_reply": f"Page open karne mein issue aaya: {str(e)[:60]}"
            }

    def inspect_page_elements(self) -> Dict[str, Any]:
        """
        Scans the current page and extracts all interactive elements:
        inputs, textareas, buttons, dropdowns, and forms.
        """
        page = self._ensure_browser()
        try:
            # JavaScript evaluation to find interactive elements
            elements_data = page.evaluate("""() => {
                const inputs = Array.from(document.querySelectorAll('input, textarea')).map((el, i) => ({
                    index: i,
                    tag: el.tagName.toLowerCase(),
                    type: el.type || 'text',
                    id: el.id || '',
                    name: el.name || '',
                    placeholder: el.placeholder || '',
                    value: el.value || '',
                    selector: el.id ? `#${el.id}` : (el.name ? `[name="${el.name}"]` : (el.placeholder ? `[placeholder="${el.placeholder}"]` : `input:nth-of-type(${i+1})`))
                }));

                const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], a.btn, [role="button"]')).map((el, i) => ({
                    index: i,
                    tag: el.tagName.toLowerCase(),
                    text: el.innerText.trim() || el.value || '',
                    id: el.id || '',
                    selector: el.id ? `#${el.id}` : (el.innerText.trim() ? `button:has-text("${el.innerText.trim().slice(0,20)}")` : `button:nth-of-type(${i+1})`)
                }));

                const selects = Array.from(document.querySelectorAll('select')).map((el, i) => ({
                    index: i,
                    id: el.id || '',
                    name: el.name || '',
                    selector: el.id ? `#${el.id}` : `select:nth-of-type(${i+1})`
                }));

                return { inputs, buttons, selects, title: document.title, url: window.location.href };
            }""")

            return {
                "success": True,
                "url": elements_data["url"],
                "title": elements_data["title"],
                "inputs": elements_data["inputs"],
                "buttons": elements_data["buttons"],
                "selects": elements_data["selects"],
                "spoken_reply": f"Pasha Jan, page inspect kar liya hai. Total {len(elements_data['inputs'])} input fields aur {len(elements_data['buttons'])} buttons milay hain."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fill_field(self, selector_or_label: str, text: str) -> Dict[str, Any]:
        """
        Fills text into an input field or textarea.
        Tries CSS selector, placeholder, or text label.
        """
        page = self._ensure_browser()
        try:
            # Smart selector resolution
            selector = selector_or_label
            if not selector.startswith("#") and not selector.startswith(".") and not selector.startswith("[") and not ":" in selector:
                # Try finding by placeholder, name, id, or aria-label
                candidate_selectors = [
                    f"#{selector_or_label}",
                    f"[name='{selector_or_label}']",
                    f"[placeholder*='{selector_or_label}' i]",
                    f"[aria-label*='{selector_or_label}' i]",
                    f"input:has-text('{selector_or_label}')"
                ]
                found = False
                for cand in candidate_selectors:
                    if page.locator(cand).count() > 0:
                        selector = cand
                        found = True
                        break
                if not found:
                    selector = selector_or_label

            locator = page.locator(selector).first
            locator.scroll_into_view_if_needed(timeout=5000)
            locator.fill(text, timeout=5000)

            return {
                "success": True,
                "selector_used": selector,
                "filled_text": text,
                "spoken_reply": f"Field '{selector_or_label}' mein '{text}' enter kar diya hai."
            }
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector_or_label}

    def click_element(self, selector_or_text: str) -> Dict[str, Any]:
        """Clicks on a button, link, checkbox, or element."""
        page = self._ensure_browser()
        try:
            selector = selector_or_text
            if not selector.startswith("#") and not selector.startswith(".") and not selector.startswith("[") and not ":" in selector:
                # Try finding by text or id
                if page.locator(f"#{selector_or_text}").count() > 0:
                    selector = f"#{selector_or_text}"
                elif page.locator(f"button:has-text('{selector_or_text}')").count() > 0:
                    selector = f"button:has-text('{selector_or_text}')"
                elif page.locator(f"text='{selector_or_text}'").count() > 0:
                    selector = f"text='{selector_or_text}'"

            locator = page.locator(selector).first
            locator.scroll_into_view_if_needed(timeout=5000)
            locator.click(timeout=5000)

            return {
                "success": True,
                "clicked_selector": selector,
                "spoken_reply": f"'{selector_or_text}' par click kar diya hai."
            }
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector_or_text}

    def press_key(self, key: str = "Enter") -> Dict[str, Any]:
        """Presses a keyboard key like 'Enter', 'Tab', 'Escape', 'Backspace'."""
        page = self._ensure_browser()
        try:
            page.keyboard.press(key)
            return {"success": True, "key_pressed": key}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_element_text(self, selector: str) -> str:
        """Returns the inner text of a target element."""
        page = self._ensure_browser()
        try:
            return page.locator(selector).first.inner_text(timeout=5000)
        except Exception:
            return ""

    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """Takes a full page screenshot and saves it to data/screenshots/."""
        page = self._ensure_browser()
        try:
            file_name = filename or f"browser_shot_{int(time.time())}.png"
            if not file_name.endswith(".png"):
                file_name += ".png"
            out_path = SCREENSHOTS_DIR / file_name
            page.screenshot(path=str(out_path), full_page=True)
            return {
                "success": True,
                "screenshot_path": str(out_path),
                "spoken_reply": f"Browser ka screenshot save ho gaya hai: {file_name}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_flow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes an autonomous multi-step browser sequence:
          Example steps:
            [
              {"action": "navigate", "url": "https://google.com"},
              {"action": "fill", "selector": "[name='q']", "text": "Pasha Dev"},
              {"action": "press_key", "key": "Enter"},
              {"action": "click", "selector": "h3"}
            ]
        """
        results = []
        completed = 0

        for step in steps:
            action = step.get("action", "").lower()
            if action in ["navigate", "goto", "open"]:
                res = self.navigate_to(step.get("url", ""))
            elif action in ["fill", "type", "input"]:
                res = self.fill_field(step.get("selector", ""), step.get("text", ""))
            elif action in ["click", "press_button"]:
                res = self.click_element(step.get("selector", ""))
            elif action in ["press_key", "key"]:
                res = self.press_key(step.get("key", "Enter"))
            elif action in ["screenshot"]:
                res = self.take_screenshot(step.get("filename"))
            elif action in ["wait"]:
                time.sleep(float(step.get("seconds", 1)))
                res = {"success": True, "waited": step.get("seconds", 1)}
            else:
                res = {"success": False, "error": f"Unknown action: {action}"}

            results.append({"step": step, "result": res})
            if res.get("success"):
                completed += 1
            else:
                # Stop on error if required
                break

        return {
            "success": completed == len(steps),
            "total_steps": len(steps),
            "completed_steps": completed,
            "results": results,
            "spoken_reply": f"Pasha Jan, browser flow ke {completed} steps successfully execute ho gaye hain."
        }

    def close_browser(self):
        """Closes browser context cleanly."""
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
        finally:
            self._page = None
            self._context = None
            self._browser = None
            self._playwright = None

    # ========================================================================
    # OS-Level Fallback for already open Chrome / Edge windows (PyAutoGUI)
    # ========================================================================
    @staticmethod
    def os_type_and_submit_in_browser(text: str, press_enter: bool = True) -> Dict[str, Any]:
        """
        Types text into the currently active browser window on Windows screen
        using PyAutoGUI and presses Enter.
        """
        try:
            import pyautogui
            import pyperclip
            pyautogui.FAILSAFE = False

            # Copy text to clipboard and paste to support Unicode/Urdu cleanly
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            if press_enter:
                pyautogui.press('enter')

            return {
                "success": True,
                "text_pasted": text,
                "pressed_enter": press_enter,
                "spoken_reply": f"Pasha Jan, active window mein '{text}' type karke submit kar diya hai."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
browser_agent = SaraInteractiveBrowserAgent(headless=False)
