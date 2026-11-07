# -*- coding: utf-8 -*-
"""
Tests for SARA AI 2.5 Pro — APInex Multi-Model Neural Provider (High-End Engine)
Follows strict TDD: Red -> Green -> Refactor.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestAPInexProvider(unittest.TestCase):

    def setUp(self):
        # Import target module
        from sara_apinex_provider import APInexProvider, VERIFIED_WORKING_MODELS, TASK_MODEL_ROUTING
        self.provider_cls = APInexProvider
        self.verified_models = VERIFIED_WORKING_MODELS
        self.routing = TASK_MODEL_ROUTING

    def test_verified_models_catalog(self):
        """Ensures all 9 live-verified models are registered in provider ranking."""
        self.assertIn("free/glm-5.3-flashx", self.verified_models)
        self.assertIn("free/gemini-3.8-flash", self.verified_models)
        self.assertIn("free/deepseek-v4-pro-0813", self.verified_models)
        self.assertIn("free/kimi-k3", self.verified_models)
        self.assertGreaterEqual(len(self.verified_models), 9)

    def test_task_routing_matrix(self):
        """Verifies intelligent task-to-model specialization routing."""
        self.assertEqual(self.routing["fast_chat"], "free/glm-5.3-flashx")
        self.assertEqual(self.routing["urdu_nuance"], "free/gemini-3.8-flash")
        self.assertEqual(self.routing["coding_architecture"], "free/deepseek-v4-pro-0813")
        self.assertEqual(self.routing["deep_research"], "free/kimi-k3")

    def test_unconfigured_token_handling(self):
        """Verifies graceful fallback response when API key is missing."""
        provider = self.provider_cls(api_key="")
        self.assertFalse(provider.is_configured())
        res = provider.generate_chat("Hello SARA", task_type="fast_chat")
        self.assertFalse(res["success"])
        self.assertTrue(res.get("fallback_recommended", False))

    def test_mock_successful_generation(self):
        """Verifies successful prompt formatting and response extraction."""
        provider = self.provider_cls(api_key="mock_test_key_12345")
        self.assertTrue(provider.is_configured())

        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices": [{"message": {"content": "SARA Online, Pasha Jan!"}}]}'
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response):
            res = provider.generate_chat("Kaisi ho SARA?", task_type="urdu_nuance")
            self.assertTrue(res["success"])
            self.assertEqual(res["model_used"], "free/gemini-3.8-flash")
            self.assertEqual(res["text"], "SARA Online, Pasha Jan!")
            self.assertGreater(res["latency_ms"], 0)

    def test_automatic_failover_on_429_or_error(self):
        """Verifies automatic fallback cascade if the primary model errors out."""
        import urllib.error
        provider = self.provider_cls(api_key="mock_test_key_12345")

        # Mock first call failing with 429, second call succeeding
        mock_success = MagicMock()
        mock_success.read.return_value = b'{"choices": [{"message": {"content": "Fallback Model Online"}}]}'
        mock_success.__enter__.return_value = mock_success

        err_429 = urllib.error.HTTPError(
            url="http://test", code=429, msg="Rate limit", hdrs={}, fp=None
        )

        with patch("urllib.request.urlopen", side_effect=[err_429, mock_success]):
            res = provider.generate_chat("Test prompt", task_type="fast_chat", max_retries=2)
            self.assertTrue(res["success"])
            self.assertEqual(res["text"], "Fallback Model Online")
            self.assertTrue(res.get("failover_occurred", False))

    def test_high_end_system_prompt_injection(self):
        """Verifies that Pasha Jan's verified identity and NEXORA constraints are injected."""
        provider = self.provider_cls(api_key="mock_test_key_12345")
        sys_prompt = provider.build_system_prompt()
        self.assertIn("Pasha Jan", sys_prompt)
        self.assertIn("+923332656733", sys_prompt)
        self.assertIn("NEXORA", sys_prompt)


if __name__ == "__main__":
    unittest.main()

