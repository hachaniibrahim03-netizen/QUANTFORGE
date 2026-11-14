"""FreeLLMAPI local OpenAI-compatible gateway adapter.

Only loopback URLs are accepted. Credentials are read from environment variables
and are never written to artifacts or logs. One request is sent per call.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlparse

from .base import ModelResponse, ProviderError

DEFAULT_BASE_URL = "http://127.0.0.1:31415/v1"


def _validated_chat_completions_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ProviderError(
            "FreeLLMAPI must use an HTTP loopback URL (127.0.0.1, localhost, or ::1)"
        )
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ProviderError("FreeLLMAPI base URL must not contain credentials, query, or fragment")
    return base_url.rstrip("/") + "/chat/completions"


class FreeLLMAPIProvider:
    provider_name = "freellmapi"

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 45.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("FREELLMAPI_API_KEY")
        self.model_name = model_name or os.getenv("FREELLMAPI_MODEL")
        self.base_url = base_url or os.getenv("FREELLMAPI_BASE_URL", DEFAULT_BASE_URL)
        self.timeout_seconds = timeout_seconds

        if not self.api_key:
            raise ProviderError("FREELLMAPI_API_KEY is not configured")
        if not self.model_name or not self.model_name.strip():
            raise ProviderError(
                "FREELLMAPI_MODEL is not configured; set it to an exact model ID shown in the gateway"
            )
        if timeout_seconds <= 0:
            raise ProviderError("timeout_seconds must be positive")
        self.endpoint = _validated_chat_completions_url(self.base_url)

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
            self.endpoint,
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
                request_id = (
                    response.headers.get("x-request-id")
                    or response.headers.get("request-id")
                    or response.headers.get("x-correlation-id")
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise ProviderError(f"FreeLLMAPI HTTP {exc.code}: {detail}") from None
        except urllib.error.URLError as exc:
            raise ProviderError(f"FreeLLMAPI connection error: {exc.reason}") from None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderError(
                f"FreeLLMAPI returned invalid JSON: {type(exc).__name__}"
            ) from None
        except TimeoutError:
            raise ProviderError("FreeLLMAPI request timed out") from None

        try:
            choice = payload["choices"][0]
            message = choice["message"]
            output_text = message["content"]
            if not isinstance(output_text, str):
                raise TypeError("message content is not text")
            usage = payload.get("usage") or {}
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(
                f"FreeLLMAPI response schema was unexpected: {type(exc).__name__}"
            ) from None

        return ModelResponse(
            provider=self.provider_name,
            model=self.model_name,
            output_text=output_text,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            request_id=request_id or payload.get("id"),
        )
