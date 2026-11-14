# QUANTFORGE Provider Registry

**Status:** Initial research baseline — NOT APPROVED for production use  
**Version:** 0.1.0  
**Verified on:** 2026-11-14  
**Owner:** QUANTFORGE  
**Purpose:** Track model providers, gateways, capabilities, quotas, terms, and evidence before any provider is enabled.

> This file is an evidence register, not a claim that API credentials exist or that any provider has passed a live smoke test. Values marked `UNKNOWN` or `TO_VERIFY` must not be guessed. Provider quotas are account-, project-, model-, region-, and time-dependent.

## 1. Decision summary

1. Evaluate **FreeLLMAPI** as an optional self-hosted aggregation/router candidate, not as QUANTFORGE's trusted control plane.
2. Do not treat the advertised **7.4 billion tokens/month** as guaranteed capacity. It is the project's estimate of the sum of free-tier allowances across multiple providers/endpoints. Each allowance remains subject to the relevant provider's account eligibility, model availability, rate limits, acceptable-use terms, and quota changes.
3. Keep direct provider adapters possible. A gateway must never hide the identity of the upstream provider/model or obscure usage, errors, and quota exhaustion.
4. No API key is stored in this repository. Use environment variables or a secret manager; record only secret references.
5. No provider is marked LIVE until QUANTFORGE has completed a credentialed smoke test and captured request/response metadata, actual usage, latency, error behavior, and a reproducible evidence artifact.

## 2. Provider / gateway register

| ID | Provider / gateway | Role | Public API / integration | Free access evidence | Quotas | Key status | QUANTFORGE status |
|---|---|---|---|---|---|---|---|
| GW-001 | FreeLLMAPI (upstream: tashfeenahmed/freellmapi) | Optional self-hosted aggregator and OpenAI-compatible gateway | Local gateway; documented default API base: `http://localhost:3001/v1` | Upstream README advertises 34 providers, 635 endpoints and roughly 7.4B tokens/month; these are upstream catalog estimates, not a personal entitlement | Per-provider/model limits; exact account-level values must be checked at each provider. Free catalog snapshot is reportedly delayed 30 days versus live feed | NOT CONFIGURED | EVALUATE — NOT APPROVED |
| PR-001 | Google Gemini Developer API | Direct model provider | OpenAI-compatible endpoint: `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | Official docs confirm a Free usage tier for selected models; account eligibility and model access must be verified | Model- and project-specific RPM, input TPM and RPD; active values are shown in AI Studio. Do not copy generic quota numbers into a live account record | NOT CONFIGURED | ADAPTER SCAFFOLDED — LIVE TEST PENDING |
| PR-002 | Groq API | Direct model provider | Official API documentation; exact base URL/model IDs to be recorded during adapter implementation | Official documentation describes rate-limit tiers and per-model limits; free-tier availability/eligibility must be confirmed in the account | RPM, RPD, TPM, TPD and other limits vary by model and organization. Exact limits are shown in the account console; 429 and rate-limit headers must be captured | NOT CONFIGURED | CANDIDATE — VERIFY ACCOUNT |
| PR-003 | Cerebras Inference | Direct model provider | Official API documentation; exact base URL/model IDs to be recorded during adapter implementation | Current public pricing page describes a Developer pay-as-you-go tier with a free $5 starting credit; this is not evidence of a recurring permanent free-token allowance | Current model limits, credit expiry, payment-method requirements, and billing transition must be checked in the account | NOT CONFIGURED | CONDITIONAL CANDIDATE — VERIFY BILLING |

## 3. Evidence and caveats

### GW-001 — FreeLLMAPI

**Primary source:** https://github.com/tashfeenahmed/freellmapi

The upstream README describes:
- An OpenAI-compatible local gateway and a unified API surface.
- Provider-key management, routing, fallback, per-key rate tracking, and a dashboard.
- Encrypted provider keys stored in a local SQLite database (as described by the project).
- A model catalog that is synchronized from a signed feed.
- A free catalog snapshot that may lag the live catalog by 30 days.
- A stated total of roughly 7.4B tokens/month across 34 providers and 635 endpoints.
- A disclaimer that the project is for personal experimentation and learning, not production, and that free tiers are not a stable supported inference substrate.

**Assessment:** Useful as a convenience layer for experimentation, but it introduces another software and credential-handling trust boundary. QUANTFORGE must review the exact source revision, dependencies, install/update scripts, secret-storage implementation, network behavior, telemetry, license, and provider terms before deployment. Do not run an unreviewed install script with elevated privileges. Do not expose its dashboard or API to the public internet without a separate security review.

**Important distinction:** A gateway can aggregate access, but it cannot create extra entitlements. The advertised aggregate is not a guaranteed token balance for one user, one model, one month, or one QUANTFORGE workload.

### PR-001 — Google Gemini Developer API

**Primary sources:**
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://ai.google.dev/gemini-api/docs/pricing

Official documentation says limits are evaluated across requests per minute (RPM), input tokens per minute (TPM), and requests per day (RPD), with values varying by model and project. The active limits should be read from Google AI Studio. The Free tier provides access to selected models and free input/output tokens; data-use terms differ from paid service. Confirm the applicable data handling terms before sending proprietary QUANTFORGE source code or private research. Current official model documentation lists `gemini-3.8-flash` as a stable model identifier, and Google's OpenAI compatibility documentation gives the base endpoint `https://generativelanguage.googleapis.com/v1beta/openai/`. The repository adapter uses the corresponding `/chat/completions` path. Sources: https://ai.google.dev/gemini-api/docs/models and https://ai.google.dev/gemini-api/docs/openai.

