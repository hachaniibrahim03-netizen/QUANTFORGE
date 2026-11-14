# QUANTFORGE Autonomous AI Workforce — Foundation Blueprint

**Status:** Proposed foundation baseline  
**Version:** 0.1.0  
**Repository:** hachaniibrahim03-netizen/QUANTFORGE  
**Default branch:** main

## 1. Mission

Build an auditable, cost-aware, multi-agent research and engineering laboratory for QUANTFORGE. The system coordinates multiple model providers and specialist agents without requiring the owner to shuttle code, prompts, or test outputs between chat interfaces.

AI agents may propose, implement, review, and explain changes. Deterministic software controls execution, permissions, validation gates, and release decisions.

## 2. Non-negotiable principles

1. **No secret in Git.** API keys, OAuth tokens, passwords, and private credentials live only in an approved secret store or local environment variables. Commit placeholders only.
2. **No trust by assertion.** A model saying tests passed is not evidence. The execution service must run commands and capture exit code, logs, artifacts, and commit identity.
3. **Independent approval.** The authoring agent cannot approve its own work. Critical acceptance checks are deterministic and independently specified.
4. **Least privilege.** Agents receive task-scoped permissions. Read-only is the default. Write access is limited to isolated branches/workspaces. Protected branches are not directly writable by agents.
5. **Reproducibility.** Every task records repository commit, model/provider, model identifier, prompt/template version, tool versions, configuration fingerprint, timestamps, and artifact hashes where applicable.
6. **Budget and quota awareness.** Track provider limits, rate limits, estimated/actual usage, failures, and fallback decisions. Advertised aggregate free-token totals are not guaranteed personal capacity.
7. **Bounded autonomy.** Every workflow has time, token, retry, and spend ceilings. Repeated failures stop and escalate rather than loop indefinitely.
8. **No silent scope changes.** Strategy rules, validation criteria, and protected engineering requirements cannot be weakened by an agent to make a run pass.
9. **Human approval for high-impact actions.** No live trading, payments, account purchases, deletion, public releases, or secret/permission changes without explicit owner approval.
10. **Data and model separation.** Market data, experiment records, source documents, model conversations, and execution artifacts have distinct storage and access rules.

## 3. Target architecture

### A. Control plane — Hermes Orchestrator

Responsibilities:
- Maintain the project task queue and state machine.
- Break approved goals into bounded tasks and assign specialist roles.
- Select a provider/model using capability, reliability, latency, quota, and cost metadata.
- Request independent review and reconcile disagreements.
- Enforce retry limits, deadlines, budgets, and approval gates.
- Produce a task report with links to commits and execution artifacts.

Hermes is a coordinator, not an authority that can override deterministic release gates.

### B. Model gateway — Provider Adapter Layer

A single internal interface supports multiple providers. Each adapter exposes:
- provider and model identifiers;
- supported capabilities (coding, reasoning, long context, vision, tool calling, structured output);
- authentication via secret references;
- rate-limit/quota metadata where available;
- timeout, retry, and error normalization;
- usage metadata when returned by the provider.

A community gateway such as the FreeLLMAPI project may be evaluated as an optional adapter or routing layer after its exact repository, implementation, license, security posture, provider terms, and quota claims are reviewed. It is not yet an approved dependency. Aggregate advertised free-token capacity is not a guaranteed account balance.

### C. Specialist agents

Initial logical roles (one or more models may serve each role):
- **Architect:** architecture and interface design.
- **Engineer:** implementation in isolated workspaces/branches.
- **QA Engineer:** independent test design and execution review.
- **Adversarial Reviewer:** attempts to falsify assumptions and find defects.
- **Data Engineer:** data ingestion, schemas, quality, and lineage.
- **Quant Researcher:** source-grounded strategy research and formal specifications.
- **Risk Analyst:** risk constraints and prop-firm rule modeling.
- **Auditor:** evidence completeness, reproducibility, and gate compliance.

Agent roles are independent of specific model brands. Model selection is dynamic and measured.

### D. Work execution plane

- GitHub is the source-control and review surface.
- A task runner executes tests in isolated, disposable environments.
- Each task gets a clean workspace and a dedicated branch.
- CI runs deterministic checks and publishes logs/artifacts.
- Agents cannot directly modify the protected default branch.
- Pull requests are the integration boundary; checks must pass before merge.

Google Colab may be used for interactive experiments and temporary compute, but it is not treated as an always-on production worker. Scheduled or continuous workloads require a runner with explicit availability and quota guarantees.

### E. State and artifact storage

