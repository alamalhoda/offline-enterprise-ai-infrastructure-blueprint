# SINA Architecture Critique — Validation & Remediation Plan (v1.1)

**Scope:** Spot-check P1–P15 against active SSOT docs; annotate accuracy; produce implementation-ready remediation. **No source-doc (SSOT) edits in this phase.** This plan file is a workspace planning artifact (`.kilo/plans/`), not an SSOT document.  
**Active docs reviewed:** `README.md`, `PROJECT_RULES.md`/`AGENTS.md`, `ADR-SSOT-001.md`, `Enterprise AI Infrastructure_ Document Intelligence & RAG Ecosystem.md` (Arch), `End-to-End Data Flow.md`, `Data-Lake-Discussion-Summary.md`, `مستند بهبودیافته_ ابزارهای RAG و AI Agent.md` (Tools), `SINA_Roadmap_v1.5.md`, `SINA_SprintPlan_v1.5.md`, `SINA_RiskQA_v1.5.md`, `SINA_LLMOps_v1.5.md`.  
**Not reviewed (insufficient):** `موتور قطعه‌بندی هوشمند متون سازمانی فارسی.md` (SSOT for splitter implementation), PDFs/PPTX/PNG/MP4, `Archive/` except inventory signals, binding decisions only in diagrams/slides. **If slides/PDFs carry binding decisions, revise this plan.**

## 1. Validation summary (P1–P15)

