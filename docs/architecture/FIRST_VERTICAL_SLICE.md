# First Vertical Slice — Provider Contract and CI Evidence

**Status:** Mock adapter implemented; Gemini adapter scaffolded; FreeLLMAPI loopback adapter implemented; live gateway smoke test pending.  
**Version:** 0.3.0

## Objective

Prove the smallest end-to-end software path before enabling multi-agent orchestration:

1. A task runner accepts a bounded prompt.
2. Provider adapters implement a stable interface.
3. A deterministic mock provider supports offline/CI testing.
4. Optional Gemini and FreeLLMAPI adapters normalize OpenAI-compatible chat responses.
5. The runner writes a JSON evidence artifact with timestamp, provider/model identity, request ID, prompt hash, status, latency, usage, and execution mode.
6. Unit tests validate response normalization without making network calls.
7. GitHub Actions runs mock-only checks; it cannot access a developer's local gateway.

## FreeLLMAPI local adapter

- Base URL default: `http://127.0.0.1:31415/v1`
- Chat endpoint: `/chat/completions`
- Secret environment variable: `FREELLMAPI_API_KEY`
- Exact model ID environment variable: `FREELLMAPI_MODEL`
- Optional base URL override: `FREELLMAPI_BASE_URL`
- Timeout: 45 seconds by default.
- Only HTTP loopback hosts are accepted: `127.0.0.1`, `localhost`, and `::1`.
- One request per invocation; no automatic retry.
- The adapter records returned token usage and request ID when supplied; it never writes the key to the evidence artifact.

The default port is the documented FreeLLMAPI port. If the desktop app selected another port, set the actual port in `FREELLMAPI_BASE_URL`. The model value must be the exact API model ID exposed by the gateway, not an assumed friendly display name.

## Gemini adapter

- API endpoint: `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`
- Model is explicitly configurable using `GEMINI_MODEL`.
- Secret environment variable: `GEMINI_API_KEY`
- Timeout: 30 seconds by default.
- No automatic retries.

## Run locally

Offline tests and mock path (no network and no credentials):

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m quantforge.task_runner --provider mock --output artifacts/provider-smoke.json
```

FreeLLMAPI live smoke (Windows PowerShell; run on the same computer as the gateway):

```powershell
$env:FREELLMAPI_BASE_URL = "http://127.0.0.1:31415/v1"
$env:FREELLMAPI_API_KEY = "YOUR_NEW_LOCAL_GATEWAY_KEY"
$env:FREELLMAPI_MODEL = "EXACT_MODEL_ID_FROM_GATEWAY"
$env:PYTHONPATH = "src"
python -m quantforge.task_runner --provider freellmapi --prompt "Reply with exactly: QUANTFORGE_GATEWAY_OK" --output artifacts/freellmapi-smoke.json
```

Never put the key in Git, source files, issues, or chat. If the app uses another local port, update the base URL accordingly.

## Evidence interpretation

- Passing unit tests prove request construction and response parsing under mocked HTTP; they do not prove a live connection.
- A successful credentialed smoke run proves one request worked through the selected gateway route and model at that time.
- It does not prove that every model in the gateway catalog is available, that fallback works, or that monthly token quotas are guaranteed.
- The mock CI job does not connect to a user's computer or local gateway.

## Not yet implemented

- Multi-agent orchestration, agent task queues, and persistent workers.
- Provider/model capability scoring and budget-aware routing.
- Independent research review and deterministic acceptance gates.
- Market data, strategy backtesting, prop-firm simulation, or broker connectivity.
