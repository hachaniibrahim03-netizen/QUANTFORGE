import json
import unittest
from unittest.mock import patch

from quantforge.providers import (
    FreeLLMAPIProvider,
    GeminiProvider,
    MockProvider,
    ProviderError,
)
from quantforge.task_runner import run_smoke


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.headers = {"x-request-id": "fake-provider-request"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class ProviderContractTests(unittest.TestCase):
    def test_mock_provider_returns_normalized_response(self):
        result = MockProvider().generate("hello")
        self.assertEqual(result.provider, "mock")
        self.assertEqual(result.model, "deterministic-echo-v1")
        self.assertEqual(result.output_text, "MOCK_OK: hello")
        self.assertEqual(result.request_id, "mock-request-0001")

    def test_empty_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            MockProvider().generate("   ")

    def test_smoke_result_is_auditable_and_explicitly_mock(self):
        result = run_smoke("test task")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["execution_mode"], "mock_only_no_external_api_call")
        self.assertEqual(len(result["prompt_sha256"]), 64)
        self.assertIn("timestamp_utc", result)
        self.assertGreaterEqual(result["latency_ms"], 0)

    def test_gemini_requires_key_without_network_access(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ProviderError):
                GeminiProvider()

    def test_gemini_adapter_normalizes_openai_compatible_response(self):
        payload = {
            "id": "chatcmpl-test",
            "choices": [{"message": {"content": "adapter works"}}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 4},
        }
        with patch("quantforge.providers.gemini.urllib.request.urlopen", return_value=FakeResponse(payload)):
            response = GeminiProvider(api_key="test-key").generate("hello")
        self.assertEqual(response.provider, "google-gemini")
        self.assertEqual(response.output_text, "adapter works")
        self.assertEqual(response.input_tokens, 12)
        self.assertEqual(response.output_tokens, 4)
        self.assertEqual(response.request_id, "fake-provider-request")

    def test_freellmapi_adapter_normalizes_local_gateway_response(self):
        payload = {
            "id": "gateway-test",
            "choices": [{"message": {"content": "local gateway works"}}],
            "usage": {"prompt_tokens": 9, "completion_tokens": 3},
        }
        with patch("quantforge.providers.freellmapi.urllib.request.urlopen", return_value=FakeResponse(payload)):
            provider = FreeLLMAPIProvider(
                api_key="test-key",
                model_name="exact-model-id",
            )
            response = provider.generate("hello")
        self.assertEqual(provider.endpoint, "http://127.0.0.1:31415/v1/chat/completions")
        self.assertEqual(response.provider, "freellmapi")
        self.assertEqual(response.model, "exact-model-id")
        self.assertEqual(response.output_text, "local gateway works")
        self.assertEqual(response.input_tokens, 9)
        self.assertEqual(response.output_tokens, 3)

    def test_freellmapi_rejects_non_loopback_hosts(self):
        with self.assertRaises(ProviderError):
            FreeLLMAPIProvider(
                api_key="test-key",
                model_name="exact-model-id",
                base_url="http://0.0.0.0:31415/v1",
            )

    def test_freellmapi_requires_explicit_model_id(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ProviderError):
                FreeLLMAPIProvider(api_key="test-key")


if __name__ == "__main__":
    unittest.main()