| # | Sev. | Verdict | Key evidence (active docs; *approximate refs — grep-verify before edits*) | Annotation / correction |
|---|---|---|---|---|
| P1 | Critical | **Mostly confirmed** | Hybrid/options contradict across Arch §F/§S, Roadmap/Sprint (Whoosh+Qdrant), Tools (Qdrant sparse+BM25). Embedding differs (e5-large/ParsBERT vs e5-base ONNX INT8 vs BGE-M3; DataFlow hardcodes 768). Orchestration/API/HW differ across Arch/Roadmap/Sprint. Only `ADR-SSOT-001.md` exists. | Arch is partly options/trade-off, but execution docs conflict — freeze gap remains. DataFlow dims must be parameterized. |
| P2 | Critical | **Confirmed, timing nuanced** | RBAC/ACL/Keycloak Phase 3; QG1.5 requires 100% audit/access control; ACL pre-filter S15–16; JWT S21–22. Identity differs (local tokens/LDAP/Keycloak). At-rest/Vault not frozen. Arch states immutable logs in PG (not WORM) and full trace logging. LLMOps validates SHA-256 against value “declared in source”. Threat model/prompt injection not found. | Audit/ACL/JWT tasks appear earlier than Phase 3, but **authN-on-all-endpoints, threat model, IdP decision, encryption, coherent identity model not frozen before ingestion**. |
| P3 | High | **Confirmed** | `content_hash UNIQUE` + `versions JSONB`; dedup returns existing link; cross-doc dedup by reference; ACL in vector payload/pre-filter; `ingest_id=hash+timestamp`; eventual indexes, ACL revocation lag undefined. | Cross-tenant existence leak plausible; shared canonical chunk ACL scope undefined. |
| P4 | High | **Mostly confirmed** | Raw immutable vs Sprint 90-day MinIO auto-expire; **Arch §L states “delete after 5 years”** (user-confirmed) — conflicts. RPO table (PG 1h, MinIO 24h, Qdrant 48h) inconsistent with schedule (daily PG+MinIO, weekly Qdrant). `chunk_text`/`norm_text` in PG; DataFlow lacks Lake steps. | Rebuild-time math is **estimate, not fact** — capacity spike required. RTO<24h for full rebuild unrealistic at scale unless proven. |
| P5 | High | **Confirmed (directional)** | >8 tok/s accepted; Gate 1 uses P95 E2E <=30s, TTFT vs full undefined. Query rewriting adds LLM call; conversation memory schema not found. **Arch §J states “Threaded workers (e.g., 4 per core)”** (user-confirmed) vs Sprint Thread=Physical Cores/HT off. 10–20 users on one LLM: queue/timeout/degradation undefined. | Capacity/budget model missing. |
| P6 | High | **Confirmed** | 10–20 users/thousands of files, QG1.3>=1000. Many services/frameworks; LangChain wraps llama.cpp despite OpenAI-compatible server. Phase 4/scale adds Iceberg/Trino/Keycloak/Temporal/K8s. “Horizontal scale without architecture change” vs Whoosh single-writer tension. | Team “Backend-Centric…” in Roadmap §2/R-004 (user-confirmed). |
| P7 | High | **Confirmed** | S1 defines only 3 interfaces; missing ports (index, object store, queue, reranker, policy, audit, model registry). Haystack DAG owns flow; policy/audit risk landing in nodes. Mermaid CDC/label conflation. Tools example inherits LangChain `TextSplitter` (hexagonal violation). | Observability/governance cross-cutting. |
| P8 | High | **Confirmed** | Multi-store pipeline without saga/outbox; Celery+Redis durability/DLQ semantics concerns; tombstone via background job; no persistent `ingestion_jobs` state machine found. | |
| P9 | High | **Confirmed** | Index version lacks normalizer/chunker/analyzer fingerprint. PG alias flip cannot atomically cover PG+Qdrant+BM25. A/B/shadow/old-index retention costly on CPU-only. | |
| P10 | High | **Confirmed (critical)** | “Reverse text/chunk order” (Arch) incorrect for Unicode logical-order models. DataLake maps `U+06CC→U+06A9, U+064A→U+06A9` (Yeh→Kaf, wrong direction). ZWNJ contradicts (DataLake remove/space vs DataFlow/RiskQA TC-02 preserve). NFKC vs NFC; chunk unit/size/overlap inconsistent. Reranker MS MARCO-minilm — Persian unproven. Tools misattributes ICU plugin to Haystack (OpenSearch in Arch). | Single versioned Normalization Contract required (ingest+query). |
| P11 | High | **Confirmed** | `Score < 0.65` after RRF invalid (RRF~1/(k+rank), k=60, not cosine). Golden Set “from Sprint 1” but no S1–2 task. QG0 lacks Persian quality. Accuracy>=75%/<=30s promised before LLM enters. Accuracy measurement undefined. Llama-3/Mistral Persian quality = **evaluation spike**, not assumed. | Calibrate “no answer”/quality on Golden Set per pipeline fingerprint; include unanswerables. |
| P12 | Medium | **Confirmed** | `entities` lacks ACL; source ACL mapping undefined. ERP extraction/CDC/freshness/re-embed undefined. Partitioning differs across docs. | |
| P13 | Medium | **Confirmed** | Single-node SPOFs; **QG2.2 “20 users, Uptime >=99%”** (user-confirmed). 3-2-1 off-site undefined for air-gapped. Recovery test month 14 while data collected earlier. | |
| P14 | Medium | **Confirmed** | CPU-irrelevant/unsourced benchmarks. SINA docs missing/mismatched headers/versions. **README date 1404/08/16 = 2025-11-07, conflicts with 2026 dates — should be 1405** (user-confirmed). **PROJECT_RULES.md is a 1-paragraph stub pointing to AGENTS.md (not byte-identical)**; README→PROJECT_RULES→AGENTS creates circular/confusing rule-source reference — fix README to point to `AGENTS.md` (or clarify single rule SSOT). Arch duplicates DataLake detail. R-001..R-016 owned by Backend Lead who approves most gates. | Doc governance, but affects decision reliability. |
| P15 | Low | **Method concern confirmed** | **KS-test in LLMOps §6.2, Arch §K, RiskQA R-013** (user-confirmed) — univariate, weak for 768/1024-d embeddings without projection. Drift>10% auto re-embed can trigger multi-day CPU job. Heavy observability stack on prod node. | Prefer Golden-Set regression as primary trigger; drift diagnostic only. |

## 2. Decision Freeze (restructured for scope/risk)

**Constraint:** 14 ADRs + threat model + eval harness + capacity spikes do **not** fit a 4-week Phase 0 with current Gate 0 (5 infra-only criteria). **Extend Phase 0 to 6–8 weeks** (explicitly) and update Gate 0 to include freeze/evidence outcomes.

