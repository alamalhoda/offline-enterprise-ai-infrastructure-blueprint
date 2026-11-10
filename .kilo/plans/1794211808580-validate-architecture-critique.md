# SINA Architecture Critique — Validation & Remediation Plan (v1.2)

**Scope:** Spot-check P1–P15 against active SSOT docs; annotate accuracy; produce implementation-ready remediation. **No source-doc (SSOT) edits in this phase.** This plan file is a workspace planning artifact (`.kilo/plans/`), not an SSOT document.  
**Active docs reviewed:** `README.md`, `PROJECT_RULES.md`/`AGENTS.md`, `ADR-SSOT-001.md`, `Enterprise AI Infrastructure_ Document Intelligence & RAG Ecosystem.md` (Arch), `End-to-End Data Flow.md`, `Data-Lake-Discussion-Summary.md`, `مستند بهبودیافته_ ابزارهای RAG و AI Agent.md` (Tools), `SINA_Roadmap_v1.5.md`, `SINA_SprintPlan_v1.5.md`, `SINA_RiskQA_v1.5.md`, `SINA_LLMOps_v1.5.md`.  
**Not reviewed (insufficient):** `موتور قطعه‌بندی هوشمند متون سازمانی فارسی.md` (SSOT for splitter implementation), PDFs/PPTX/PNG/MP4, `Archive/` except inventory signals, binding decisions only in diagrams/slides. **If slides/PDFs carry binding decisions, revise this plan.**

## 1. Validation summary (P1–P15)

