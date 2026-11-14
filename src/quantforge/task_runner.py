"""Minimal task runner with bounded input and auditable JSON output."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from quantforge.providers import MockProvider

MAX_PROMPT_CHARS = 8_000


def run_smoke(prompt: str) -> dict:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError(f"prompt exceeds {MAX_PROMPT_CHARS} characters")

    provider = MockProvider()
    response = provider.generate(prompt)
    payload = {
        "schema_version": "1.0",
        "status": "PASS",
        "task_type": "provider_contract_smoke_test",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "provider": response.provider,
        "model": response.model,
        "request_id": response.request_id,
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "output_text": response.output_text,
        "execution_mode": "mock_only_no_external_api_call",
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run QUANTFORGE provider contract smoke test")
    parser.add_argument("--prompt", default="QUANTFORGE provider contract check")
    parser.add_argument("--output", default="artifacts/provider-smoke.json")
    args = parser.parse_args(argv)
    try:
        result = run_smoke(args.prompt)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if k != "output_text"}, indent=2))
        print(f"ARTIFACT={output_path.as_posix()}")
        return 0
    except Exception as exc:  # runner boundary: report failure, never fabricate PASS
        print(json.dumps({"status": "ERROR", "error_type": type(exc).__name__, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
