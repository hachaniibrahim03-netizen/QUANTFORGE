# First Vertical Slice — Provider Contract and CI Evidence

**Status:** Mock path implemented; Gemini adapter scaffold added; live credentials and live smoke test pending.  
**Version:** 0.2.0

## Objective

Prove the smallest end-to-end software path before enabling multi-agent orchestration:

1. A task runner accepts a bounded prompt.
2. A provider adapter implements a stable interface.
3. A deterministic mock provider supports offline/CI testing.
4. An optional Gemini adapter sends one explicit request through Google's OpenAI-compatible endpoint.
5. The runner writes a JSON evidence artifact with timestamp, provider/model identity, request ID, prompt hash, status, and execution mode.
6. Unit tests validate the provider contract and Gemini response parsing without making a network call.
7. GitHub Actions runs the mock-only checks and uploads the evidence artifact.

## Gemini adapter

- API endpoint: `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`
- Default model: `gemini-3.8-flash` (stable model identifier in the current official model catalogue; verify account access before use).
- Secret environment variable: `GEMINI_API_KEY`
- Optional model override: `GEMINI_MODEL`
- Timeout: 30 seconds by default.
- Retry policy: no automatic retries; rate limits and transient errors must be handled by the orchestrator later.
- The adapter sends one user message, temperature 0, and max_tokens 512.
- The adapter does not log the API key.

Official references:
- https://ai.google.dev/gemini-api/docs/openai
- https://ai.google.dev/gemini-api/docs/models

## Run locally

Mock-only (no network and no credentials):
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m quantforge.task_runner --provider mock --output artifacts/provider-smoke.json
```

Optional real Gemini request (requires a key in the local environment; never commit it):
```bash
export GEMINI_API_KEY="your-key-in-local-shell"
PYTHONPATH=src python -m quantforge.task_runner --provider gemini --output artifacts/gemini-smoke.json
```

## What this proves

A passing mock test proves the provider contract, task runner, and artifact path. A passing mocked Gemini adapter test proves request-response parsing and normalization, not real API connectivity.

Only a successful credentialed Gemini smoke run proves that the configured account, key, model, endpoint, and current quota permit a real request.

## What this does not prove

- No real Gemini API call has yet been made by QUANTFORGE.
- No provider credentials are configured in GitHub.
- No autonomous agent orchestration or persistent background worker exists yet.
- No trading strategy, market data, backtest, or live trading is involved.

## Evidence acceptance

The mock CI workflow must show all tests passing and upload `provider-smoke-evidence`. A real provider smoke test must be run separately with a secret configured in the execution environment, and its evidence must record provider/model identity, request ID, token usage when returned, latency, response status, and artifact hash.