| # | Sev. | Verdict | Key evidence (active docs; *approx refs — grep-verify before edits*) | Annotation / correction |
|---|---|---|---|---|
| P1 | Critical | **Mostly confirmed** | Hybrid/options contradict across Arch §F/§S, Roadmap/Sprint (Whoosh+Qdrant), Tools (Qdrant sparse+BM25). Embedding differs (e5-large/ParsBERT vs e5-base ONNX INT8 vs BGE-M3; DataFlow hardcodes 768). Orchestration/API/HW differ. Only `ADR-SSOT-001.md` exists. | Arch partly options/trade-off; execution docs conflict — freeze gap remains. Parameterize dims. |
| P2 | Critical | **Confirmed, timing nuanced** | RBAC/ACL/Keycloak Phase 3; QG1.5 100% audit/access; ACL pre-filter S15–16; JWT S21–22. Identity differs (local tokens/LDAP/Keycloak). At-rest/Vault not frozen. Immutable logs claimed in PG (not WORM); full trace logging. LLMOps SHA-256 compared to “declared” source value. Threat model/prompt injection not found. | Audit/ACL/JWT appear earlier, but **authN-on-all-endpoints, threat model, IdP decision, encryption, coherent identity model not frozen before ingestion**. |
| P3 | High | **Confirmed** | `content_hash UNIQUE` + `versions JSONB`; dedup returns existing link; cross-doc dedup by reference; ACL in vector payload/pre-filter; `ingest_id=hash+timestamp`; eventual indexes, ACL revocation lag undefined. | Cross-tenant existence leak plausible; shared canonical chunk ACL scope undefined. |
| P4 | High | **Mostly confirmed** | Raw immutable vs Sprint 90-day MinIO auto-expire; Arch §L “delete after 5 years” (verified from active docs) conflicts. RPO table inconsistent with schedule. `chunk_text`/`norm_text` in PG; DataFlow lacks Lake steps. | Rebuild-time math is **estimate, not fact** — capacity spike required. RTO<24h for full rebuild unrealistic at scale unless proven. |
| P5 | High | **Confirmed (directional)** | >8 tok/s accepted; Gate 1 P95 E2E <=30s, TTFT/full undefined. Query rewriting adds LLM call; conversation memory schema not found. Arch §J “Threaded workers (e.g., 4 per core)” vs Sprint physical cores/HT off (verified from active docs). 10–20 users on one LLM: queue/timeout/degradation undefined. | Capacity/budget model missing. |
| P6 | High | **Confirmed** | 10–20 users/thousands of files, QG1.3>=1000. Many services/frameworks; LangChain wraps llama.cpp despite OpenAI-compatible server. Phase 4 adds Iceberg/Trino/Keycloak/Temporal/K8s. “Horizontal scale without architecture change” vs Whoosh single-writer tension. | Team “Backend-Centric…” in Roadmap §2/R-004 (verified from active docs). |
| P7 | High | **Confirmed** | S1 defines 3 interfaces; missing ports (index, object store, queue, reranker, policy, audit, model registry). Haystack DAG owns flow. Mermaid CDC/label conflation. Tools inherits LangChain `TextSplitter` (hexagonal violation). | Observability/governance cross-cutting. |
| P8 | High | **Confirmed** | Multi-store pipeline without saga/outbox; Celery+Redis durability/DLQ semantics concerns; tombstone via background job; no persistent `ingestion_jobs` state machine found. | |
| P9 | High | **Confirmed** | Index version lacks normalizer/chunker/analyzer fingerprint. PG alias flip cannot atomically cover PG+Qdrant+BM25. A/B/shadow/old-index retention costly on CPU-only. | |
| P10 | High | **Confirmed (critical)** | “Reverse text/chunk order” incorrect for Unicode logical-order models. DataLake maps `U+06CC→U+06A9, U+064A→U+06A9` wrong. ZWNJ contradicts (remove/space vs preserve). NFKC vs NFC; chunk unit/size/overlap inconsistent. Reranker MS MARCO-minilm Persian unproven. Tools misattributes ICU plugin to Haystack. | Single versioned Normalization Contract required. |
| P11 | High | **Confirmed** | `Score < 0.65` after RRF invalid. Golden Set “from Sprint 1” but no S1–2 task. QG0 lacks Persian quality. Accuracy promised before LLM enters. Accuracy measurement undefined. Llama-3/Mistral Persian quality = **evaluation spike**. | Calibrate on Golden Set per pipeline fingerprint; include unanswerables. |
| P12 | Medium | **Confirmed** | `entities` lacks ACL; source ACL mapping undefined. ERP extraction/CDC/freshness/re-embed undefined. Partitioning differs. | |
| P13 | Medium | **Confirmed** | Single-node SPOFs; QG2.2 “20 users, Uptime >=99%” (verified from active docs). 3-2-1 off-site undefined for air-gapped. Recovery test month 14 while data collected earlier. | |
| P14 | Medium | **Confirmed** | CPU-irrelevant/unsourced benchmarks. SINA docs missing/mismatched headers/versions. README date 1404/08/16=2025-11-07 conflicts with 2026 — should be 1405 (verified from active docs). `PROJECT_RULES.md` is a stub to `AGENTS.md` (not byte-identical); README→PROJECT_RULES→AGENTS circular/confusing — fix README to point to `AGENTS.md`. Arch duplicates DataLake detail. R-001..R-016 owned by Backend Lead who approves most gates. | |
| P15 | Low | **Method concern confirmed** | KS-test in LLMOps §6.2, Arch §K, RiskQA R-013 (verified from active docs) — univariate, weak for high-d embeddings without projection. Drift>10% auto re-embed can trigger multi-day CPU job. Heavy observability on prod node. | Golden-Set regression primary; drift diagnostic. |

## 2. Decision Freeze (restructured)

**Constraint:** 14 ADRs + threat model + eval harness + capacity spikes do not fit 4-week Phase 0 / current Gate 0. **Extend Phase 0 to 6–8 weeks** and update Gate 0 criteria (see B1). Re-plan Roadmap/Sprint and 18-month impact; get stakeholder approval.

### 2.1 Gate 0 (revised, proposed)
Gate 0 passes only when all are true:
- **G0-D:** Critical-path ADRs accepted with evidence (002,003,004,006,007,011,012,013) or explicitly deferred with dated risk acceptance.
- **G0-E:** Golden Set v1 (>=100 questions, includes unanswerables/citations/TC-01..TC-10 cases) versioned with measurement protocol.
- **G0-Q:** Baseline Recall@5 (and keyword/Persian cases) measured on **target hardware** against Golden Set v1.
- **G0-C:** Prefill/decode, embedding throughput, TTFT/full P95, and rebuild estimate recorded on target hardware (10–20 user concurrency model).
- **G0-S:** Threat model reviewed; authN-on-all-endpoints + `AccessPolicy` port design accepted for first deploy.
- **G0-I:** Existing infra criteria retained where still relevant (Docker/Gitea/PyPI mirror/CI/model vault basics), reconciled with revised Phase 0 schedule.

