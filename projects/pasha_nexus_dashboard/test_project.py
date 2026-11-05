# -*- coding: utf-8 -*-
import unittest
import os
import json
import py_compile
from pathlib import Path

class TestPashaNexus(unittest.TestCase):
    def test_syntax_server_py(self):
        p = Path(__file__).parent / "server.py"
        py_compile.compile(str(p), doraise=True)
        self.assertTrue(p.exists())

    def test_manifest_package_json(self):
        p = Path(__file__).parent / "package.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(data.get("version"), "1.0.0")

    def test_index_html_exists(self):
        p = Path(__file__).parent / "index.html"
        self.assertTrue(p.exists())
        self.assertIn("Pasha Nexus", p.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
