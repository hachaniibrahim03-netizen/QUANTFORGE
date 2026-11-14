# First Vertical Slice — Provider Contract and CI Evidence

**Status:** Implemented as a mock-only scaffold; awaiting GitHub Actions execution evidence.  
**Version:** 0.1.0

## Objective

Prove the smallest end-to-end software path before connecting external model accounts:

1. A task runner accepts a bounded prompt.
2. A provider adapter implements a stable interface.
3. A deterministic mock provider returns a normalized response.
4. The runner writes a JSON evidence artifact with timestamp, provider/model identity, request ID, prompt hash, status, and execution mode.
5. Unit tests validate the contract and failure behavior.
6. GitHub Actions runs the tests and uploads the evidence artifact.

## What this proves

If the workflow passes, it proves that the repository's Python package, provider interface, task runner, tests, and evidence artifact path work together in GitHub-hosted CI.

## What this does not prove

- No external model API is called.
- No provider credentials are configured or validated.
- No agent orchestration, autonomous task delegation, or background worker exists yet.
- No trading strategy, market data, backtest, or live trading is involved.
- A workflow file being committed is not proof that the workflow has run or passed.

## Run locally

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m quantforge.task_runner --output artifacts/provider-smoke.json
```

## Evidence acceptance

The GitHub Actions run must show:
- all unit tests passing;
- smoke runner exit code 0;
- uploaded `provider-smoke-evidence` artifact;
- JSON status `PASS` and execution mode `mock_only_no_external_api_call`.

Only after this slice passes should a direct provider adapter be added. Credentials must be supplied through GitHub Actions secrets or a local environment secret store, never committed to Git.