### 2.2 Critical-path ADRs (B3a draft → evidence → B3b accept)
| ADR | Decision | Blocks | Direction to validate | Notes/risks |
|---|---|---|---|---|
| ADR-002 Retrieval Engine | One engine; eliminate Whoosh | S13+, schema, ops | **Spike:** Persian keyword Recall (app-side normalization/tokenization/stemming/ZWNJ per ADR-011, versioned) on Qdrant sparse+dense vs OpenSearch+ICU. | Qdrant no Persian analyzer — app-side handling required. |
| ADR-003 Embedding Contract | Model+format+dims+quantization+license+path | ingest/query/rebuild | Golden Set on target CPU; parameterize dims; remove hardcoded 768. | |
| ADR-004 LLM/Reranker Contract | LLM GGUF serving; reranker with Persian evidence | M2.3+, quality | llama.cpp OpenAI-compatible server behind port; validate Persian generation/rerank. | |
| ADR-006 Identity/AuthZ/Audit | IdP, authN, PDP/PEP, ACL scope, revocation SLA, audit | first exposed endpoint/data | AuthN all endpoints from first deploy; **in-process PDP behind `AccessPolicy` port**; PEP at retrieval + authoritative top-K recheck. | No OPA initially. |
| ADR-007 Blob/Document/Chunk | Content-addressed blob vs logical document vs chunk; ACL scope | dedup, security | No cross-tenant existence leak; shared chunks only within identical ACL scope or policy-checked indirection. | |
| ADR-011 Persian Normalization Contract | Versioned ingest+query contract | NLP/indexing/eval | Remove reversal; fix Unicode mappings; resolve ZWNJ; choose Unicode form; define chunk unit/size/overlap; test vectors. | ZWNJ direction to spike: keep canonical text with ZWNJ; BM25/analyzer path must match both forms as needed. |
| ADR-012 Quality Gates & Measurement | TTFT/full P95, Golden Set, no-answer calibration, accuracy protocol | gates/eval | No fixed RRF/cosine 0.65; calibrate per pipeline fingerprint; include unanswerables. | |
| ADR-013 Capacity/Deployment Baseline | HW profile, CPU allocation, concurrency, degradation | Phase 0–2 | One baseline from B0 hardware; prefill/decode, throughput, rebuild, TTFT/full P95. | |

### 2.3 Secondary ADRs (decide by named sprint/milestone)
| ADR | Decide by | Direction | Dependency/risk |
|---|---|---|---|
| ADR-005 Orchestration & Queue | Before S3 | Thin pipeline + PG job/outbox acceptable; PG `SKIP LOCKED` requires **lease/heartbeat, stale-job recovery, visibility timeout**. **Query path never uses ingestion/job queue.** | Reliability. |
| ADR-008 Ingestion State Machine | Before S3–S4 | Deterministic `ingest_id` (no timestamp), persistent states, compensating actions for derived stores. | With ADR-005. |
| ADR-009 Lake/Index SoT & Backup | Before production data (Gate 1 latest) | Raw immutable/never auto-expire default; legal deletion explicit; RPO/RTO aligned with schedule; derivatives rebuildable/measured. | |
| ADR-010 Index Snapshot & Fingerprint | Before re-embed/migration features | Fingerprint includes embedder/normalizer/chunker/analyzer/schema/ACL-model; blue/green pointer; coordinated vector+BM25 cutover. | |
| ADR-014 Observability & Log Safety | Before production data | No sensitive content in logs/traces by default; retention/TTL; audit semantics separated. | With ADR-006. |
| ADR-015 Scope/Strangler | Phase 0 (decision) | Minimal Persian RAG walking skeleton to Gate 2; defer Lakehouse/Entity/Iceberg/Trino/Keycloak/Temporal/K8s behind gates. | Governs scope. |

