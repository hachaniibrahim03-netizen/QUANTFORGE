"""Small, auditable provider contract. No provider SDK dependency is required."""
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class ModelResponse:
    provider: str
    model: str
    output_text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    request_id: str | None = None


class ProviderError(RuntimeError):
    """Normalized provider failure; callers must not blindly retry it."""


@runtime_checkable
class ModelProvider(Protocol):
    provider_name: str
    model_name: str

    def generate(self, prompt: str) -> ModelResponse:
        """Execute one bounded prompt and return normalized metadata."""
