import unittest

from quantforge.providers import MockProvider
from quantforge.task_runner import run_smoke


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


if __name__ == "__main__":
    unittest.main()
