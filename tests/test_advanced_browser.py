"""
SARA AI 2.5 — ADVANCED AUTONOMOUS BROWSER TEST SUITE
Verifies:
  1. Multi-tier element resolution and form filling
  2. Dropdown selection, scrolling, and cookie banner dismissal
  3. Single Page App (SPA) dynamic tab switching & network idle
  4. Multi-tab context management (open, list, switch, close)
  5. Flow runner execution and screenshot verification
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_interactive_browser import SaraInteractiveBrowserAgent


class TestAdvancedAutonomousBrowser(unittest.TestCase):

    def setUp(self):
        self.browser_agent = SaraInteractiveBrowserAgent(headless=True)
        self.test_dir = PROJECT_ROOT / "data" / "test_web"

    def tearDown(self):
        self.browser_agent.close_browser()

    def test_form_interaction_and_cookie_dismissal(self):
        """Verifies full form automation, dropdown selection, and cookie banner dismissal."""
        form_url = (self.test_dir / "form_app.html").as_uri()
        nav_res = self.browser_agent.navigate_to(form_url)
        self.assertTrue(nav_res["ok"])

        # Inspect DOM
        inspect_res = self.browser_agent.inspect_page_elements()
        self.assertTrue(inspect_res["ok"])
        self.assertTrue(len(inspect_res["inputs"]) >= 4)

        # Fill fields using multi-tier locators (id, placeholder, label)
        fill1 = self.browser_agent.fill_field("#full-name", "Muhammad Mubashar")
        self.assertTrue(fill1["ok"])

        fill2 = self.browser_agent.fill_field("name@example.com", "pashadev804@gmail.com")
        self.assertTrue(fill2["ok"])

        fill3 = self.browser_agent.fill_field("taskDesc", "Autonomous engineering overhaul test")
        self.assertTrue(fill3["ok"])

        # Select dropdown option
        drop_res = self.browser_agent.select_dropdown("#project-type", "desktop_ai")
        self.assertTrue(drop_res["ok"])

        # Click submit button
        submit_res = self.browser_agent.click_element("#submit-btn")
        self.assertTrue(submit_res["ok"])

        # Verify page state
        page = self.browser_agent._page
        status_text = page.locator("#status-msg").inner_text()
        self.assertIn("Form Successfully Submitted by SARA!", status_text)

    def test_spa_dynamic_tab_switching(self):
        """Verifies handling of client-side SPAs, dynamic state rendering, and network idle."""
        spa_url = (self.test_dir / "spa_app.html").as_uri()
        self.browser_agent.navigate_to(spa_url)

        # Click Async Data tab
        self.browser_agent.click_element("#tab-data")
        # Wait for async rendering
        self.browser_agent.wait_for_network_idle(timeout_ms=1000)
        self.browser_agent.scroll_page("down", 100)

        page = self.browser_agent._page
        page.wait_for_selector("#data-list", timeout=3000)
        data_text = page.locator("#data-list").inner_text()
        self.assertIn("Node Agents: 14 Active", data_text)

        # Click Live Logs tab
        self.browser_agent.click_element("#tab-logs")
        page.wait_for_selector("#log-box", timeout=3000)
        log_text = page.locator("#log-box").inner_text()
        self.assertIn("WebSocket 24kHz stream online", log_text)

    def test_multi_tab_context_management(self):
        """Verifies opening new tabs, listing them, switching, and closing."""
        url1 = (self.test_dir / "form_app.html").as_uri()
        url2 = (self.test_dir / "spa_app.html").as_uri()

        self.browser_agent.navigate_to(url1)
        self.browser_agent.new_tab(url2)

        # List tabs
        tabs_res = self.browser_agent.list_tabs()
        self.assertTrue(tabs_res["ok"])
        self.assertEqual(tabs_res["tab_count"], 2)

        # Switch back to tab 0
        switch_res = self.browser_agent.switch_tab(0)
        self.assertTrue(switch_res["ok"])
        self.assertEqual(switch_res["active_tab"], 0)
        self.assertIn("form_app.html", switch_res["url"])

        # Close tab 1
        close_res = self.browser_agent.close_tab(1)
        self.assertTrue(close_res["ok"])
        self.assertEqual(close_res["remaining_tabs"], 1)

    def test_flow_execution_and_screenshot(self):
        """Verifies execution of multi-step autonomous workflows and screenshot capture."""
        form_url = (self.test_dir / "form_app.html").as_uri()
        flow = [
            {"action": "navigate", "url": form_url},
            {"action": "fill", "selector": "#full-name", "value": "Pasha Dev"},
            {"action": "fill", "selector": "#email-addr", "value": "pasha@dev.com"},
            {"action": "click", "selector": "#submit-btn"},
            {"action": "screenshot", "filename": "test_flow_complete.png"}
        ]
        res = self.browser_agent.execute_flow(flow)
        self.assertTrue(res["ok"])
        self.assertEqual(len(res["steps_completed"]), 5)

        snap_path = PROJECT_ROOT / "data" / "screenshots" / "test_flow_complete.png"
        self.assertTrue(snap_path.exists())


if __name__ == "__main__":
    unittest.main()

