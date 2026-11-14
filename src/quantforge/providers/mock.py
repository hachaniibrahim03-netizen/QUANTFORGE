"""Deterministic provider used only for local/CI contract tests."""
from .base import ModelResponse


class MockProvider:
    provider_name = "mock"
    model_name = "deterministic-echo-v1"

    def generate(self, prompt: str) -> ModelResponse:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        output = f"MOCK_OK: {prompt.strip()}"
        return ModelResponse(
            provider=self.provider_name,
            model=self.model_name,
            output_text=output,
            input_tokens=None,
            output_tokens=None,
            request_id="mock-request-0001",
        )
