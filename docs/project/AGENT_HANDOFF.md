# QUANTFORGE — Agent Handoff

Last updated: 2026-11-21

## Read first
1. README.md
2. docs/project/PROJECT_STATE.md
3. docs/project/ROADMAP.md
4. docs/project/DECISION_LOG.md
5. docs/governance/RECORDKEEPING_POLICY.md
6. The relevant architecture or data specification for the assigned task.

## Roles
- ChatGPT: project director, architecture and research quality authority, reviewer.
- Hermes: local execution lead; owns local inspection, code changes, tests, service operations, local data storage, and Git synchronization.
- Specialist models: bounded contributors. Their work requires evidence and review.
- User: final authority for payments, credentials, security-sensitive changes, and live trading.

## Current handoff state
- QMIR Phase 1 Spec 003: approved with minor corrections.
- QMIR implementation: previously assigned to Hermes; awaiting implementation evidence/report in the current project workflow. Do not assume complete.
- Data Integrity MVP 001: scope selected, not yet implemented.
- Current data pilot: free-first Forex + CFD; 1m base, 5m derived; Daily/Tick deferred.
- Candidate data sources: Dukascopy and MT5 demo broker feeds; not yet verified or certified.

## Rules for every Hermes task
1. Inspect current branch, git status, existing files, and recent commits first.
2. Read the relevant project docs before changing anything.
3. Do not overwrite or discard unrelated work.
4. Keep changes bounded; avoid unnecessary frameworks and duplicate systems.
5. Never put secrets in Git or logs.
6. Do not upload licensed/restricted market data to the public repository.
7. Run tests and capture exact commands/results.
8. Update docs/project/PROJECT_STATE.md, ROADMAP.md, DECISION_LOG.md when state or decisions materially change.
9. Update this handoff with commit SHA, branch, tests, failures, and next step.
10. Commit and push only after checking the diff and verifying no sensitive files are included.

## Required final report
- Summary of changes.
- Files created/modified.
- Commit SHA and push status.
- Tests run and exact outcomes.
- Local service/dashboard status where relevant.
- Data artifacts/manifests and checksums where relevant.
- Security/permission issues.
- Remaining work and next recommended action.

## Important limitation
ChatGPT cannot directly inspect or operate the user's local WSL filesystem or Hermes process in this workflow. Hermes must perform local synchronization and report verifiable results. GitHub connector operations can write supported documentation to the remote repository, but this does not automatically update the local checkout.
