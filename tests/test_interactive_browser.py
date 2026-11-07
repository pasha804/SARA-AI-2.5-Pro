# -*- coding: utf-8 -*-
"""
Tests for SARA AI 2.5 Pro — Interactive Browser Agent
Verifies:
  1. Browser launching & navigation (Playwright Chromium)
  2. Inspecting form fields, inputs, and interactive buttons
  3. Filling input fields, textareas, and typing text
  4. Clicking buttons and submitting forms
  5. Multi-step automated browser flow execution
"""

import unittest
from pathlib import Path
import json

BASE_DIR = Path(r"D:\MARAA AI").resolve()

class TestInteractiveBrowserAgent(unittest.TestCase):

    def setUp(self):
        from sara_interactive_browser import SaraInteractiveBrowserAgent
        self.browser_agent = SaraInteractiveBrowserAgent(headless=True)

    def tearDown(self):
        self.browser_agent.close_browser()

    def test_inspect_and_fill_form(self):
        # Create a mock HTML page with inputs and a button
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Pasha Dev Portal</title></head>
        <body>
            <h1>Welcome Pasha Jan</h1>
            <form id="contact-form">
                <input type="text" id="username" name="username" placeholder="Enter your name" />
                <input type="email" id="useremail" placeholder="Enter your email" />
                <textarea id="message" placeholder="Your message here"></textarea>
                <button type="button" id="submit-btn" onclick="document.getElementById('result').innerText = 'Submitted by ' + document.getElementById('username').value;">Submit</button>
            </form>
            <div id="result">Waiting</div>
        </body>
        </html>
        """
        temp_html_path = BASE_DIR / "data" / "test_form.html"
        temp_html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(mock_html)

        url = f"file:///{temp_html_path.as_posix()}"
        nav_res = self.browser_agent.navigate_to(url)
        self.assertTrue(nav_res["success"])
        self.assertEqual(nav_res["title"], "Pasha Dev Portal")

        # 1. Inspect Form Fields
        inspect_res = self.browser_agent.inspect_page_elements()
        self.assertTrue(inspect_res["success"])
        self.assertGreaterEqual(len(inspect_res["inputs"]), 3)
        self.assertGreaterEqual(len(inspect_res["buttons"]), 1)

        # 2. Fill Input Fields
        fill_user = self.browser_agent.fill_field("#username", "Muhammad Mubashar")
        self.assertTrue(fill_user["success"])

        fill_email = self.browser_agent.fill_field("#useremail", "pashadev804@gmail.com")
        self.assertTrue(fill_email["success"])

        fill_msg = self.browser_agent.fill_field("#message", "Testing SARA interactive browser agent")
        self.assertTrue(fill_msg["success"])

        # 3. Click Submit Button
        click_res = self.browser_agent.click_element("#submit-btn")
        self.assertTrue(click_res["success"])

        # 4. Verify DOM Updated
        text_content = self.browser_agent.get_element_text("#result")
        self.assertIn("Submitted by Muhammad Mubashar", text_content)

        # Clean up temp file
        if temp_html_path.exists():
            temp_html_path.unlink()

    def test_multi_step_flow_execution(self):
        mock_html = """
        <!DOCTYPE html>
        <html>
        <body>
            <input type="text" id="search-box" placeholder="Search..." />
            <button id="search-btn" onclick="document.body.innerHTML += '<p id=found>Query: ' + document.getElementById('search-box').value + '</p>';">Go</button>
        </body>
        </html>
        """
        temp_html_path = BASE_DIR / "data" / "test_flow.html"
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(mock_html)

        url = f"file:///{temp_html_path.as_posix()}"
        flow_steps = [
            {"action": "navigate", "url": url},
            {"action": "fill", "selector": "#search-box", "text": "Pasha Dev AI"},
            {"action": "click", "selector": "#search-btn"}
        ]

        flow_res = self.browser_agent.execute_flow(flow_steps)
        self.assertTrue(flow_res["success"])
        self.assertEqual(flow_res["completed_steps"], 3)

        found_text = self.browser_agent.get_element_text("#found")
        self.assertIn("Query: Pasha Dev AI", found_text)

        if temp_html_path.exists():
            temp_html_path.unlink()


if __name__ == "__main__":
    unittest.main()