**Governance:** New ADRs expand scope beyond `ADR-SSOT-001`. In implementation, update `AGENTS.md` ADR section; keep `README.md` references consistent.

## 3. Implementation-ready backlog

*Effort: S=<=2d, M=3–5d, L=1–2w, XL=>2w. Owners are roles; **assign names before execution**. `NLP owner`/`Security owner`/`ML owner` are not established in RiskQA (R-004: no ML expertise; QA embedded); plan external review or named assignees for threat model, Golden Set, and Persian eval.* **All SSOT edits: follow `AGENTS.md` (artifacts/project change → pull/reconcile → explicit user approval → commit/push), bump Version/Updated headers, grep-verify references, B14 prerequisite.**

| ID | Pri. | Item | Owner | Effort | Depends on | Exit criteria | SSOT targets |
|---|---|---|---|---|---|---|---|
| B0 | 1,4 | **Blocker:** confirm target hardware (cores/RAM/disk), corpus/growth, deployment constraints | PO + Tech Lead | S | — | Hardware baseline recorded; B5/B13 thresholds can be defined | decision register / roadmap input |
| B1 | 1,7 | Extend Phase 0 to 6–8 weeks; define Gate 0 (G0-D/E/Q/C/S/I); re-plan Roadmap/Sprint and 18-month impact; state S1–S2 infra tasks parallel/adjusted; **stakeholder approval for gate/date moves** | Tech Lead + PO | M | B0 (baseline context) | Revised schedule + Gate 0 published; stakeholder approval recorded | `SINA_Roadmap_v1.5.md`, `SINA_SprintPlan_v1.5.md` |
| B2 | 1 | Decision register (Open/Decided/Deferred), owners, ADR links, blockers | Tech Lead | S | B1 | Linked from README; critical-path decisions tracked | `README.md` (+ register location) |
| B3a | 1 | Draft critical-path ADRs (002–004,006,007,011,012,013): context/options/decision criteria/spike plan | Tech Lead + domain owners | M | B2 | Drafts reviewable; each has explicit accept criteria | new `ADR-*.md`, `AGENTS.md` ADR scope |
| B4 | 7,1 | Golden Set v1 + eval harness spec/protocol (>=100 Q, unanswerables, citations, TC-01..TC-10, accuracy method) | QA/NLP owner + Tech Lead (or external reviewer) | M | B3a (011/012 criteria) | Versioned dataset/protocol; runnable spec; supports G0-E/Q | eval artifact (TBD), `SINA_RiskQA_v1.5.md` |
| B5 | 4,1 | Capacity spike on **target hardware**: prefill/decode, embedding throughput, rebuild estimate, 10–20 user concurrency, TTFT/full P95 | Backend/ML owner | M | B0, B3a (002–004,013), B4 (test queries) | Measured numbers recorded; supports G0-C and B3b | spike report, `SINA_LLMOps_v1.5.md`/Roadmap |
| B3b | 1 | Accept critical-path ADRs with B4/B5/B6 evidence (or defer with dated risk acceptance) | Tech Lead (decider) + PO/Security as needed | S | B3a, B4, B5, B6 | ADRs Accepted/Deferred; G0-D satisfied | `ADR-*.md`, decision register |
| B6 | 2 | Threat model (light STRIDE): authN/Z, ingestion/quarantine, prompt injection from docs, artifact provenance, log leakage, admin paths | Security owner + Tech Lead (external review recommended) | M | B3a (006) | Risks/mitigations mapped; supports G0-S | `SINA_RiskQA_v1.5.md`, ADR-006/014 |
| B14 | 7 | Doc-governance prep: grep-verify all cited refs; fix README rule-source/date in implementation pass; header/version/date lint checklist; verify AGENTS/PROJECT_RULES consistency | Tech Lead | S | B1/B2 context | Verified ref list + checklist; **prerequisite for B7–B13 SSOT edits** | `README.md`, `AGENTS.md`, `PROJECT_RULES.md` |
| B7a | 7 (quick win) | **Immediate, low-risk doc fixes (no ADR/spike):** remove “reverse text/chunk order” (Arch); fix Unicode mapping in DataLake (`U+064A→U+06CC`, `U+0643→U+06A9`); fix ICU misattribution to Haystack; fix README date/rule-source. | Tech Lead/Editor | S | B14, explicit user approval | Corrections applied with headers/version bumps and cross-ref check | Arch, DataLake, Tools, `README.md` |
| B7b | 7,1 | Full Normalization Contract after ADR-011: ZWNJ policy, Unicode form (NFKC/NFC), chunk unit/size/overlap, align DataFlow/DataLake/Tools/Splitter/RiskQA TC-02. | NLP owner | M | B3b (011), B4, B14 | One versioned contract; tests/examples aligned | Arch, DataFlow, DataLake, Tools, Splitter SSOT, RiskQA |
| B8 | 2,3 | Identity/AuthZ/data-model baseline: authN first, in-process PDP, Blob/Document/Chunk, deterministic `ingest_id`, ACL revocation behavior | Backend Lead + Security | L | B3b (006–008), B6, B14 | Design/tasks decomposed; no cross-tenant leak path | Arch, DataFlow, Roadmap/Sprint, RiskQA |
| B9 | 3 | Ingestion reliability: job state machine/outbox/leases+heartbeat+stale recovery; Raw never auto-expire; RPO/RTO/schedule coherent; rebuild measured | Backend Lead | L | B3b (005,008–010), B5, B14 | State model + backup/restore runbook; derivatives rebuildable/measured | Arch, DataLake, SprintPlan, LLMOps |
| B10 | 4 | Capacity controls: TTFT/full definitions, LLM gateway queue/timeout/circuit breaker, ingestion/query isolation; query never queued behind ingestion | Backend Lead | M | B5, B8, B14 | Gate thresholds measurable; degradation mode defined | Roadmap, SprintPlan, Arch, LLMOps |
| B11 | 5 | Scope/ports simplification: minimal stack, full port catalog, apply ADR-015; defer/remove Whoosh/LangChain as justified | Tech Lead + Arch owner | M | B3b (002,005,015), B14 | Approved target architecture + deferred items gated | Arch, Tools, Roadmap/Sprint |
| B16 | 5,7 | **Walking skeleton** (thin Persian RAG path): ingest minimal doc → normalize per interim rules → index → retrieve → answer/citation with authN/policy hook, no full Lakehouse/Entity | Backend Lead + Tech Lead | L | B0, B3a/B3b inputs as available, B4 minimal, B7a/B8/B11 direction | Runnable skeleton on target HW with Golden Set smoke tests; proves critical path | implementation artifacts (not SSOT docs except references) |
| B12 | 6 | Pipeline fingerprint + coordinated snapshot cutover (vector+BM25) | Backend/ML owner | M | B3b (003,009,010), B9, B14 | Fingerprint stored; cutover/rollback runbook tested | Arch, LLMOps, SprintPlan |
| B13 | 2,7 | Quality gate repair: remove invalid RRF 0.65; security expectations realistic/earlier; accuracy protocol | PO + Tech Lead + QA | S | B4, B6, B8, B14 | Gates measurable/aligned to phase capabilities | Roadmap, SprintPlan, RiskQA |
| B15 | 3,4 | Recovery drills from Phase 1; governance independence for gate/security approval | Ops/Security + PO | M | B9, B6, B14 | Drill schedule/evidence; named independent approver | LLMOps, RiskQA, Roadmap |

