# QUANTFORGE — Permanent Recordkeeping & Backup Policy

Last updated: 2026-11-21

## 1. Objective
No essential project knowledge may exist only in a chat transcript, an agent's temporary context, or an uncommitted local file. The repository and local project checkout must preserve the project's decisions, architecture, roadmap, experiments, and handoff state.

## 2. Sources of truth
- Git repository: canonical version history for code, architecture, specifications, policies, decision records, schemas, and non-sensitive project documentation.
- Local checkout: working copy and local operational state; must be synchronized with the canonical repository.
- Data store: actual raw/processed/certified datasets and experiment artifacts, stored separately from source code where size or licensing requires it.
- Artifact manifests: tracked in Git; describe data/artifact IDs, paths, checksums, source, version, license/usage constraints, and certification status without exposing restricted data.
- Chat conversations: collaboration channel, not the only permanent archive.

## 3. What must be recorded
Record every material project event:
- Roadmap changes and phase status.
- Architecture decisions and rejected alternatives.
- Specifications and review verdicts.
- Implementation assignments and agent handoffs.
- Code changes and commit references.
- Test commands, results, failures, and evidence.
- Data source evaluations, licenses, coverage, quality findings, corrections, quarantines, and certificates.
- Strategy source records, formal rule versions, and experiment results.
- Known limitations, unresolved risks, and next actions.

Routine conversation need not be copied verbatim. Preserve decisions, facts, evidence, rationale, and actionable outcomes.

## 4. Required documentation structure
- docs/project/PROJECT_STATE.md — current state and next checkpoint.
- docs/project/ROADMAP.md — phases, gates, and status.
- docs/project/DECISION_LOG.md — append-only material decisions.
- docs/project/AGENT_HANDOFF.md — current instructions and handoff status for Hermes/specialists.
- docs/governance/RECORDKEEPING_POLICY.md — this policy.
- docs/architecture/ — architecture and specifications.
- docs/data/ — data source registry, data contracts, quality rules, and MVP specifications.
- docs/strategies/ — strategy research records and formal rule specifications.
- docs/experiments/ — experiment definitions and summaries; large raw outputs may live outside Git with manifests.
- artifacts/manifests/ — machine-readable manifests and checksums, not necessarily the underlying large data.
- changelog/ or docs/project/CHANGELOG.md — notable project changes.

Adapt to existing repository conventions after inspection; do not create duplicate documentation systems.

## 5. Commit and synchronization rules
- Commit each meaningful, reviewable milestone; do not wait until the end of a long task.
- Before a task, inspect git status and current branch; never overwrite unrelated user changes.
- After a task, run relevant tests, record results, and commit the code plus documentation together where practical.
- Push completed commits to the canonical GitHub repository when connectivity and permissions allow.
- Record commit SHA, branch, test evidence, and remaining work in the handoff.
- Never claim a local change is on GitHub until the push is verified; never claim a GitHub change is on the user's computer until local synchronization is verified.
- Avoid force pushes and destructive history rewrites.
- Use branches and pull requests for high-risk or broad changes where practical.

## 6. Local and remote resilience
Minimum resilience:
1. Local Git working copy at /home/ibra0808/quantforge.
2. Remote GitHub repository as canonical versioned copy.
3. Periodic independent backup of the local project and non-Git data to a separate location/device or encrypted backup service.
4. Verify backups by checking manifests/checksums and performing occasional restore tests.

GitHub is not a substitute for a separate backup. A remote repository and local checkout can both be lost or corrupted through mistaken synchronization, account compromise, or destructive operations.

## 7. Data storage rules
- Raw market data must be immutable and retained with source, acquisition time, instrument/feed identity, timezone, interval, license/terms, and SHA-256 checksum.
- Processed datasets are derived artifacts with transformation version and correction log.
- Certified datasets are immutable versioned snapshots with a quality certificate and permitted-use scope.
- Large market-data files should normally remain in the local data store or an authorized object store, not in ordinary Git history.
- Do not upload market data to a public repository unless redistribution and licensing explicitly permit it.
- Git should track manifests, schemas, certificates, small fixtures, and reproducible instructions.
- Never fabricate missing observations. Quarantine unresolved defects.

## 8. Public repository security
The QUANTFORGE repository was observed as Public on 2026-11-21. Until visibility is intentionally changed:
- Commit only content safe for public disclosure.
- Never commit API keys, tokens, passwords, credentials, personal/private data, private logs, or sensitive account details.
- Use local secret management/environment variables.
- Review generated logs and artifacts before committing.
- Do not commit proprietary or licensed market data unless redistribution is permitted.
- Consider whether the repository should become Private before adding commercially sensitive research or proprietary strategy material. This is a user-owned security decision.

## 9. Agent continuity protocol
Every agent handoff must include:
- Project identity and mission.
- Relevant repository paths and branch/commit.
- Current phase and verified status.
- Decisions and constraints.
- Task scope and prohibited actions.
- Acceptance criteria.
- Evidence required in the final report.
- Next action and unresolved questions.

Agents must read the project state, roadmap, relevant specifications, and handoff before acting. They must update documentation when work changes project state.

## 10. Completion definition
A task is not complete until its deliverables are saved, tests/evidence are recorded, and the handoff/state documents are updated. A verbal claim or chat response alone is not completion.
