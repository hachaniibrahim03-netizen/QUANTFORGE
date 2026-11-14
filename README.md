# QUANTFORGE

An auditable, cost-aware multi-agent quantitative research and engineering laboratory.

## Current status

This repository is in its foundation phase. Architecture documents and a mock-only provider execution slice exist. **No external model provider is connected, no API credentials are stored here, and no live trading or market-data execution is enabled.**

## Start here

- [Foundation blueprint](docs/architecture/FOUNDATION_BLUEPRINT.md)
- [Provider registry and evidence register](docs/architecture/PROVIDER_REGISTRY.md)
- [First vertical slice](docs/architecture/FIRST_VERTICAL_SLICE.md)

## Run the current mock-only quality checks

Requires Python 3.10+:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m quantforge.task_runner --output artifacts/provider-smoke.json
```

The mock provider is deterministic and makes **no network request**. Its PASS result proves only that the local provider contract and evidence-writing path execute; it does not prove that an external API works.

GitHub Actions runs the same checks through `.github/workflows/quality-gate.yml` and uploads a smoke evidence artifact.

## Security

- Never commit API keys, tokens, passwords, or personal credentials.
- Use a local environment or an approved secret manager for credentials.
- Do not expose a local model gateway or dashboard publicly without a security review.
- External model calls must record provider/model identity, usage, request IDs, errors, and bounded retry behavior.
- No live broker connection or live trading is part of this foundation slice.


## Optional: one real Gemini smoke request

The live test is manual and sends exactly one short prompt. It is not part of the automatic quality workflow.

1. Create a Gemini API key in Google AI Studio.
2. In this GitHub repository, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Name the secret `GEMINI_API_KEY` and paste the key into GitHub's secret field. Do not paste it into a chat, issue, commit, or source file.
4. Open **Actions → QUANTFORGE Gemini Live Smoke Test → Run workflow**.
5. If the run succeeds, download the `gemini-live-smoke-evidence` artifact. It records the provider/model, request ID when supplied, latency, token usage when returned, and output.

The workflow is manually triggered, has a 3-minute job timeout, sends one request, and retains its evidence artifact for 7 days. Check the current Gemini account quota and data-use terms before running it. A successful smoke test proves only that this one request worked; it does not establish durable free capacity or production reliability.