**Backlog dependency graph (acyclic):** B0 → B1 → B2 → B3a → (B4,B5,B6) → B3b; B14 depends on B1/B2 context and gates SSOT edits; B7a quick win after B14+approval; B7b/B8–B13 after B3b/B14; B16 can start once B0 and minimal B3a/B4/B7a/B8 direction exist (time-boxed spike) but production path follows B3b.

## 4. Doc-change map (SSOT-compliant, implementation mode)

| SSOT target | Changes |
|---|---|
| `README.md` | Fix rule source to `AGENTS.md`; fix date to 1405 (2026); decision register; study-guide warnings; Data Lake summary+link only. |
| `ADR-SSOT-001.md` + new `ADR-002..015` | Freeze decisions; expand ADR governance scope via `AGENTS.md`. |
| `AGENTS.md` / `PROJECT_RULES.md` | `AGENTS.md` rules SSOT + ADR process; keep `PROJECT_RULES.md` stub consistent. |
| `Enterprise AI Infrastructure_ Document Intelligence & RAG Ecosystem.md` | Resolve options→decisions; remove reverse-text; fix CDC/alias atomicity; align HW; port catalog; cross-cutting; refs to ADRs/DataLake SSOT. |
| `End-to-End Data Flow.md` | Lake touchpoints, ACL/revocation, DLQ, deterministic ingest_id, TTFT/memory scope, no hardcoded dims. |
| `Data-Lake-Discussion-Summary.md` | Fix Unicode mapping; Raw immutability; partition contract; entity ACL/freshness; encryption pointer; ZWNJ resolved per ADR-011. |
| `SINA_Roadmap_v1.5.md` / `SINA_SprintPlan_v1.5.md` | Phase 0 6–8 weeks + Gate 0 (G0-D/E/Q/C/S/I); S1–S2 disposition; 18-month impact; security earlier; Golden Set/TTFT/capacity; fix RRF threshold; align RPO/backup/retention; stakeholder approval. |
| `SINA_RiskQA_v1.5.md` | R-001..R-016 mitigations/gates; independent approver; TC/ZWNJ alignment; unanswerables/accuracy protocol. |
| `SINA_LLMOps_v1.5.md` | Artifact provenance; Persian reranker evidence; consistent RPO/RTO/schedule; vector+BM25+snapshot migration. |
| `مستند بهبودیافته_ ابزارهای RAG و AI Agent.md` | Remove/label CPU-irrelevant benchmarks; fix ICU attribution; adapter-only hexagonal example; align to ADRs. |
| `Archive/README.md` | Update only if files archived/moved. |