### PR-002 — Groq API

**Primary source:** https://console.groq.com/docs/rate-limits

Official documentation defines RPM, RPD, TPM, TPD and audio limits, notes that limits apply at organization level, and says exact current limits are visible in the account console. The docs describe 429 responses and rate-limit headers. Do not assume a published table is the actual entitlement for this account.

### PR-003 — Cerebras Inference

**Primary sources:**
- https://inference-docs.cerebras.ai/support/pricing
- https://www.cerebras.ai/pricing

The currently surfaced public pricing page describes a Developer pay-as-you-go tier with a free $5 credit to start, and an Enterprise tier. An older inference documentation page still describes a $0 Free tier with lower limits, so the official sources are not fully aligned. Treat Cerebras as a conditional candidate only: verify the actual signup offer, credit expiry, billing transition, payment-method requirement, and model quotas in the account before use. Do not count the $5 starter credit as recurring monthly free capacity.

## 4. Required fields for every future provider entry

Every provider record must include:

- `provider_id`, `provider_name`, `provider_type` (direct | gateway | local)
- `api_base_url`, `protocol`, `supported_endpoints`
- `model_ids` (exact upstream IDs; no guessed aliases)
- `capabilities` (reasoning, coding, tool_calling, structured_output, long_context, vision, audio, embeddings)
- `auth_method`, `secret_reference` (never the secret itself)
- `free_tier_type` (permanent | trial | promotional | unknown)
- `free_tier_eligibility`, `payment_method_required`, `region_restrictions`
- `rpm`, `rpd`, `tpm`, `tpd`, `monthly_token_cap`, `credit_amount`, `credit_expiry`
- `quota_scope` (account | organization | project | key | model | IP)
- `usage_reporting`, `rate_limit_headers`, `reset_timezone`
- `data_retention`, `training_use`, `privacy_terms_url`, `acceptable_use_url`
- `license` (for gateways/software), `source_urls`, `verified_at`, `verified_by`
- `evidence_grade`, `status`, `notes`

## 5. Evidence grades and activation gates

| Grade | Meaning | Allowed use |
|---|---|---|
| A | Current official provider documentation or account console, confirmed by a live test | May be considered for controlled experiments |
| B | Current official documentation, but no account-level confirmation or live test | Candidate only |
| C | Maintainer README, community catalog, or secondary source | Discovery only |
| D | Unattributed claim, video, copied table, or unsupported estimate | Do not rely on it |

