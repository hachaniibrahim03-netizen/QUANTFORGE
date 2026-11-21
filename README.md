# QUANTFORGE

An auditable, cost-aware multi-agent quantitative research and engineering laboratory.

## Current status

The foundation now includes offline mock testing, a Gemini adapter scaffold, and a loopback-only FreeLLMAPI adapter. **No live QUANTFORGE-to-FreeLLMAPI request has yet been verified.** No API credentials are stored in this repository. No live trading or market-data execution is enabled.

## Project continuity (read before contributing)

- [Current project state](docs/project/PROJECT_STATE.md)
- [Roadmap](docs/project/ROADMAP.md)
- [Decision log](docs/project/DECISION_LOG.md)
- [Agent handoff](docs/project/AGENT_HANDOFF.md)
- [Permanent recordkeeping and backup policy](docs/governance/RECORDKEEPING_POLICY.md)
- [Data Integrity MVP 001](docs/data/DATA_INTEGRITY_MVP_001.md)

All agents must read the project state, roadmap, decision log, and relevant handoff/specification before work. Material decisions, code changes, tests, and experiment outcomes must be recorded in the repository. Never commit secrets or restricted market data.

## Start here

- [Foundation blueprint](docs/architecture/FOUNDATION_BLUEPRINT.md)
- [Provider registry and evidence register](docs/architecture/PROVIDER_REGISTRY.md)
- [First vertical slice](docs/architecture/FIRST_VERTICAL_SLICE.md)

## Run offline quality checks

Requires Python 3.10+:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m quantforge.task_runner --provider mock --output artifacts/provider-smoke.json
```

The mock provider is deterministic and makes no network request. Its PASS result proves only that the local provider contract and evidence-writing path execute.

## Optional: test the local FreeLLMAPI gateway

Keep FreeLLMAPI running on the same Windows computer as the QUANTFORGE runner. The adapter accepts only loopback HTTP addresses; it deliberately rejects LAN/public bind addresses.

PowerShell example (use the actual port shown by FreeLLMAPI if it differs):

```powershell
$env:FREELLMAPI_BASE_URL = "http://127.0.0.1:31415/v1"
$env:FREELLMAPI_API_KEY = "YOUR_NEW_LOCAL_GATEWAY_KEY"
$env:FREELLMAPI_MODEL = "EXACT_MODEL_ID_FROM_FREELLMAPI"
$env:PYTHONPATH = "src"
python -m quantforge.task_runner --provider freellmapi --prompt "Reply with exactly: QUANTFORGE_GATEWAY_OK" --output artifacts/freellmapi-smoke.json
```

Use a newly rotated gateway key stored only in your local shell or a local secret manager. Do not paste it into ChatGPT, commit it, or put it in a repository file. Do not assume a model's display label is its API model ID: copy the exact ID shown by the gateway's model/API catalogue. If the gateway port differs, change only the port in the base URL.

The output artifact records the selected provider/model, request ID when available, latency, token usage when returned, prompt hash, and response. It does not record the API key. A successful result verifies one request through the selected route only; it does not prove every listed model is usable or that monthly quotas are guaranteed.

## Optional: one real Gemini smoke request

The Gemini adapter is separate from FreeLLMAPI. It reads `GEMINI_API_KEY` and optional `GEMINI_MODEL` from the local environment. Run only if you intentionally want a direct Google API route:

```bash
PYTHONPATH=src python -m quantforge.task_runner --provider gemini --output artifacts/gemini-smoke.json
```

Check current account quota and data-use terms before making external requests.

## Security and scope

- Never commit API keys, tokens, passwords, or personal credentials.
- Do not expose the local model gateway or dashboard to the LAN or public internet.
- External calls are one-request-per-run with no automatic retry.
- GitHub Actions quality checks remain mock-only; they cannot reach your computer's localhost gateway.
- No broker connection, live trading, or strategy backtesting is enabled in this foundation slice.
