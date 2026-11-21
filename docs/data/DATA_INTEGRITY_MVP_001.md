# QUANTFORGE Data Integrity — MVP 001

Status: Scope accepted; implementation and source certification pending.
Decision date: 2026-11-21

## 1. Objective
Build a free-first, reproducible data acquisition, validation, comparison, quarantine, and certification pipeline. The pipeline must preserve raw originals and only release certified datasets for compatible research/backtests.

## 2. Initial universe
### Forex major pairs
- EURUSD
- GBPUSD
- USDJPY
- AUDUSD
- USDCAD
- USDCHF
- NZDUSD

### CFD instruments
- XAUUSD
- US100
- US500

Symbol aliases must be mapped to provider-specific instrument identifiers. Do not assume that USA500 equals every broker's US500, or that USATECH is identical in contract specification to every US100 feed. Record exact provider symbol and instrument metadata.

## 3. Timeframes
- 1m is the base interval.
- 5m is derived from validated 1m bars using explicit timezone, session, and boundary rules.
- Daily is deferred until needed.
- Tick is deferred until a strategy's execution or intrabar-ordering requirements justify it.

A derived 5m bar must retain lineage to its source 1m bars and transformation version. Do not aggregate blindly across session boundaries, missing intervals, or invalid source bars.

## 4. Cost policy
- No paid subscriptions during the initial proof-of-concept.
- Prefer free downloadable history and demo-account access where lawful and technically reliable.
- Free availability does not guarantee full history, stable API access, redistribution rights, or commercial-use rights.
- Do not bypass provider limits, authentication, or terms.
- Before any paid upgrade, document the exact missing capability and why free alternatives fail.

## 5. Candidate sources — unverified
### Candidate A: Dukascopy
Investigate historical Forex, metal, and index CFD coverage; 1m availability; Bid/Ask semantics; symbol mapping; timezone/session conventions; history depth; download reliability; and usage/redistribution terms.

### Candidate B: MT5 demo broker feed
Investigate availability through a demo account and official terminal/API; exact broker and server identity; symbol specifications; history limits; OHLC price basis; Bid/Ask and tick-volume semantics; timezone/session behavior; and terms.

Do not label the sources independent until ownership, liquidity/feed lineage, and data characteristics have been assessed. Two different interfaces may redistribute the same upstream feed.

## 6. Data model and provenance
Every dataset/partition should record:
- provider and exact source/server/feed identity;
- exact provider symbol and normalized instrument mapping;
- asset class and instrument specification;
- price basis (Bid, Ask, Mid, Last, or provider-defined);
- interval and candle timestamp convention;
- timezone and session calendar;
- volume type (real volume, tick volume, unavailable);
- collection timestamp and retrieval method;
- source file checksum (SHA-256);
- raw/processed/certified state;
- transformation and validation versions;
- usage/license notes and redistribution restrictions.

## 7. Immutable layers
1. Raw: byte-preserved source download plus metadata and checksum.
2. Processed: normalized/derived copy with transformation log; never overwrite raw.
3. Quarantine: unresolved defects or conflicts retained with reason and investigation history.
4. Certified: immutable versioned snapshot with certificate and permitted-use scope.

Large raw/market-data files normally stay in the authorized local data store or approved storage, not in this public Git repository. Git tracks schemas, manifests, checksums, certificates, small synthetic fixtures, and reproducible procedures.

## 8. Validation
- Structural: OHLC consistency, duplicates, invalid values, ordering.
- Temporal: UTC normalization, daylight-saving transitions, session boundaries, weekends, holidays, provider timestamps.
- Continuity: expected versus unexpected gaps; distinguish no-trade intervals from missing data.
- Cross-source: compare only semantically compatible instruments, price bases, intervals, and timestamps.
- Market semantics: bid/ask spread, tick size, decimal precision, volume meaning, symbol specification.
- Derived bars: validate 5m OHLCV against the correct 1m constituents.
- Execution suitability: record whether the data can support close-based, OHLC, bid/ask-aware, or intrabar-sensitive testing.

Do not apply a universal exact-match rule to different broker feeds. Define tolerances by instrument, price basis, interval, and intended use. Unexplained material discrepancies are quarantined.

## 9. AI assistance
Models may identify anomalies, investigate source documentation, explain likely causes, and propose corrections. They must not invent missing values or autonomously rewrite source prices. Final certification is deterministic and evidence-based; model consensus is not proof.

## 10. Certification states
- ACCEPTED: passed all required checks for a defined use.
- CONDITIONAL: usable only under explicit constraints (e.g. close-based research only; no trustworthy historical spread).
- REJECTED: material unexplained defects or insufficient provenance.

Certification is fitness-for-purpose, not a universal endorsement. A dataset can be acceptable for one strategy and unsuitable for another.

## 11. Acceptance tests
- Detect injected duplicate bars.
- Detect impossible OHLC relationships.
- Detect out-of-order timestamps and timezone errors.
- Identify missing intervals while accounting for market closures and provider no-trade conventions.
- Detect cross-source conflicts after semantic alignment.
- Verify 5m aggregation from valid 1m constituents.
- Prove raw data is unchanged after processing.
- Prove quarantine cannot be read by the backtesting interface.
- Reproduce the same certificate from the same data and validator version.
- Record complete dataset lineage in every backtest experiment.

## 12. MVP delivery boundary
First run source discovery and small sample downloads for EURUSD, XAUUSD, US100, and US500 where available. Do not download all instruments and multiple years until source semantics, history coverage, terms, and pipeline tests are understood. Expand to the remaining Forex pairs only after the pilot passes.

## 13. Not included
- Paid data subscriptions.
- Live market streaming.
- Broker order execution.
- Tick-by-tick history as a requirement.
- Daily timeframe as a requirement.
- Automated AI price correction.
- Claims of institutional-grade execution realism from 1m OHLC alone.