Recommended logical stores:
- **PostgreSQL:** task state, agent assignments, provider registry, experiments, approvals, audit events, and metadata.
- **Parquet/Object Storage:** large market datasets and generated research artifacts.
- **Git:** source code, versioned specifications, prompts/templates, and configuration schemas.
- **Artifact store:** raw logs, test reports, JSON outputs, plots, and checksums.
- **Vector store (optional later):** semantic retrieval over approved documents; never the system of record for experiments or financial results.

Start with the smallest operational footprint. Do not deploy every database or service before a demonstrated need.

### F. Observability and owner dashboard

The dashboard should show:
- active tasks and current stage;
- assigned agent and selected model/provider;
- queue, retries, elapsed time, and resource usage;
- provider quota/rate-limit status;
- task diffs and pull requests;
- test outcomes (PASS, FAIL, ERROR, SKIPPED);
- links to raw logs and immutable artifacts;
- approval requests and blocked tasks.

## 4. Task lifecycle

REQUESTED → PLANNED → ASSIGNED → WORKING → REVIEW → EXECUTION → VALIDATION → APPROVAL_REQUIRED (if applicable) → COMPLETED

Failure path: WORKING/REVIEW/EXECUTION/VALIDATION → BLOCKED or RETRY_QUEUED.

Rules:
- Retries are bounded and each attempt is separately recorded.
- A retry includes a diagnosis and a changed hypothesis or patch; blind repetition is prohibited.
- Any critical test result other than PASS blocks acceptance.
- SKIPPED tests are visible and never counted as passing.
- Conflicting agent opinions trigger a documented adjudication task, not silent majority voting.
- A completed task links to its commit/PR and execution evidence.

## 5. Initial implementation sequence

### Foundation 0 — Access and safety
- Confirm GitHub integration and repository permissions.
- Protect main; require pull requests and passing checks.
- Define secret-management method; do not commit credentials.
- Establish task and artifact naming conventions.

### Foundation 1 — Minimal working orchestrator
- Define provider/agent/task interfaces.
- Create provider registry with capability and quota metadata.
- Implement task queue, bounded retries, and audit events.
- Add one provider adapter first; prove end-to-end operation before adding many providers.

### Foundation 2 — Execution and evidence
- Run a harmless smoke task in an isolated runner.
- Capture raw stdout/stderr, exit code, commit SHA, timestamps, and artifact hashes.
- Verify the system can report a real failure as a failure.
- Add independent reviewer and QA roles.

### Foundation 3 — Multi-provider routing
- Add providers incrementally after terms, reliability, security, and limits are checked.
- Benchmark model quality on a fixed task suite.
- Route by measured capability and availability, not marketing claims or model count.
- Add fallback behavior without hiding provider errors.

### Foundation 4 — QUANTFORGE engineering workflow
- Import and inspect the current engine and its specifications.
- Reproduce existing engine-integrity failures.
- Repair and validate the synthetic engine test suite.
- Keep strategy benchmarking blocked until engine acceptance criteria are met.

## 6. Initial acceptance criteria

The first operational milestone is not “100 models connected.” It is one complete, reproducible, auditable task executed without manual copy/paste:

1. Hermes creates a bounded task.
2. A selected model receives the task through the gateway.
3. The agent creates a change on an isolated branch.
4. An independent reviewer inspects the change.
5. The runner executes prescribed checks.
6. Raw logs, exit code, commit SHA, and report are stored.
7. The task state reflects the actual result.
8. A failure remains a failure; it cannot be relabeled PASS by an agent.

Only after this vertical slice works should provider count and agent count expand.

## 7. Risks and controls

| Risk | Control |
|---|---|
| Free quotas change or disappear | Provider registry, quota checks where supported, graceful fallback, budget caps |
| Leaked API keys | Secret store, secret scanning, key rotation, no secrets in prompts or Git |
| Prompt injection in retrieved content | Treat external content as untrusted data; tool permissions and output validation |
| Agent loops or runaway usage | Retry ceilings, timeouts, token/spend budgets, circuit breakers |
| Conflicting or low-quality model output | Independent review, fixed benchmarks, deterministic checks |
| Malicious or unsafe dependency | Pin versions, review license and source, vulnerability scanning, sandbox execution |
| False green reports | Runner-generated evidence and independent validation |
| Accidental destructive Git operation | Protected default branch, scoped tokens, PR-only integration |

## 8. Explicitly out of scope for the first milestone

- Connecting to a live broker or placing trades.
- Autonomous purchases or payments.
- Unrestricted shell access or production credentials for agents.
- Claiming a guaranteed seven-billion-token allowance.
- Connecting 100+ models before measuring the first provider integrations.
- Moving to market-strategy benchmarking before the synthetic engine validation gate is passed.

## 9. Decision record

This blueprint establishes the target architecture and safety constraints only. It does not claim that any orchestrator, model gateway, database, runner, or dashboard has already been deployed. Each component becomes implemented only after its code is committed and its acceptance test has run successfully.
