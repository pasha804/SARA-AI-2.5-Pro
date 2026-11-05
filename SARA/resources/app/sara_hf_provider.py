# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Hugging Face Inference Providers Adapter
Provides access to hosted frontier open-weight models via official HF Inference Providers:
  - Meta Llama 3.3 70B Instruct
  - DeepSeek R1 Distill Qwen 32B
  - Qwen 2.5 Coder 32B Instruct
  - Mistral 7B Instruct v0.3
Features:
  - Hosted cloud inference (Zero local heavy weight downloads)
  - Secure token resolution via .env (HF_TOKEN or HUGGINGFACE_API_KEY)
  - Usage-aware timeout & automatic fallback to Google Gemini
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

APP_ENV = Path(r"D:\MARAA AI\SARA\resources\app\.env").resolve()
load_dotenv(APP_ENV)

HF_INFERENCE_ROUTER = "https://router.huggingface.co/hf-inference/v1/chat/completions"
HF_CLASSIC_ENDPOINT = "https://api-inference.huggingface.co/v1/chat/completions"

SUPPORTED_HF_MODELS = {
    "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-r1-32b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "qwen-coder-32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "mistral-7b": "mistralai/Mistral-7B-Instruct-v0.3"
}


class HuggingFaceProvider:
    def __init__(self, api_token: Optional[str] = None):
        self.token = api_token or os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN") or ""

    def is_configured(self) -> bool:
        """Returns True if a Hugging Face API key is configured."""
        return bool(self.token and len(self.token) > 8)

    def get_supported_models(self) -> Dict[str, str]:
        return SUPPORTED_HF_MODELS.copy()

    def generate_chat(
        self,
        messages: Any,
        model_alias: Optional[str] = None,
        model_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        timeout: int = 20
    ) -> Dict[str, Any]:
        """
        Executes hosted inference call against Hugging Face Inference Providers.
        Supports both raw string prompt or messages list, and both model_alias or model_id.
        Automatically falls back if unavailable.
        """
        chosen_model = model_id or model_alias or "qwen-coder-32b"
        resolved_model = SUPPORTED_HF_MODELS.get(chosen_model, chosen_model)

        if isinstance(messages, str):
            formatted_messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list):
            formatted_messages = messages
        else:
            formatted_messages = [{"role": "user", "content": str(messages)}]

        if not self.is_configured():
            return {
                "success": False,
                "provider": "huggingface",
                "error": "HUGGINGFACE_API_KEY or HF_TOKEN not configured in .env",
                "fallback_recommended": True
            }

        payload = {
            "model": resolved_model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        data_bytes = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        # Try Router endpoint first, then classic fallback
        endpoints = [HF_INFERENCE_ROUTER, HF_CLASSIC_ENDPOINT]
        last_error = None

        for endpoint in endpoints:
            try:
                req = urllib.request.Request(endpoint, data=data_bytes, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    choice = res.get("choices", [{}])[0]
                    content = choice.get("message", {}).get("content", "")
                    return {
                        "success": True,
                        "provider": "huggingface",
                        "model": resolved_model,
                        "text": content,
                        "usage": res.get("usage", {})
                    }
            except urllib.error.HTTPError as e:
                last_error = f"HTTP {e.code}: {e.reason}"
                if e.code in (401, 403):
                    break  # Auth failure, no need to retry endpoint
            except Exception as e:
                last_error = str(e)

        return {
            "success": False,
            "provider": "huggingface",
            "model": resolved_model,
            "error": last_error or "Inference request failed",
            "fallback_recommended": True
        }


# Singleton Instance
hf_provider = HuggingFaceProvider()

if __name__ == "__main__":
    print("Testing Hugging Face Inference Provider Adapter...")
    print("Configured:", hf_provider.is_configured())
    print("Supported Models:", list(hf_provider.get_supported_models().keys()))
    res = hf_provider.generate_chat([{"role": "user", "content": "Hello"}])
    print("Test Response:", res)