### 2.1 Critical-path ADRs (must decide before dependent work)
| ADR | Decision | Blocks | Direction to validate | Notes/risks |
|---|---|---|---|---|
| ADR-002 Retrieval Engine | One engine; eliminate Whoosh | S13+, schema, ops | **Spike-required:** compare Persian keyword Recall (with app-side normalization/tokenization/stemming per ADR-011) on Qdrant sparse+dense vs OpenSearch+ICU. Operational simplicity alone is insufficient. | Qdrant has no Persian analyzer — tokenization/stemming/ZWNJ must be app-side and versioned with ADR-011. |
| ADR-003 Embedding Contract | Model+format+dims+quantization+license+path | ingest/query/rebuild | Golden Set on target CPU; parameterize dims; remove hardcoded 768. | |
| ADR-004 LLM/Reranker Contract | LLM GGUF serving; reranker with Persian evidence | M2.3+, quality | Prefer llama.cpp OpenAI-compatible server behind port; validate Persian generation/rerank. | Avoid English-only reranker assumption. |
| ADR-006 Identity/AuthZ/Audit | IdP, authN, PDP/PEP, ACL scope, revocation SLA, audit | first exposed endpoint/data | AuthN on all endpoints from first deploy; **in-process PDP behind `AccessPolicy` port** (RBAC+ACL); PEP at retrieval + authoritative top-K recheck. | **Do not add OPA initially** (conflicts with ADR-015 simplification); add only if externalized policy becomes necessary. |
| ADR-007 Blob/Document/Chunk | Content-addressed blob vs logical document vs chunk; ACL scope | dedup, security | No cross-tenant existence leak; shared chunks only within identical ACL scope or policy-checked indirection. | |
| ADR-011 Persian Normalization Contract | Versioned ingest+query contract | all NLP/indexing/eval | Remove reversal; fix Unicode mappings; resolve ZWNJ; choose Unicode form; define chunk unit/size/overlap; test vectors TC-01..TC-10. | Highest correctness risk. |
| ADR-012 Quality Gates & Measurement | TTFT/full P95, Golden Set, no-answer calibration, accuracy protocol | gates/eval | No fixed RRF/cosine 0.65; calibrate per pipeline fingerprint; include unanswerables. | |
| ADR-013 Capacity/Deployment Baseline | HW profile, CPU allocation, concurrency, degradation | Phase 0–2 | One baseline; measure prefill/decode, embedding throughput, rebuild time. | |

### 2.2 Secondary ADRs (decide by named sprint/milestone)
| ADR | Decide by | Direction | Dependency/risk |
|---|---|---|---|
| ADR-005 Orchestration & Queue | Before S3 implementation | Thin pipeline + PG job/outbox acceptable at this scale; if PG `SKIP LOCKED` used, require **lease/heartbeat, stale-job recovery, visibility timeout**. **Query path must never pass through ingestion/job queue.** | Reliability over simplicity. |
| ADR-008 Ingestion State Machine | Before S3–S4 | Deterministic `ingest_id` (no timestamp), persistent states, compensating actions for derived stores. | With ADR-005. |
| ADR-009 Lake/Index SoT & Backup | Before production data (Gate 1 latest) | Raw immutable/never auto-expire by default; legal deletion explicit; RPO/RTO aligned with schedule; derivatives rebuildable with measured rebuild. | |
| ADR-010 Index Snapshot & Fingerprint | Before re-embed/migration features | Fingerprint includes embedder/normalizer/chunker/analyzer/schema/ACL-model version; blue/green pointer; coordinated vector+BM25 cutover. | |
| ADR-014 Observability & Log Safety | Before production data | No sensitive content in logs/traces by default; retention/TTL; audit semantics separated from generic PG claims. | With ADR-006. |
| ADR-015 Scope/Strangler | Phase 0 (decision) | Minimal Persian RAG walking skeleton to Gate 2; defer Lakehouse/Entity/Iceberg/Trino/Keycloak/Temporal/K8s behind explicit gates. | Governs all others. |

**Governance note:** New ADRs expand scope beyond `ADR-SSOT-001`. In implementation, update `AGENTS.md` (SSOT for rules) ADR section and keep `README.md` references consistent.

## 3. Implementation-ready backlog (owners/effort/deps/exit criteria)

*Effort: S=<=2d, M=3–5d, L=1–2w, XL=>2w (spike-heavy). Owners are roles; assign names in execution. Map to critique priorities 1–7.*

