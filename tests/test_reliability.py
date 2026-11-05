# -*- coding: utf-8 -*-
"""
Automated Reliability & Filesystem Regression Tests for SARA AI 2.5 Pro
Tests path resolution, verified writes, unicode handling, and tool response contracts.
"""

import sys
import unittest
from pathlib import Path

# Add root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from sara_path_resolver import (
    resolve_user_path,
    create_verified_file,
    create_verified_dir,
    open_path_verified,
    format_tool_response,
    REAL_DESKTOP,
    USER_PROFILE
)


class TestSaraReliability(unittest.TestCase):

    def test_01_desktop_path_resolution(self):
        """Verify that relative 'Desktop/test' maps to real user Desktop."""
        resolved = resolve_user_path("Desktop/test_subfolder")
        expected = (REAL_DESKTOP / "test_subfolder").resolve()
        self.assertEqual(resolved, expected)

    def test_02_tilde_path_resolution(self):
        """Verify that '~' maps to user profile."""
        resolved = resolve_user_path("~/Projects/test")
        expected = (USER_PROFILE / "Projects/test").resolve()
        self.assertEqual(resolved, expected)

    def test_03_paths_with_spaces_and_parentheses(self):
        """Verify paths containing spaces and parentheses resolve cleanly."""
        raw = "Desktop/My Project (Pasha Dev 2026)/app.js"
        resolved = resolve_user_path(raw)
        self.assertIn("My Project (Pasha Dev 2026)", str(resolved))
        self.assertTrue(resolved.is_absolute())

    def test_04_verified_file_creation_with_unicode(self):
        """Test file creation, size verification, and UTF-8 Urdu readback."""
        test_file = "Desktop/sara_test_unicode_verified.txt"
        urdu_content = "پاشا دیو (Pasha Dev) — سارہ اے آئی پرو مکمل خود مختار ٹیسٹ"
        
        result = create_verified_file(test_file, urdu_content)
        self.assertTrue(result["success"], f"Create failed: {result.get('error')}")
        self.assertIn("hash_sha256", result["data"])
        self.assertTrue(result["verification"]["readback_verified"])
        
        # Cleanup
        p = Path(result["data"]["path"])
        if p.exists():
            p.unlink()

    def test_05_verified_directory_creation(self):
        """Test directory creation and existence validation."""
        test_dir = "Desktop/sara_test_dir_verified"
        result = create_verified_dir(test_dir)
        self.assertTrue(result["success"])
        self.assertTrue(result["verification"]["exists"])
        
        # Cleanup
        p = Path(result["data"]["path"])
        if p.exists():
            p.rmdir()

    def test_06_nonexistent_path_open_error_handling(self):
        """Verify open_path_verified distinguishes nonexistent targets."""
        fake_path = "Desktop/nonexistent_folder_xyz_12345"
        result = open_path_verified(fake_path)
        self.assertFalse(result["success"])
        self.assertIn("does not exist", result["error"])

    def test_07_standard_tool_response_contract(self):
        """Verify all 8 standardized contract fields exist in tool responses."""
        resp = format_tool_response(
            tool="testTool",
            operation="sample_op",
            success=True,
            data={"val": 42},
            message="Test executed",
            duration_ms=12.5
        )
        required_keys = ["success", "tool", "operation", "message", "data", "error", "duration_ms", "verification", "timestamp"]
        for k in required_keys:
            self.assertIn(k, resp, f"Missing required response field: {k}")


if __name__ == "__main__":
    unittest.main()
