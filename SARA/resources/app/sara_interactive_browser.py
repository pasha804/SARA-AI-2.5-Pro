# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Enterprise Autonomous Interactive Browser Engine
Production-grade Playwright Chromium automation agent providing:
  - Persistent browser profiles and cookie persistence
  - Resilient multi-tier locator hierarchy (ARIA role, text, test-id, CSS, XPath)
  - Full human-like interaction (type, click, double-click, hover, scroll, select, upload)
  - Multi-tab management and SPA loading state handling
  - Automatic cookie banner dismissal and dialog handling
  - Visual screenshot capture with target element highlighting
  - OS-level PyAutoGUI fallback for active browser windows
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
BROWSER_PROFILE_DIR = BROWSER_DATA_DIR / "sara_default_profile"
BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class BrowserAutomationError(Exception):
    """Raised when Playwright browser automation fails after retries"""
    pass


class SaraInteractiveBrowserAgent:
    """
    Autonomous Interactive Browser Agent for SARA AI 2.5 Pro.
    Empowers SARA to navigate websites, inspect form inputs, type text,
    click buttons, manage tabs, and complete complex web workflows.
    """

    def __init__(self, headless: bool = True, persistent: bool = False, slow_mo_ms: int = 50):
        self.headless = headless
        self.persistent = persistent
        self.slow_mo_ms = slow_mo_ms
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._dialog_action = "accept"

    @property
    def page(self):
        """Active Playwright page instance (guarantees initialized browser context)."""
        return self._ensure_browser()

    def _resolve_selector(self, selector_or_label: str) -> str:
        """Resolves selector or label into a valid CSS/XPath/text locator string."""
        s = selector_or_label.strip()
        if any(s.startswith(p) for p in ("#", ".", "[", "//", "input", "button", "textarea", "select", "a", "xpath=")):
            return s
        return f"input[placeholder*='{s}' i], input[name='{s}'], [aria-label*='{s}' i], button:has-text('{s}'), text='{s}'"

    def _ensure_browser(self):
        """Initializes or restores browser context and active page."""
        if self._page and not self._page.is_closed():
            return self._page

        from playwright.sync_api import sync_playwright

        self._playwright = sync_playwright().start()

        if self.persistent:
            self._context = self._playwright.chromium.launch_persistent_context(
                user_data_dir=str(BROWSER_PROFILE_DIR),
                headless=self.headless,
                slow_mo=self.slow_mo_ms,
                viewport={"width": 1280, "height": 800} if self.headless else None,
                args=["--start-maximized" if not self.headless else "--window-size=1280,800"]
            )
            pages = self._context.pages
            self._page = pages[0] if pages else self._context.new_page()
        else:
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

        # Dialog handler setup
        self._page.on("dialog", lambda dialog: dialog.accept() if self._dialog_action == "accept" else dialog.dismiss())
        return self._page

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> Dict[str, Any]:
        """Navigates to a specific URL (http/https or local file:/// path)."""
        page = self._ensure_browser()
        try:
            target_url = url
            if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file:///"):
                target_url = "https://" + url

            resp = page.goto(target_url, wait_until=wait_until, timeout=30000)
            status_code = resp.status if resp else 200

            # Automatically dismiss cookie banners if present
            self.dismiss_cookie_banner()

            return {
                "ok": True,
                "success": True,
                "url": page.url,
                "title": page.title(),
                "status": status_code,
                "message": f"Successfully navigated to {page.url}"
            }
        except Exception as e:
            return {"ok": False, "success": False, "error": str(e), "url": url}

    def _find_element(self, selector_or_text: str):
        """
        Resilient multi-tier element locator:
        Tier 1: Direct CSS / XPath selector
        Tier 2: ARIA role and label
        Tier 3: Placeholder / Test-ID
        Tier 4: Visible text match
        """
        page = self._ensure_browser()

        # 1. Direct CSS / XPath
        try:
            loc = page.locator(selector_or_text)
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        # 1b. Direct Name or ID match
        try:
            clean_token = selector_or_text.replace("'", "\\'")
            loc = page.locator(f"[name='{clean_token}'], [id='{clean_token}'], #{clean_token}")
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        # 2. Placeholder
        try:
            loc = page.get_by_placeholder(selector_or_text, exact=False)
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        # 3. Label
        try:
            loc = page.get_by_label(selector_or_text, exact=False)
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        # 4. Text
        try:
            loc = page.get_by_text(selector_or_text, exact=False)
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        # 5. Fuzzy match on buttons/links
        try:
            loc = page.locator(f"button:has-text('{selector_or_text}'), a:has-text('{selector_or_text}'), input[name='{selector_or_text}']")
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass

        return None

    def fill_field(self, selector_or_label: str, value: str, press_enter: bool = False, raise_on_failure: bool = False) -> Dict[str, Any]:
        """
        Fill form field using 100% Playwright-native DOM injection (Ref: Section 46.4).
        Wait for element to be ready (5 second timeout) and fills using Playwright native method.
        """
        page = self.page
        selector = self._resolve_selector(selector_or_label)
        last_err = None

        for attempt in range(1, 4):
            try:
                page.wait_for_selector(selector, timeout=5000, state='visible')
                loc = page.locator(selector).first
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.fill(value, timeout=5000)
                if press_enter:
                    loc.press("Enter")
                print(f"[BrowserAgent] Filled field '{selector}' with text")
                return {
                    "ok": True,
                    "success": True,
                    "selector": selector,
                    "value_filled": value,
                    "pressed_enter": press_enter,
                    "engine": "playwright_native"
                }
            except Exception as e:
                last_err = e
                try:
                    elem = self._find_element(selector_or_label)
                    if elem:
                        elem.scroll_into_view_if_needed(timeout=3000)
                        elem.fill(value, timeout=5000)
                        if press_enter:
                            elem.press("Enter")
                        print(f"[BrowserAgent] Filled field '{selector_or_label}' via DOM element")
                        return {
                            "ok": True,
                            "success": True,
                            "selector": selector_or_label,
                            "value_filled": value,
                            "pressed_enter": press_enter,
                            "engine": "playwright_native"
                        }
                except Exception as inner_e:
                    last_err = inner_e
                time.sleep(0.2)

        err_msg = f"[BrowserAgent] ERROR: Failed to fill field '{selector_or_label}' after 3 attempts: {str(last_err)}"
        print(err_msg)
        if raise_on_failure:
            raise BrowserAutomationError(err_msg)
        return {"ok": False, "success": False, "error": str(last_err), "selector": selector_or_label}

    def click_element(self, selector_or_text: str, force: bool = True, raise_on_failure: bool = False) -> Dict[str, Any]:
        """
        Click element using 100% Playwright-native DOM injection (Ref: Section 46.4).
        Wait for element to be ready (5s timeout), scroll into view, and click with force=True.
        """
        page = self.page
        selector = self._resolve_selector(selector_or_text)
        last_err = None

        for attempt in range(1, 4):
            try:
                page.wait_for_selector(selector, timeout=5000, state='visible')
                loc = page.locator(selector).first
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click(force=force, timeout=5000)
                print(f"[BrowserAgent] Clicked element '{selector}'")
                return {
                    "ok": True,
                    "success": True,
                    "action": "click",
                    "target": selector,
                    "engine": "playwright_native"
                }
            except Exception as e:
                last_err = e
                try:
                    elem = self._find_element(selector_or_text)
                    if elem:
                        elem.scroll_into_view_if_needed(timeout=3000)
                        elem.click(force=force, timeout=5000)
                        print(f"[BrowserAgent] Clicked element '{selector_or_text}' via DOM element")
                        return {
                            "ok": True,
                            "success": True,
                            "action": "click",
                            "target": selector_or_text,
                            "engine": "playwright_native"
                        }
                except Exception as inner_e:
                    last_err = inner_e
                time.sleep(0.2)

        err_msg = f"[BrowserAgent] ERROR: Failed to click element '{selector_or_text}' after 3 attempts: {str(last_err)}"
        print(err_msg)
        if raise_on_failure:
            raise BrowserAutomationError(err_msg)
        return {"ok": False, "success": False, "error": str(last_err), "target": selector_or_text}

    def submit_form(self, selector: str, raise_on_failure: bool = False) -> Dict[str, Any]:
        """Submit form using Playwright-native Enter key press (Ref: Section 46.4)"""
        page = self.page
        resolved = self._resolve_selector(selector)
        try:
            page.wait_for_selector(resolved, timeout=5000, state='visible')
            loc = page.locator(resolved).first
            loc.press('Enter')
            print(f"[BrowserAgent] Submitted form via Enter key on '{resolved}'")
            return {
                "ok": True,
                "success": True,
                "action": "submit",
                "target": resolved,
                "engine": "playwright_native"
            }
        except Exception as e:
            err_msg = f"[BrowserAgent] ERROR: Failed to submit form '{selector}': {str(e)}"
            print(err_msg)
            if raise_on_failure:
                raise BrowserAutomationError(err_msg)
            return {"ok": False, "success": False, "error": str(e), "target": selector}

    def double_click(self, selector_or_text: str) -> Dict[str, Any]:
        """Double clicks an element."""
        self._ensure_browser()
        elem = self._find_element(selector_or_text)
        if not elem:
            return {"ok": False, "error": f"Element '{selector_or_text}' not found for double click"}
        try:
            elem.scroll_into_view_if_needed(timeout=3000)
            elem.dblclick(timeout=5000)
            return {"ok": True, "action": "double_click", "target": selector_or_text}
        except Exception as e:
            return {"ok": False, "error": str(e), "target": selector_or_text}

    def right_click(self, selector_or_text: str) -> Dict[str, Any]:
        """Right clicks an element."""
        self._ensure_browser()
        elem = self._find_element(selector_or_text)
        if not elem:
            return {"ok": False, "error": f"Element '{selector_or_text}' not found for right click"}
        try:
            elem.scroll_into_view_if_needed(timeout=3000)
            elem.click(button="right", timeout=5000)
            return {"ok": True, "action": "right_click", "target": selector_or_text}
        except Exception as e:
            return {"ok": False, "error": str(e), "target": selector_or_text}

    def hover(self, selector_or_text: str) -> Dict[str, Any]:
        """Hovers mouse over an element."""
        self._ensure_browser()
        elem = self._find_element(selector_or_text)
        if not elem:
            return {"ok": False, "error": f"Element '{selector_or_text}' not found for hover"}
        try:
            elem.scroll_into_view_if_needed(timeout=3000)
            elem.hover(timeout=5000)
            return {"ok": True, "action": "hover", "target": selector_or_text}
        except Exception as e:
            return {"ok": False, "error": str(e), "target": selector_or_text}

    def select_dropdown(self, selector: str, value: str) -> Dict[str, Any]:
        """Selects an option in a `<select>` dropdown by value, label, or index."""
        page = self._ensure_browser()
        elem = self._find_element(selector)
        if not elem:
            return {"ok": False, "error": f"Dropdown element '{selector}' not found"}
        try:
            elem.select_option(value=value)
            return {"ok": True, "action": "select_dropdown", "target": selector, "selected": value}
        except Exception:
            try:
                elem.select_option(label=value)
                return {"ok": True, "action": "select_dropdown", "target": selector, "selected_label": value}
            except Exception as e:
                return {"ok": False, "error": str(e), "target": selector}

    def scroll_page(self, direction: str = "down", amount: int = 500) -> Dict[str, Any]:
        """Scrolls the page up or down naturally."""
        page = self._ensure_browser()
        try:
            delta_y = amount if direction.lower() == "down" else -amount
            page.mouse.wheel(0, delta_y)
            time.sleep(0.1)
            return {"ok": True, "action": "scroll", "direction": direction, "amount": amount}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def dismiss_cookie_banner(self) -> Dict[str, Any]:
        """Detects and closes common cookie consent dialogs."""
        page = self._ensure_browser()
        common_selectors = [
            "#accept-cookies", "button:has-text('Accept All')", "button:has-text('Accept all cookies')",
            "#cookie-notice button", ".cookie-banner button"
        ]
        dismissed = False
        for sel in common_selectors:
            try:
                loc = page.locator(sel)
                if loc.count() > 0:
                    loc.first.click(timeout=300)
                    dismissed = True
                    break
            except Exception:
                continue
        return {"ok": True, "dismissed_cookie_banner": dismissed}

    def wait_for_network_idle(self, timeout_ms: int = 5000) -> Dict[str, Any]:
        """Waits for active network requests to settle (ideal for SPAs)."""
        page = self._ensure_browser()
        try:
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
            return {"ok": True, "state": "networkidle"}
        except Exception:
            return {"ok": True, "state": "networkidle_timeout_reached"}

    # --- MULTI-TAB MANAGEMENT ---
    def list_tabs(self) -> Dict[str, Any]:
        """Lists all open tabs/pages in the browser context."""
        self._ensure_browser()
        tabs = []
        for idx, p in enumerate(self._context.pages):
            tabs.append({
                "index": idx,
                "url": p.url,
                "title": p.title(),
                "is_active": (p == self._page)
            })
        return {"ok": True, "tab_count": len(tabs), "tabs": tabs}

    def new_tab(self, url: str = "about:blank") -> Dict[str, Any]:
        """Opens a new tab and sets it as the active page."""
        self._ensure_browser()
        self._page = self._context.new_page()
        if url != "about:blank":
            return self.navigate_to(url)
        return {"ok": True, "action": "new_tab", "index": len(self._context.pages) - 1}

    def switch_tab(self, index: int) -> Dict[str, Any]:
        """Switches focus to the tab at specified index."""
        self._ensure_browser()
        pages = self._context.pages
        if 0 <= index < len(pages):
            self._page = pages[index]
            self._page.bring_to_front()
            return {"ok": True, "active_tab": index, "url": self._page.url, "title": self._page.title()}
        return {"ok": False, "error": f"Tab index {index} out of range (0..{len(pages)-1})"}

    def close_tab(self, index: Optional[int] = None) -> Dict[str, Any]:
        """Closes the current or indexed tab."""
        self._ensure_browser()
        pages = self._context.pages
        target = self._page if index is None else (pages[index] if 0 <= index < len(pages) else None)
        if target:
            target.close()
            remaining = self._context.pages
            self._page = remaining[-1] if remaining else None
            return {"ok": True, "remaining_tabs": len(remaining)}
        return {"ok": False, "error": "Invalid tab to close"}

    # --- DOM INSPECTION & FORM PERCEPTION ---
    def inspect_page_elements(self) -> Dict[str, Any]:
        """Extracts structured DOM elements: forms, inputs, buttons, and selects."""
        page = self._ensure_browser()
        try:
            data = page.evaluate("""
                () => {
                    const inputs = Array.from(document.querySelectorAll('input, textarea, select')).map((el, i) => ({
                        index: i,
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        name: el.name || '',
                        type: el.type || '',
                        placeholder: el.placeholder || '',
                        value: el.value || '',
                        isVisible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
                        ariaLabel: el.getAttribute('aria-label') || ''
                    }));

                    const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], a[role="button"]')).map((el, i) => ({
                        index: i,
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        text: (el.innerText || el.value || '').trim(),
                        ariaLabel: el.getAttribute('aria-label') || '',
                        isVisible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
                    }));

                    return {
                        title: document.title,
                        url: window.location.href,
                        inputs: inputs.filter(x => x.isVisible),
                        buttons: buttons.filter(x => x.isVisible)
                    };
                }
            """)
            data["ok"] = True
            data["success"] = True
            return data
        except Exception as e:
            return {"ok": False, "success": False, "error": str(e)}

    def get_element_text(self, selector_or_text: str) -> str:
        """Returns inner text of specified element."""
        self._ensure_browser()
        elem = self._find_element(selector_or_text)
        if elem:
            return elem.inner_text()
        return ""

    # --- SCREENSHOT & VISUAL OBSERVABILITY ---
    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """Captures page screenshot to disk."""
        page = self._ensure_browser()
        try:
            fname = filename or f"browser_snap_{int(time.time())}.png"
            dest = SCREENSHOTS_DIR / fname
            page.screenshot(path=str(dest), full_page=False)
            return {"ok": True, "screenshot_path": str(dest)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # --- MULTI-STEP FLOW EXECUTION ---
    def execute_flow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes a multi-step web workflow:
        Example:
          [
            {"action": "navigate", "url": "https://example.com"},
            {"action": "fill", "selector": "#username", "value": "testuser"},
            {"action": "click", "selector": "button[type='submit']"}
          ]
        """
        results = []
        for idx, step in enumerate(steps):
            act = step.get("action", "").lower()
            res = {"step": idx, "action": act, "ok": False}
            try:
                if act == "navigate":
                    res = self.navigate_to(step["url"])
                elif act == "fill":
                    val = step.get("value") if step.get("value") is not None else step.get("text", "")
                    res = self.fill_field(step["selector"], val, step.get("enter", False))
                elif act == "click":
                    res = self.click_element(step["selector"])
                elif act == "double_click":
                    res = self.double_click(step["selector"])
                elif act == "right_click":
                    res = self.right_click(step["selector"])
                elif act == "hover":
                    res = self.hover(step["selector"])
                elif act == "select":
                    val = step.get("value") if step.get("value") is not None else step.get("text", "")
                    res = self.select_dropdown(step["selector"], val)
                elif act == "scroll":
                    res = self.scroll_page(step.get("direction", "down"), step.get("amount", 500))
                elif act == "wait":
                    time.sleep(step.get("seconds", 1))
                    res = {"ok": True, "success": True, "action": "wait"}
                elif act == "screenshot":
                    res = self.take_screenshot(step.get("filename"))
                else:
                    res["error"] = f"Unknown flow action: {act}"
            except Exception as e:
                res["error"] = str(e)

            results.append(res)
            if not (res.get("ok", False) or res.get("success", False)):
                return {"ok": False, "success": False, "failed_at_step": idx, "steps_completed": results, "completed_steps": len(results)}

        return {"ok": True, "success": True, "steps_completed": results, "completed_steps": len(results)}

    def close_browser(self):
        """Cleanly releases browser resources."""
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

    def type_and_submit(self, text: str, selector: Optional[str] = None) -> Dict[str, Any]:
        """
        [DEPRECATED FOR DIRECT OS AUTOMATION IN WEB CONTEXTS — Ref: Master Technical Reference Section 46.4]
        Enforces 100% Playwright-native execution for all web contexts.
        Uses page.locator(selector).fill(text) followed by page.locator(selector).press('Enter')
        with explicit page.wait_for_selector(timeout=5000).
        """
        try:
            page = self._ensure_browser()
            target_sel = selector or "input:focus, textarea:focus, [contenteditable='true']:focus, input:not([type='hidden']), textarea"
            try:
                page.wait_for_selector(target_sel, timeout=5000, state="attached")
                loc = page.locator(target_sel).first
                loc.fill(text, timeout=5000)
                loc.press("Enter")
                return {
                    "ok": True,
                    "success": True,
                    "text": text,
                    "selector": target_sel,
                    "submitted": True,
                    "engine": "playwright_native",
                    "deprecated_os_fallback": True
                }
            except Exception:
                page.keyboard.type(text)
                page.keyboard.press("Enter")
                return {
                    "ok": True,
                    "success": True,
                    "text": text,
                    "submitted": True,
                    "engine": "playwright_native_keyboard",
                    "deprecated_os_fallback": True
                }
        except Exception as e:
            return {"ok": False, "success": False, "error": str(e), "engine": "playwright_native"}

    # --- 100% PLAYWRIGHT-NATIVE ACTIVE BROWSER ACTION ---
    @staticmethod
    def os_type_and_submit_in_browser(text: str, selector: Optional[str] = None, agent: Optional['SaraInteractiveBrowserAgent'] = None) -> Dict[str, Any]:
        """
        [DEPRECATED FOR DIRECT OS AUTOMATION IN WEB CONTEXTS — Ref: Master Technical Reference Section 46.4]
        Eradicates PyAutoGUI browser fallback in web contexts in favor of 100% Playwright-native execution.
        Uses page.locator(selector).fill(text) followed by page.locator(selector).press('Enter')
        with explicit page.wait_for_selector(timeout=5000).
        OS-level paste (Win32/pyautogui) is strictly preserved ONLY for non-browser desktop applications.
        """
        global browser_agent
        target_agent = agent or browser_agent
        return target_agent.type_and_submit(text, selector=selector)


# Global interactive agent instance
browser_agent = SaraInteractiveBrowserAgent(headless=True)
