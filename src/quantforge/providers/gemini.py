"""Gemini adapter via Google's OpenAI-compatible Chat Completions endpoint.

The adapter makes one request per call and intentionally performs no automatic
retries. API keys are read from GEMINI_API_KEY and are never logged.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .base import ModelResponse, ProviderError

DEFAULT_MODEL = "gemini-3.8-flash"
DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"


class GeminiProvider:
    provider_name = "google-gemini"

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.timeout_seconds = timeout_seconds
        if not self.api_key:
            raise ProviderError("GEMINI_API_KEY is not configured")
        if not self.model_name.strip():
            raise ProviderError("Gemini model name must not be empty")
        if timeout_seconds <= 0:
            raise ProviderError("timeout_seconds must be positive")

    def generate(self, prompt: str) -> ModelResponse:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")

        body = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt.strip()}],
            "temperature": 0,
            "max_tokens": 512,
        }
        request = urllib.request.Request(
            DEFAULT_BASE_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
                request_id = response.headers.get("x-request-id") or response.headers.get("request-id")
        except urllib.error.HTTPError as exc:
            # Do not include request headers or the API key in error messages.
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise ProviderError(f"Gemini HTTP {exc.code}: {detail}") from None
        except urllib.error.URLError as exc:
            raise ProviderError(f"Gemini connection error: {exc.reason}") from None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderError(f"Gemini returned an invalid JSON response: {type(exc).__name__}") from None
        except TimeoutError:
            raise ProviderError("Gemini request timed out") from None

        try:
            choice = payload["choices"][0]
            message = choice["message"]
            output_text = message["content"]
            if not isinstance(output_text, str):
                raise TypeError("message content is not text")
            usage = payload.get("usage") or {}
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"Gemini response schema was unexpected: {type(exc).__name__}") from None

        return ModelResponse(
            provider=self.provider_name,
            model=self.model_name,
            output_text=output_text,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            request_id=request_id or payload.get("id"),
        )
