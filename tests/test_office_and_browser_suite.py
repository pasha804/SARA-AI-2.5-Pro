# -*- coding: utf-8 -*-
import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(r"D:\MARAA AI").resolve()
sys.path.insert(0, str(BASE_DIR))

from sara_office_and_browser_suite import word_engine, ppt_engine, browser_engine, DOCS_DIR, PPT_DIR


class TestOfficeAndBrowserSuite(unittest.TestCase):

    def test_word_document_creation_and_reading(self):
        """Test MS Word .docx creation, styling, and text extraction."""
        test_filename = "test_unit_word_doc.docx"
        res = word_engine.create_word_document(
            title="Unit Test Word Document",
            subtitle="Testing SARA Word Engine",
            author="Pasha Dev",
            filename=test_filename,
            open_after_create=False
        )
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("filename"), test_filename)
        self.assertTrue(Path(res.get("file_path")).exists())
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

        # Read the file
        read_res = word_engine.read_word_document(res["file_path"])
        self.assertTrue(read_res.get("success"))
        self.assertGreater(read_res.get("total_paragraphs", 0), 0)
        self.assertGreater(read_res.get("total_characters", 0), 100)

        # Cleanup test file
        if Path(res["file_path"]).exists():
            Path(res["file_path"]).unlink()

    def test_powerpoint_presentation_creation_and_reading(self):
        """Test PowerPoint .pptx executive slide deck generation and slide reading."""
        test_filename = "test_unit_deck.pptx"
        res = ppt_engine.create_presentation(
            title="Unit Test Executive Deck",
            subtitle="Testing SARA PPT Engine",
            author="Pasha Dev",
            filename=test_filename,
            theme="dark_executive",
            open_after_create=False
        )
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("filename"), test_filename)
        self.assertEqual(res.get("total_slides"), 5)
        self.assertTrue(Path(res.get("file_path")).exists())
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

        # Read the presentation
        read_res = ppt_engine.read_presentation(res["file_path"])
        self.assertTrue(read_res.get("success"))
        self.assertEqual(read_res.get("total_slides"), 5)
        self.assertTrue(len(read_res.get("slides", [])) == 5)

        # Cleanup test file
        if Path(res["file_path"]).exists():
            Path(res["file_path"]).unlink()

    def test_browser_search_and_url_handling(self):
        """Test search query URL generation and spoken notification."""
        res = browser_engine.search_web("FastAPI Python official documentation", engine="google", open_browser=False)
        self.assertTrue(res.get("success"))
        self.assertIn("google.com/search?q=", res.get("search_url", ""))
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

        res_yt = browser_engine.search_web("Three.js anime avatar tutorial", engine="youtube", open_browser=False)
        self.assertTrue(res_yt.get("success"))
        self.assertIn("youtube.com/results?search_query=", res_yt.get("search_url", ""))


if __name__ == "__main__":
    unittest.main()
