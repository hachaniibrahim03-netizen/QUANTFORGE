# QUANTFORGE Roadmap

Last updated: 2026-11-21

This roadmap is cumulative. Completed work requires evidence; a task being assigned does not mean it is complete.

## Phase 0 — Project foundation
Goal: establish a reproducible repository, provider contract, offline test path, and security boundaries.

Status: Foundation exists; see README and architecture documents. Do not infer live provider connectivity from configuration alone.

## Phase 1 — QMIR (Model Intelligence & Routing)
Goal: route bounded tasks to suitable models, track evidence and performance, and provide controlled fallback.

Specification: QMIR Architecture Phase 1 Spec 003 was reviewed as APPROVE WITH MINOR CORRECTIONS.

Acceptance reminders:
- Log each fallback attempt immediately.
- Warn on duplicate attempt_id collisions.
- Keep sensitive operations permission-gated.
- Use offline deterministic tests before any external model calls.
- Integrate into the existing dashboard; do not create a competing dashboard.
- Background service, if used, must remain loopback-only and must not expose the gateway/dashboard to LAN or public internet.
- Do not store API secrets in Git.
- Implementation is pending evidence-based review.

Gate: implementation report, code diff, automated test output, service status, dashboard evidence, and security review.

## Phase 2 — Data Integrity & Certification MVP 001
Goal: build a free-first data pipeline for Forex and CFD with raw preservation, source comparison, quarantine, deterministic validation, and certified dataset versions.

Initial universe:
- Forex: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD.
- CFD: XAUUSD, US100, US500.
- 1m raw/base interval; 5m derived from validated 1m.
- Daily and Tick deferred.

Candidate source plan:
- Dukascopy as candidate source.
- MT5 demo broker feeds as candidate comparison source.
- Verify exact symbols, history coverage, timezone/session semantics, bid/ask availability, volume meaning, source independence, and licensing before certification.
- No paid subscriptions at the start.

Implementation sequence:
1. Inspect existing repository and avoid duplicate components.
2. Source capability discovery using small samples only.
3. Download a pilot sample for EURUSD, XAUUSD, US100, US500 where available.
4. Preserve immutable raw files and checksums.
5. Normalize metadata/time without altering source values.
6. Run structural, temporal, continuity, and cross-source checks.
7. Quarantine unexplained conflicts; never invent prices.
8. Derive 5m with documented boundaries and validation.
9. Issue fitness-for-purpose certificates.
10. Add certified-data access gate to backtesting.
11. Integrate monitoring into the existing dashboard.

Gate: deliberately corrupted fixtures must be detected; rejected data cannot reach backtesting; repeated runs must be reproducible.

## Phase 3 — Strategy research library
Goal: curate at least 50 credible, non-duplicative strategies from primary or high-quality sources; larger target may follow.

Rules:
- Research discovery first; do not mix coding, optimization, or prop-firm constraints into discovery.
- Record source, attribution confidence, evidence grade, original rule wording, missing details, and extraction status.
- Do not invent rules or results.
- Separate genuinely distinct strategies from parameter variations and overlapping labels.
- Convert approved research into explicit, testable rules only after source review.

## Phase 4 — Backtesting and research evaluation
Goal: test formally specified strategies across compatible certified datasets and instruments.

Every experiment must record:
- Strategy ID and immutable rules/version.
- Dataset ID/version and quality certificate.
- Source and acquisition metadata.
- Timeframe, timezone, session, and contract/feed definition.
- Engine and code version.
- Costs, spread, slippage, and execution assumptions.
- Train/validation/holdout boundaries where applicable.
- Metrics, equity curve, drawdown, trade log, and reproducibility metadata.

No strategy may be called robust based only on an in-sample result.

## Phase 5 — Prop-firm risk simulation
Goal: apply separate, explicit rule sets for Futures Prop Firms and CFD Prop Firms after baseline strategy behavior is understood.

Do not mix firm rules into strategy discovery or silently alter baseline results. Preserve baseline and each risk-overlay experiment separately.

## Phase 6 — Professional research dashboard
Goal: extend the existing dashboard with strategy library, experiment detail, equity/performance curves, drawdown, trade logs, dataset certificates, model routing telemetry, and project status.

Do not build a second dashboard or expose local services beyond loopback.

## Operating rule
Prefer short execution/review cycles with tangible artifacts. Do not create repeated specification-only loops. Every phase ends with a documented acceptance decision and evidence links.
