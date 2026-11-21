# QUANTFORGE — Project State

Last updated: 2026-11-21
Status: Active research and engineering project

## Mission
Build an auditable, reproducible, cost-aware quantitative research laboratory for discovering, formalizing, testing, and evaluating trading strategies. Research integrity and data quality take priority over strategy count or attractive backtest results.

## Governance and roles
- ChatGPT: project director and architecture/research quality authority; maintains roadmap, standards, acceptance gates, and reviews submitted execution evidence.
- Hermes: local execution lead; inspects and modifies the local project, runs tests, maintains local records, and reports evidence.
- Specialist models: delegated for bounded research, data audits, coding, or independent reviews. Model agreement is not proof.
- The user retains authority over financial commitments, credentials, security-sensitive changes, and live-trading decisions.

ChatGPT does not have direct access to the user's local WSL filesystem or Hermes runtime. GitHub connector access is available for repository documentation and supported GitHub operations. Local synchronization and execution must be performed by Hermes.

## Current repository
- GitHub: https://github.com/hachaniibrahim03-netizen/QUANTFORGE
- Default branch: main
- Visibility observed on 2026-11-21: Public
- Local project path reported by user: /home/ibra0808/quantforge
- Security rule: never commit credentials, API keys, passwords, private personal data, or licensed market data unless redistribution is explicitly permitted.

## Current engineering state
- Existing foundation includes offline mock testing, Gemini adapter scaffold, and a loopback-only FreeLLMAPI adapter.
- Repository README states that no live QUANTFORGE-to-FreeLLMAPI request has yet been verified.
- QMIR Architecture Phase 1 Specification 003 received an APPROVE WITH MINOR CORRECTIONS review. Recommendations: record fallback attempts immediately as they occur, and warn on duplicate attempt_id collisions.
- QMIR implementation was requested from Hermes; implementation status remains unverified until Hermes supplies a report and test evidence.
- No live trading is enabled.
- No strategy backtesting/data certification pipeline is considered production-ready until implementation and acceptance tests prove it.

## Current data direction — latest user decision
The initial data lab has changed from Futures to a free-first Forex + CFD pilot:
- Forex: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD.
- CFD: XAUUSD, US100, US500.
- Primary interval: 1-minute.
- 5-minute bars are derived from validated 1-minute data.
- Daily and Tick are deferred until strategy requirements justify them.
- No paid data subscriptions at the beginning.
- Multi-source comparison is desired; rejected/uncertain data must be quarantined and raw originals retained.
- Dukascopy is a candidate first source; MT5 demo broker feeds are candidate comparison sources. Availability, history depth, source independence, instrument definitions, and usage terms remain to be verified. These are not yet certified sources.

## Non-negotiable research principles
1. Preserve immutable raw data and provenance.
2. Correct only with deterministic rules or independent evidence; otherwise quarantine.
3. Never fabricate missing prices or intrabar event order.
4. Dataset certification is fitness-for-purpose, not a universal quality badge.
5. Every backtest records dataset version, certificate, strategy/rules version, engine version, and execution assumptions.
6. Prevent look-ahead bias, survivorship bias, and silent data revisions.
7. Separate broker/feed-specific Forex and CFD prices; do not assume a universal consolidated price.
8. No live broker connection or live trading without a separate explicit user decision.

## Next immediate checkpoint
1. Obtain and review Hermes' QMIR implementation report; verify code, tests, background service, and dashboard integration before accepting.
2. Preserve the latest decisions in this repository and synchronize them to the local WSL checkout.
3. Start Data Integrity MVP 001 only after the QMIR checkpoint is reviewed, without reopening already-approved architecture unnecessarily.