A provider can be enabled for a QUANTFORGE experiment only after:
1. Terms, region, privacy, and data-use policy are reviewed.
2. The user configures the credential in a local secret store or approved secret manager.
3. A smoke test confirms authentication and the exact model ID.
4. The runner records provider, model, timestamps, latency, request ID, token usage, response status, rate-limit headers, and artifact hash where available.
5. A second request verifies expected error handling and that a 429 does not cause an unbounded retry loop.
6. The provider can be disabled without changing experiment definitions or losing audit records.

## 6. Next implementation sequence

- [ ] Inspect FreeLLMAPI source, release, license, dependency tree, install/update scripts, and credential storage before running it.
- [ ] Confirm the user's eligible provider accounts and their actual quotas in provider dashboards; never request API keys in chat.
- [ ] Select one direct provider for the first controlled smoke test; keep the gateway optional until its security review is complete.
- [ ] Implement a minimal adapter interface and a non-sensitive test prompt.
- [ ] Store a machine-readable provider registry alongside this document only after the fields and validation rules are agreed.
- [ ] Add a usage ledger and bounded retry policy before multi-agent fan-out.

## 7. Current state

**No provider credentials are configured by this document. No API call has been made through a provider. No smoke test has passed. FreeLLMAPI is not installed or running.** This is a research and governance baseline only.


## 8. Desktop installation review — FreeLLMAPI v0.16.28 (Windows)

**User-selected installer:** `FreeLLMAPI-Setup-0.16.28.exe`  
**Official asset URL:** https://github.com/tashfeenahmed/freellmapi/releases/download/v0.16.28/FreeLLMAPI-Setup-0.16.28.exe  
**Review date:** 2026-11-14  
**Status:** User is installing locally; QUANTFORGE integration is NOT YET APPROVED.

### What was verified from project documentation

- The project's README explicitly directs Windows users to download the desktop `.exe` installer from GitHub Releases.
- The desktop application is a local Electron app and includes the router and dashboard.
- The documented desktop data directory on Windows is `%APPDATA%\\FreeLLMAPI\\`; it contains the SQLite database, configuration, and logs.
- The project describes provider keys as encrypted at rest in SQLite and says the desktop app is intended for single-user, local use.
- The desktop README says the router binds to loopback by default; do not enable LAN/public binding for QUANTFORGE.
- The project itself states that it is for personal experimentation and learning, not a stable production inference substrate. Upstream provider terms still apply.

### Security checks still required

- The exact v0.16.28 Windows executable's Authenticode signature and publisher identity have NOT been independently verified here.
- A trustworthy SHA-256 checksum for this exact Windows installer was NOT verified from the release page during this review. Do not compare it with a checksum from a mirror or a different release.
- The repository's current `SECURITY.md` appears stale relative to the v0.16.x release numbering (it still labels 0.6.x as current). This is a documentation-maintenance concern, not proof of malware.
- Before entering any provider credentials, scan the downloaded installer with Microsoft Defender and inspect Windows file Properties → Digital Signatures. If the file has no signature, an invalid signature, or an unexpected publisher, stop and report the exact Windows warning rather than bypassing it.
- Keep the application local-only. Do not expose its dashboard/API to the LAN or internet.
- Do not add valuable/proprietary QUANTFORGE source code or research prompts until the data handling and upstream provider policies are reviewed.

### First-run configuration gate

1. Install only if Windows security checks are satisfactory.
2. Launch the desktop app and confirm the dashboard opens locally.
3. Do not add provider keys yet.
4. Confirm the displayed local API base URL and model catalog version.
5. Confirm the listener is bound to loopback (127.0.0.1), not 0.0.0.0.
6. Record the installed version, local port, and observed security status.
7. Only then run a harmless test prompt with one provider key and verify which upstream provider/model served it.

### Architecture decision

FreeLLMAPI remains an optional local gateway candidate. QUANTFORGE will retain a direct-provider adapter path and will not depend exclusively on FreeLLMAPI. The advertised aggregate token capacity is not a guaranteed entitlement and must not be entered into a QUANTFORGE capacity forecast as committed monthly usage.