| ID | Priority map | Item | Owner | Effort | Depends on | Exit criteria | SSOT targets |
|---|---|---|---|---|---|---|---|
| B1 | 1,7 | Extend Phase 0 to 6–8 weeks; update Gate 0 to include decision freeze + eval/capacity evidence | Tech Lead + PO | S | — | Roadmap/Sprint show revised Phase 0 duration and Gate 0 criteria | `SINA_Roadmap_v1.5.md`, `SINA_SprintPlan_v1.5.md` |
| B2 | 1 | Decision register (Open/Decided/Deferred), owners, ADR links | Tech Lead | S | B1 | Register published/linked from README; every critical-path decision tracked | `README.md` (+ register location per SSOT) |
| B3 | 1 | ADR-002/003/004/006/007/011/012/013 drafts + reviews | Tech Lead (decider), domain owners | L | B2 | ADRs accepted or explicitly deferred with date/risk | new `ADR-*.md`, `AGENTS.md` ADR scope |
| B4 | 7,1 | Persian Golden Set + eval harness spec (incl. unanswerables, citations, TC-01..TC-10, accuracy protocol) | QA/NLP owner + Tech Lead | M | B3 (011/012 inputs) | Versioned dataset/protocol; runnable spec; Gate 0/P0 usable | new eval artifact (path TBD per SSOT), `SINA_RiskQA_v1.5.md` refs |
| B5 | 4,1 | Capacity spike: prefill/decode, embedding throughput, rebuild estimate, 10–20 user concurrency, TTFT/full P95 | Backend/ML owner | M | B3 (002-004,013), target HW confirmed | Measured numbers recorded; informs ADR-013 and gate thresholds | spike report, `SINA_LLMOps_v1.5.md`/Roadmap refs |
| B6 | 2 | Threat model (light STRIDE) for air-gapped RAG | Security owner + Tech Lead | M | B3 (006) | Risks/mitigations mapped to backlog; prompt-injection/log/model-provenance covered | `SINA_RiskQA_v1.5.md`, ADR-006/014 |
| B7 | 7 | Fix Persian normalization contract in docs/code guidance (no reversal, Unicode/ZWNJ, unit/overlap) | NLP owner | M | B3/B4 (011) | All active docs/examples aligned to one versioned contract; TC-02 consistent | Arch, DataFlow, DataLake, Tools, Splitter SSOT, RiskQA |
| B8 | 2,3 | Identity/AuthZ/data-model baseline (authN first, in-process PDP, Blob/Document/Chunk, deterministic ingest_id) | Backend Lead + Security | L | B3 (006-008), B6 | Design approved in ADRs; implementation tasks decomposed; no cross-tenant leak path | Arch, DataFlow, Roadmap/Sprint, RiskQA |
| B9 | 3 | Ingestion reliability: job state machine/outbox/leases; Raw never auto-expire; RPO/RTO/schedule coherent; rebuild measured | Backend Lead | L | B3/B5 (005,008,009,010) | State model + backup/restore runbook; derivative rebuild declared/measured | Arch, DataLake, SprintPlan, LLMOps |
| B10 | 4 | Capacity controls: TTFT/full definitions, LLM gateway queue/timeout/circuit breaker, ingestion/query isolation | Backend Lead | M | B5, B8 | Gate thresholds measurable; degradation mode defined | Roadmap, SprintPlan, Arch, LLMOps |
| B11 | 5 | Scope/ports simplification: minimal stack, full port catalog, ADR-015 applied; remove/defer Whoosh/LangChain where justified | Tech Lead + Arch owner | M | B3 (002,005,015) | Approved target architecture; deferred items gated | Arch, Tools, Roadmap/Sprint |
| B12 | 6 | Pipeline fingerprint + coordinated snapshot cutover (vector+BM25) | Backend/ML owner | M | B3 (003,009,010), B9 | Fingerprint stored; cutover/rollback runbook tested in non-prod | Arch, LLMOps, SprintPlan |
| B13 | 2,7 | Quality gate repair: remove invalid RRF 0.65; security expectations realistic/earlier; evidence protocol | PO + Tech Lead + QA | S | B4, B6, B8 | Gates measurable and aligned to phase capabilities | Roadmap, SprintPlan, RiskQA |
| B14 | 7 | Doc governance: fix README rule-source/date, verify AGENTS/PROJECT_RULES references, header/version lint checklist, grep-verify all cited lines before edits | Tech Lead | S | — | No circular rule refs; date/header issues listed/fixed in implementation pass | `README.md`, `AGENTS.md`, `PROJECT_RULES.md`, all active headers |
| B15 | 3,4 | Recovery drills from Phase 1; governance independence for gate/security approval | Ops/Security + PO | M | B9, B6 | Drill schedule/evidence; named independent approver | `SINA_LLMOps_v1.5.md`, `SINA_RiskQA_v1.5.md`, Roadmap |