## 5. Open questions (confirm before execution)
1. Binding decisions only in **PDF/PPTX/PNG/MP4**?
2. **Target hardware** (cores/RAM/disk), corpus size/growth, and environment constraints for Phase 0/1 — **B0 blocker**.
3. **Air-gapped off-site backup** method feasible?
4. Required **ACL revocation SLA**?
5. **Conversation memory** in scope for query rewriting/state?
6. Named **independent approver** for security/gate evidence (besides Backend Lead)?
7. **Team capacity/named owners** for NLP, Security/ML review, and QA (embedded) — assign or arrange external review?
8. **S1–S2 disposition:** run in parallel with revised Phase 0 or reschedule? **Stakeholder approval** authority for gate/date/18-month changes?

## 6. Recommendation
Adopt **ADR-015**: 6–8 week Phase 0, freeze critical-path ADRs via **B3a→evidence→B3b**, deliver thin Persian RAG walking skeleton (B16) with authN/policy hooks + Golden Set + capacity evidence, then expand only behind gates. Do quick-win factual fixes (B7a) after B14+approval. Defer OPA/Entity/Lakehouse/Trino/Iceberg/Keycloak/Temporal/K8s until evidence requires them.

## 7. Execution checklist
- [ ] Resolve B0 + open questions (esp. hardware, owners/approver, S1–S2/stakeholder approval).
- [ ] B14 prep (grep-verify refs) → **B7a quick wins** after explicit user approval (SSOT edits).
- [ ] B1/B2 (Phase 0/Gate 0/reschedule + decision register) after stakeholder approval.
- [ ] B3a drafts → B4/B5/B6 evidence → B3b accept/defer.
- [ ] B7b–B13, B16 walking skeleton, B15 drills per dependencies.
- [ ] Cross-reference audit before archive/move; update `AGENTS.md` ADR scope.
- [ ] Re-validate P1–P15; close/carry residual risks in `SINA_RiskQA_v1.5.md`. No commit/push without explicit user approval.