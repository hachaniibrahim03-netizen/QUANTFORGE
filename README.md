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
