# QUANTFORGE — Decision Log

Append-only record of material decisions. New decisions are added at the top with date, status, rationale, and consequences. Superseded decisions remain for traceability.

## DEC-2026-11-21-003 — Free-first Forex + CFD data pilot
Status: Accepted as the current MVP direction; source availability and licensing remain to be verified.

Decision:
- Begin with Forex major pairs and CFD symbols XAUUSD, US100, US500.
- Use 1m as the base interval and derive 5m after validation.
- Defer Daily and Tick until justified by strategy requirements.
- Do not pay for data subscriptions at the beginning.
- Compare multiple candidate sources where genuinely independent and semantically compatible.
- Quarantine rejected or unresolved data and retain raw originals.

Rationale: Prove the integrity pipeline and research workflow without upfront data subscription costs.

Consequences:
- Feed identity and broker/provider semantics must be stored explicitly.
- A Forex/CFD price is source-specific, not a universal consolidated market price.
- Dukascopy is a candidate source; MT5 demo broker feeds are candidate comparison sources. Neither is certified yet.
- Verify symbol mapping, available history, bid/ask, timezone, sessions, volume semantics, independence, and licensing before acceptance.

## DEC-2026-11-21-002 — Multi-source comparison and quarantine
Status: Accepted.

Decision:
- Prefer multiple independent sources with comparison.
- Preserve original raw datasets.
- Rejected or uncertain datasets go to quarantine; do not permanently delete them.
- AI models may investigate anomalies and propose hypotheses, but deterministic checks and independent evidence decide certification.

Rationale: Improve error detection while preserving provenance and the ability to reproduce prior experiments.

## DEC-2026-11-21-001 — QMIR Phase 1 architecture approval
Status: Approved with minor corrections after read-only review.

Decision:
- QMIR is a bounded model registry, task router, fallback manager, and performance ledger around the existing Hermes/QUANTFORGE environment.
- Keep one model for simple work, two for review, and at most three for high-risk tasks where justified.
- No broad framework additions without demonstrated need.
- Keep sensitive operations permission-gated; no live trading.
- Integrate into the existing dashboard rather than creating a competing dashboard.

Minor corrections to enforce during implementation:
1. Record each fallback attempt immediately.
2. Warn on duplicate attempt_id collisions.

Implementation completion remains unverified until code and test evidence are reviewed.

## Historical note
Earlier planning considered Futures ES/NQ/GC as the initial data pilot. The user's later explicit decision on 2026-11-21 supersedes that pilot choice: start with free-first Forex and CFD instead. Preserve Futures as a later possible expansion, not the current MVP.