## 4. Doc-change map (SSOT-compliant, implementation mode)

Before editing: follow `AGENTS.md` workflow (change in artifacts/project files, pull/reconcile remote, user approval, then commit/push). Bump Version/Updated headers on every edited file. Grep-verify all line references.

| SSOT target | Changes |
|---|---|
| `README.md` | Fix rule source to `AGENTS.md` (resolve circular PROJECT_RULES ref); fix date to 1405/… (2026) as confirmed; add decision register; study-guide warnings; keep Data Lake as summary+link only. |
| `ADR-SSOT-001.md` + new `ADR-002..015` | Freeze decisions; expand ADR governance scope via `AGENTS.md` update. |
| `AGENTS.md` / `PROJECT_RULES.md` | `AGENTS.md` remains rules SSOT; clarify ADR scope/process; ensure `PROJECT_RULES.md` stub remains consistent (no drift). |
| `Enterprise AI Infrastructure_ Document Intelligence & RAG Ecosystem.md` | Resolve options→decisions; remove reverse-text; fix CDC/alias atomicity claims; align HW; add port catalog/cross-cutting; reference ADRs/DataLake SSOT. |
| `End-to-End Data Flow.md` | Lake touchpoints, ACL/revocation, DLQ, deterministic ingest_id, TTFT/memory scope note, no hardcoded dims. |
| `Data-Lake-Discussion-Summary.md` | Fix Unicode mapping/ZWNJ per ADR-011; Raw immutability; partition contract; entity ACL/freshness; encryption pointer. |
| `SINA_Roadmap_v1.5.md` / `SINA_SprintPlan_v1.5.md` | Phase 0 duration/Gate 0; security earlier; Golden Set/TTFT/capacity; fix RRF threshold; align RPO/backup/retention. |
| `SINA_RiskQA_v1.5.md` | R-001..R-016 mitigations/gates; independent approver; TC/ZWNJ alignment; unanswerables/accuracy protocol. |
| `SINA_LLMOps_v1.5.md` | Artifact provenance; Persian reranker evidence; consistent RPO/RTO/schedule; vector+BM25+snapshot migration. |
| `مستند بهبودیافته_ ابزارهای RAG و AI Agent.md` | Remove/label CPU-irrelevant benchmarks; fix ICU attribution; adapter-only hexagonal example; align to ADRs. |
| `Archive/README.md` | Update only if files archived/moved. |

## 5. Open questions (confirm before implementation)
1. Binding decisions only in **PDF/PPTX/PNG/MP4**?
2. Actual **target hardware** (cores/RAM/disk) and corpus growth for Phase 0/1?
3. **Air-gapped off-site backup** method feasible?
4. Required **ACL revocation SLA**?
5. **Conversation memory** in scope for query rewriting/state?
6. Named **independent approver** for security/gate evidence (besides Backend Lead)?

## 6. Recommendation
Adopt **ADR-015** (strangler/minimal scope): extend Phase 0 (6–8 weeks), freeze critical-path ADRs (002–004/006–007/011–013), build a thin Persian RAG walking skeleton with authN/policy hooks + Golden Set + capacity evidence, then expand only behind gates. Defer OPA/Entity/Lakehouse/Trino/Iceberg/Keycloak/Temporal/K8s until evidence requires them.

## 7. Implementation handoff checklist
- [ ] Confirm open questions (esp. hardware, off-site backup, ACL SLA, independent approver).
- [ ] Execute B1–B2 (Phase 0/Gate 0 + decision register).
- [ ] Run spikes/eval/threat model (B4–B6) and accept critical-path ADRs (B3).
- [ ] Apply SSOT doc changes (B7–B15) with Version/Updated headers and grep-verified references.
- [ ] Cross-reference audit before any archive/move; update `AGENTS.md` ADR scope.
- [ ] Re-validate P1–P15; close/carry residual risks in `SINA_RiskQA_v1.5.md`. No commit/push without explicit user approval per `AGENTS.md`.