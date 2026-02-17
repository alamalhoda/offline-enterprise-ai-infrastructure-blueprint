# Enterprise AI Infrastructure: Document Intelligence & RAG Ecosystem

**Status:** Draft | **Version:** 1.1 | **Environment:** Air-Gapped / CPU-Only

## Executive Summary

This architecture outlines a resilient, backend-agnostic system for managing a large-scale multilingual (primarily Persian/English) document corpus in a fully air-gapped environment. It emphasizes deterministic retrieval via hybrid search (BM25 + Vector), with strong provisions for Persian NLP challenges such as RTL text handling and character normalization. Offline constraints are prioritized through local model registries, manual update pipelines, and rebuild-from-source strategies to ensure long-term maintainability without internet dependency. The design supports auditability, governance, and scalability while optimizing for CPU-only inference to minimize hardware costs in secure, isolated deployments.

---

## A. Layered System Architecture

The system adopts a **Hexagonal Architecture (Ports & Adapters)** to maintain backend agnosticism, allowing seamless integration with frameworks like Django while isolating core logic. This enables extensibility through defined interfaces (ports) for swapping components, such as replacing a vector DB without refactoring.

1. **Ingestion Layer (The "Senses")**

   - **Responsibilities:** Monitor file directories for changes, compute hashes, perform offline virus scanning (using pre-loaded definitions), and trigger idempotent ingestion. Handles initial format detection for PDFs/DOCX.
   - **Components:** Directory Watcher (e.g., Watchdog), Hashing Module, Ingress Gateway.
   - **Extensibility:** Ports for custom scanners or additional file formats (e.g., future support for scanned images with Persian OCR).
2. **Processing Layer (The "Brain" - CPU Optimized)**

   - **Responsibilities:** Extract text/layouts, normalize multilingual content (with Persian-specific rules), chunk documents semantically, and generate embeddings using quantized models. All operations are batched for CPU efficiency.
   - **Components:** ETL Pipelines, Normalization Engine (Persian-focused), Embedding Service (ONNX Runtime).
   - **Extensibility:** Adapters for new NLP models, ensuring offline loading from local repositories.
3. **Storage Layer (The "Memory")**

   - **Responsibilities:** Persist raw files, metadata, normalized text, and indexes with ACID guarantees for metadata and eventual consistency for search indexes. Supports offline backups and rebuilds.
   - **Components:** Object Store (MinIO), Relational DB (PostgreSQL), Vector/Hybrid Index (Qdrant or OpenSearch).
   - **Extensibility:** Modular schemas for adding fields like Persian-specific metadata (e.g., script direction).
4. **Indexing Layer (The "Catalog")**

   - **Responsibilities:** Maintain versioned vector and keyword indexes, handle deduplication, and support hybrid fusion. Offline index rebuilds are triggered manually or scheduled.
   - **Components:** Index Builder, Version Registry, Deduplication Clusterer.
   - **Extensibility:** Hooks for custom index types or fusion algorithms.
5. **Retrieval & Ranking Layer (The "Recall")**

   - **Responsibilities:** Execute hybrid queries, apply filters (e.g., ACLs), and re-rank results. Optimizes for Persian queries by expanding terms morphologically.
   - **Components:** Query Planner, Retriever Service, Re-ranker (Cross-Encoder).
   - **Extensibility:** Pluggable query expanders for additional languages.
6. **Orchestration & Governance Layer (The "Control")**

   - **Responsibilities:** Schedule background jobs, enforce policies (e.g., retention, ACLs), manage index migrations, and log audits. In offline mode, all orchestration is local with no external dependencies.
   - **Components:** Workflow Orchestrator, Policy Engine, Audit Logger.
   - **Extensibility:** Integration ports for enterprise identity providers (e.g., local LDAP).
7. **API & Interface Layer (The "Interface")**

   - **Responsibilities:** Expose REST/gRPC endpoints for ingestion/query, validate requests, and stream responses. Supports offline authentication via local tokens.
   - **Components:** API Gateway, Authentication Module.
   - **Extensibility:** Adapters for UI frameworks or additional protocols.
8. **Observability & Monitoring Layer (The "Eyes")**

   - **Responsibilities:** Collect metrics/logs offline, detect anomalies (e.g., embedding drift), and provide dashboards. All data stays local.
   - **Components:** Metrics Collector, Log Aggregator, Dashboard Server.
   - **Extensibility:** Exports to file-based reports for air-gapped analysis.

**Separation of Concerns:** Layers communicate via defined interfaces to prevent tight coupling, ensuring that changes in one layer (e.g., new Persian tokenizer) don't propagate. **Extensibility Strategy:** Use dependency injection for components; maintain a local model registry for offline updates, with versioning to avoid disruptions.

---

## B. Text-Based Component Diagram

```mermaid
graph TD
    User[User/Client App] --> API[API Gateway (REST/gRPC)]
    API --> Orch[Orchestrator Service (Workflow Engine)]
  
    subgraph "Ingestion & Processing Pipeline (Async, Offline)"
        Orch --> Q[Task Queue (Redis/RabbitMQ)]
        Q --> W1[Ingest Worker (Hashing, Scanning)]
        Q --> W2[Normalize Worker (Persian NLP)]
        Q --> W3[Embed Worker (ONNX, Quantized)]
      
        W1 -- Read/Write --> Blob[MinIO (Raw Files, Normalized Text)]
        W2 -- Process --> NLP[Multilingual NLP Module (Hazm/DadmaTools)]
        W3 -- Inference --> Models[Local Model Registry (HuggingFace/ONNX Files)]
    end
  
    subgraph "Storage & Indexing Plane"
        W1 -- Metadata --> DB[(PostgreSQL - Metadata, Schemas)]
        W3 -- Vectors/Keywords --> VDB[(Hybrid Vector DB - Qdrant/OpenSearch)]
        DB -- CDC/Sync --> VDB[Index Version Registry]
    end
  
    subgraph "Retrieval & Query Plane"
        API --> Search[Search Service (Query Planner)]
        Search --> VDB
        Search --> DB[ACL Filters]
        Search --> Models[Re-ranker]
    end
  
    subgraph "Governance & Observability"
        Orch --> Gov[Governance Engine (ACL, Audit)]
        All[All Components] --> Obs[Observability Stack (Prometheus/Loki)]
    end
  
    Obs --> Dash[Local Dashboard (Grafana)]
```

**Key Connections:**

- **Data Flow:** Unidirectional from Ingestion to Storage/Retrieval; normalized text is stored separately for offline re-embedding without re-parsing.
- **Control Flow:** Orchestrator triggers jobs via queues; governance intercepts all flows for compliance.
- **Background Pipelines:** Dedicated queues for re-indexing/migration, running in low-priority mode to avoid CPU contention.
- **Index Routing:** Queries route to the "active" index version via PostgreSQL registry; during migrations, a router proxies to both old/new indexes for zero-downtime.

---

## C. End-to-End Data Flow

1. **Document Ingestion:** Files dropped into watched directory. Worker computes SHA-256 hash and metadata (e.g., filename, size). Offline virus scan using pre-loaded ClamAV definitions. Edge case: Corrupted file → log error, quarantine to DLQ.
2. **Change Detection:** Query PostgreSQL for existing hash. If match, skip (idempotency). For updates, compare content fingerprint (e.g., perceptual hash for PDFs). Edge case: Persian filename encoding mismatch → normalize UTF-8 before hashing.
3. **Parsing & Normalization:** Use layout-aware parser to extract text/tables/images. For Persian, apply RTL detection and ZWNJ unification. Edge case: Mixed-script documents → segment by language before normalization.
4. **Chunking:** Semantic chunking with overlap (e.g., 20% window). Persian heuristics: Split at sentence boundaries using morphology-aware tools to avoid mid-word breaks. Edge case: Long RTL paragraphs → reverse chunk order for embedding alignment.
5. **Embedding Generation:** Batch chunks, embed using quantized multilingual model. Offline mode: Models loaded from local dir; no dynamic downloads. Edge case: CPU overload → fallback to smaller batches or sequential processing.
6. **Vector Indexing:** Store embeddings in HNSW index with payload (e.g., ACLs, lang). Edge case: High-dimensional drift in Persian embeddings → monitor and trigger alert.
7. **Hybrid Indexing:** Parallel BM25 index build with Persian tokenizers (stemming, stopwords). Edge case: Multilingual queries → route to language-specific sub-indexes.
8. **Query Flow:** User query normalized (e.g., Persian variants unified). Embed query, extract keywords. Edge case: Offline query expansion → use local synonym dictionary for Persian terms.
9. **RAG Orchestration:** Retrieve top-K from hybrid, re-rank, assemble context. Apply governance filters. Edge case: No results → fallback to keyword-only for sparse Persian corpora.
10. **Response Generation:** Feed context to local LLM for answer. Offline mode: All generation on-device; log full trace for audit. Edge case: Sensitive data in response → redact based on ACLs.

---

## D. Ingestion & Document Update Detection

- **File Hashing Strategy:** SHA-256 on raw bytes for initial dedup, combined with content-based fingerprint (e.g., ssdeep for fuzzy matching) to handle minor edits.
- **Content-Based Fingerprinting:** For PDFs, extract text hash post-normalization; ignore metadata changes.
- **Chunk-Level Diff Detection:** Use diff algorithms on normalized text chunks; only re-embed changed chunks. Trade-off: Compute-intensive but saves storage in large corpora.
- **Partial Re-Indexing:** Triggered by diff; update vector DB incrementally via upsert. Offline: Batch diffs nightly to minimize daytime CPU use.
- **Tombstone Strategy for Deletions:** Mark in PostgreSQL with `deleted_at`; propagate to vector DB via background job. Retain for audit (e.g., 90 days).
- **Version History Tracking:** Each document has a version chain in SQL; queries can filter by version.
- **Idempotent Ingestion Design:** Use unique `ingest_id` (hash + timestamp); duplicate jobs abort early.

---

## E. Semantic Deduplication

- **Exact Duplicate Detection:** SHA-256 on normalized text post-Persian unification.
- **Near-Duplicate Detection via Embedding Similarity:** Cosine threshold (>0.95); cluster using MiniBatchKMeans for efficiency.
- **LSH or Clustering Strategy:** Use Random Projection LSH for initial bucketing; refine with exact similarity. Offline: Pre-compute LSH indexes locally.
- **Cross-Document Deduplication:** Scan across corpus; link duplicates via references in DB to avoid vector storage bloat.
- **Multilingual Normalization Impact:** Persian variants (e.g., ي/ی) unified before embedding; this reduces false negatives in dedup but may merge semantically distinct terms—mitigate with language tagging.
- **Storage Optimization Techniques:** Store deduped chunks as references; compress vectors with PQ. Trade-off: Slight recall loss vs. 50-70% storage savings in Persian-heavy corpora.

---

## F. Hybrid Search Architecture (BM25 + Vector)

- **Unified vs Separate Index Trade-Offs:** Unified (e.g., OpenSearch) simplifies management but increases RAM; separate (pgvector + FTS) allows independent scaling but requires custom fusion logic. Choose unified for offline simplicity.
- **Score Fusion:** RRF primary; weighted merge optional (e.g., 0.7 vector + 0.3 BM25 for Persian, where keywords handle morphology better). Learned ranking: Offline-trained linear model if corpus allows.
- **Query Planner Design:** Parse query lang; for Persian, apply stemming/query expansion; execute parallel searches; fuse scores.
- **Retrieval Pipeline:** Pre-filter (ACLs, dates); retrieve; post-filter (dedup).
- **Trade-Offs Between Options:**
  - **Elasticsearch/OpenSearch:** Excellent Persian analyzers (ICU plugin for RTL/ZWNJ); high throughput but RAM-heavy.
  - **PostgreSQL + pgvector + FTS:** Lightweight, ACID; weaker Persian tokenization—augment with extensions.
  - **Dedicated Vector DB + Search Engine:** Qdrant (vectors) + Whoosh (BM25); flexible but more components to maintain offline.

---

## G. Index Versioning Strategy

- **Index Version Registry Design:** PostgreSQL table tracking versions; offline exports to JSON for backups.
- **Embedding Model Version Tracking:** Each version links to model hash/path in local registry.
- **Metadata Schema for Index Lifecycle:** Include `build_params` (e.g., HNSW M=16), `compatibility_flags` (e.g., dimension match).
- **Rolling Index Migration:** Build new index in parallel; test offline with golden queries.
- **Zero-Downtime Index Switching:** Use alias in config; atomic update via DB trigger.
- **Backward Compatibility Handling:** Maintain old indexes for queries; deprecate after grace period. Offline: Manual verification before switch.

---

## H. Re-Embedding Strategy (Model Evolution)

- **Full vs Incremental Re-Embedding:** Incremental for minor changes (e.g., quantization); full for model swaps.
- **Background Parallel Index Creation:** Low-priority workers process stored normalized text; offline queuing prevents overload.
- **Consistency Guarantees (Strong vs Eventual):** Eventual for search (acceptable lag); strong for metadata. Trade-off: Eventual reduces downtime but risks stale results.
- **Atomic Index Cutover Strategy:** Validate new index coverage; flip alias in DB.
- **Query Routing During Migration:** Router directs % of queries to new index for A/B testing; full switch post-validation.
- **Performance Optimization:** Batch size tuned to CPU (e.g., 32); prioritize Persian chunks if corpus skewed.

---

## I. Persian / Multilingual NLP Challenges

- **Unicode Normalization:** Apply NFKC; unify Persian/Arabic variants (ي/ی, ك/ک) to Persian forms to prevent embedding fragmentation.
- **ZWNJ (Half-Space) Handling:** Replace with standard space or preserve as token; test impact on retrieval accuracy offline.
- **Character Variants:** Custom mapping table for offline use; apply pre-tokenization.
- **Tokenization Issues:** Use morphology-aware tokenizers; handle agglutinative Persian words to avoid subword overflow.
- **Stopword Strategy:** Curated list (e.g., from Hazm) + custom additions for domain-specific terms; bilingual lists for mixed docs.
- **Morphology & Stemming:** Persian stemmer (e.g., DadmaTools) for BM25; reduces index size by 20-30%.
- **RTL Considerations:** Reverse text for left-to-right embeddings; ensure query/display handles bidi.
- **Multilingual Embedding Alignment:** Use aligned models (e.g., LaBSE); offline fine-tune if needed for Persian-English cross-lingual recall.
- **Chunking Heuristics for Persian Text:** Sentence-based with RTL-aware boundaries; max chunk 512 tokens; overlap for context preservation.

---

## J. CPU-Only Performance & Cost Optimization

- **Embedding Batch Sizing:** Dynamic: Start at 16, adjust based on CPU load; offline profiling for Persian text (longer sentences increase time).
- **Quantization Strategies:** ONNX Runtime with INT8/FP16; reduces model footprint 4x, inference 2x faster with <2% accuracy drop.
- **Index Type Selection:** HNSW for fast queries; IVF for large corpora (trade-off: build time vs. recall). Flat for small setups.
- **Memory Footprint Control:** Vector compression (PQ); limit index to RAM-resident for speed.
- **Storage Layout Optimization:** SSD for indexes; HDD for raw files. Offline: Defrag indexes periodically.
- **Concurrency Model:** Threaded workers (e.g., 4 per core); avoid over-subscription.
- **Caching Strategy:** LRU cache for frequent embeddings/queries; local Redis.
- **Cold Start Mitigation:** Pre-warm models on startup; offline scripts for benchmarking.
- **Disk vs RAM Trade-Offs:** RAM for hot indexes (fast); disk for cold (cost-effective); hybrid for Persian corpora where queries are sparse.

---

## K. Observability & Auditability

- **Structured Logging Strategy:** JSON logs with fields (e.g., `event_type`, `persian_text_length`); rotate offline.
- **Metrics and Monitoring in Offline Mode:** Prometheus scrapes local endpoints; export to files for analysis.
- **Index Health Monitoring:** Check fragmentation, dimension consistency.
- **Embedding Drift Detection:** Offline batch jobs compare distributions (KS-test) quarterly.
- **Retrieval Quality Monitoring:** Log MRR per query; aggregate locally.
- **Audit Trail for Document and Index Changes:** Immutable logs in PostgreSQL; include Persian-specific events (e.g., normalization applied).
- **Failure Tracing Strategy:** Distributed tracing with local Jaeger; no external sends.

---

## L. Data Governance & Compliance

- **Data Lineage Tracking:** Track full chain (source → normalized → embedded) in DB; queryable for audits.
- **Document-Level Access Control (ACL):** RBAC with groups; enforce at retrieval.
- **Sensitive Data Tagging:** Offline ML classifier tags PII (e.g., Persian names); mask in responses.
- **Retention Policy:** Configurable (e.g., delete after 5 years); automated via cron jobs.
- **Role-Based Access Model:** Admin/Reader/Auditor; local auth.
- **Index-Level Security Boundaries:** Partition indexes by sensitivity; Persian docs often tagged "confidential" due to cultural contexts.

---

## M. Consistency & Reliability Model

- **Strong vs Eventual Consistency Trade-Offs:** Strong for ingestion/metadata (immediate visibility); eventual for indexes (lag <5min acceptable offline).
- **Atomic Index Switching Mechanism:** DB transaction flips alias; rollback on failure.
- **Read/Write Isolation During Reindex:** Shadow writes to both indexes; reads from old until switch.
- **Idempotent Background Jobs:** Use job IDs; retry with backoff.
- **Failure Recovery Design:** Checkpointing for long jobs; offline rebuild from logs.
- **Retry & Dead-Letter Queue Strategy:** Exponential retry (max 5); DLQ for manual review, especially for Persian parsing failures.

---

## N. Backup & Disaster Recovery (Offline Context)

- **Index Snapshotting Strategy:** Filesystem snapshots (e.g., BTRFS); versioned for rollback.
- **Raw Document Canonical Storage:** MinIO with replication; immutable buckets.
- **Rebuild-from-Source Design:** Scripts to re-ingest from raw + normalized text; prioritized for Persian to minimize downtime.
- **Cold vs Hot Backup Trade-Offs:** Hot (live snapshots) for low RTO (<1h); cold (offline dumps) for low cost but higher RTO (4-8h).
- **Recovery Time Objectives:** RTO <2h for metadata, <24h for full index; tested quarterly offline.

---

## O. Evaluation & Quality Control

- **Retrieval Evaluation Metrics:** Recall@K, MRR, NDCG; compute offline on held-out set.
- **Golden Query Test Set Design:** Curated bilingual queries (50% Persian); include edge cases like ZWNJ variants.
- **Embedding Benchmarking:** Offline A/B tests on precision/recall for new models.
- **Drift Detection Over Time:** Monitor vector centroids; alert if Persian cluster shifts >10%.
- **Continuous Validation Pipeline (Offline):** Scheduled jobs run golden set; fail if metrics drop >3%; log results locally.

---

## P. Scalability Roadmap

- **Single-Node Production Architecture:** All-in-one server (e.g., 128GB RAM, 32 cores); Docker for isolation.
- **Vertical Scaling Strategy:** Upgrade hardware; partition data (e.g., Persian-only node).
- **Horizontal Scaling Evolution:** Add nodes for workers/index replicas.
- **Cluster-Ready Design:** Kubernetes manifests; shared MinIO for storage.
- **Future GPU Integration Strategy:** Conditional loading in code; offline model conversion to CUDA.

---

## Q. Storage & Data Schema Design

- **Raw File Storage Layout:** MinIO buckets: `raw/docs`, versioned objects.
- **Processed Text Storage:** Bucket `normalized/text`; JSON per chunk with lang tag.
- **Metadata Schema (SQL):**
  ```sql
  CREATE TABLE documents (
      id UUID PRIMARY KEY,
      content_hash CHAR(64) UNIQUE,
      filename TEXT,
      lang ENUM('fa', 'en', 'mixed'),
      metadata JSONB,
      acl_groups TEXT[],
      versions JSONB -- array of {version_id, timestamp}
  );
  CREATE TABLE chunks (
      id UUID PRIMARY KEY,
      doc_id UUID REFERENCES documents,
      chunk_text TEXT,
      norm_text TEXT, -- Persian-normalized
      embedding_version VARCHAR
  );
  ```
- **Vector DB Schema:** Collections with fields: `id`, `vector`, `payload` (incl. `lang`, `acl`).
- **Index Version Registry Schema:** Table with `version_tag`, `model_hash`, `build_date`.
- **Deduplication Registry:** Table mapping duplicate chunks to canonical IDs.

---

## R. Background Processing Architecture

- **Task Queue Design:** Redis for fast, RabbitMQ for durable; offline persistence.
- **Job Orchestration Model:** Celery with priority queues (e.g., high for queries).
- **Parallelism Strategy:** Worker pools scaled to CPU cores; embarrassingly parallel for embedding.
- **Failure Recovery:** Auto-retry; checkpoints for Persian-heavy jobs.
- **Idempotency Guarantees:** Job hashes; abort duplicates.

---

## S. Open-Source Tooling Recommendations

| Component                            | Tool Recommendation                                                                                                                      | Trade-Off / Rationale / Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vector Database**            | **Qdrant** (primary); **Faiss** (alternative for pure vectors); **LanceDB** (for disk-optimized)                       | Qdrant: Rust-based, CPU-efficient HNSW/IVF indexes, supports hybrid sparse vectors for BM25 integration; offline-friendly with file-based persistence. Trade-off: Less mature than OpenSearch but lower RAM (up to 30% savings on large Persian corpora). Faiss: Facebook's library for in-memory vectors; integrate via Python for custom apps—fast but no built-in query lang. LanceDB: Arrow-based for offline analytics; excels in cold storage trade-offs. All load locally without internet. |
| **Hybrid Search Engine**       | **OpenSearch** (with ICU plugin); **Whoosh** (lightweight Python alternative)                                                | OpenSearch: Fork of Elasticsearch; strong Persian analyzers (RTL, ZWNJ via custom ICU chains), score fusion built-in. Offline: Run in Docker, no AWS deps. Trade-off: Higher resource use vs. better recall in multilingual setups. Whoosh: Pure Python, no external deps; ideal for small offline nodes but slower indexing (2-5x vs. OpenSearch).                                                                                                                                                 |
| **OCR / Document Parser**      | **Docling/Surya** (AI-based); **Tesseract OCR** (with Persian traineddata); **pdfplumber** (for structured extraction) | Docling/Surya: Modern ML parsers for layouts/tables; offline via local models. Trade-off: CPU-heavy but accurate for mixed Persian-English PDFs. Tesseract: Free, supports Persian out-of-box; augment with custom training data for handwriting. pdfplumber: Lightweight for text/tables; no ML, fast on CPU. All run fully offline.                                                                                                                                                               |
| **NLP Framework**              | **Haystack** (pipelines); **LangChain** (prototyping); **Transformers** (HuggingFace for custom)                       | Haystack: Production-focused for RAG; modular, offline model loading. Trade-off: Steeper curve but better extensibility. LangChain: Quick for chains; offline-compatible. Transformers: Core library for tokenization/embedding; use with local Persian models like ParsBERT for stemming.                                                                                                                                                                                                          |
| **Persian NLP Specific**       | **Hazm** + **DadmaTools**; **Stanza** (Stanford NLP with Persian support)                                              | Hazm/Dadma: Python libs for normalization, stemming, POS tagging; offline, lightweight. Trade-off: Hazm faster, Dadma more accurate for morphology. Stanza: Multi-lingual pipeline; download models once offline; handles RTL/ZWNJ robustly. Essential for preprocessing to boost retrieval by 10-20% in Persian.                                                                                                                                                                                   |
| **Embedding Model**            | **intfloat/multilingual-e5-large** (quantized); **LaBSE** (for cross-lingual); **ParsBERT** (Persian-tuned)            | Multilingual-e5: Balanced size/performance; ONNX-quantized for CPU. Trade-off: General but may underperform on pure Persian—fine-tune offline. LaBSE: Aligned for Persian-English; better dedup. ParsBERT: BERT-based for Persian; smaller, faster on CPU. All stored locally.                                                                                                                                                                                                                     |
| **Local LLM for RAG**          | **Llama.cpp** (with GGUF quantized models); **Ollama** (containerized)                                                       | Llama.cpp: C++ for CPU inference; supports Llama/Mistral models quantized to 4-bit. Trade-off: Fast but no fine-tuning. Ollama: Easy Docker deployment; offline model pulls from local registry. Use for generation in air-gapped.                                                                                                                                                                                                                                                                  |
| **Task Queue / Orchestration** | **Celery** (with Redis/RabbitMQ); **Temporal** (for complex workflows)                                                       | Celery: Mature Python; idempotent, offline. Trade-off: Simple but scales via workers. Temporal: Go-based for resilience; better failure handling in long offline jobs like re-embedding.                                                                                                                                                                                                                                                                                                            |
| **Database**                   | **PostgreSQL 16** (with pgvector); **SQLite** (for small setups)                                                             | PostgreSQL: Robust JSONB, extensions for vectors/FTS; offline ACID. Trade-off: Heavier than SQLite but essential for governance. SQLite: Lightweight for single-node; use for testing.                                                                                                                                                                                                                                                                                                              |
| **Observability**              | **Prometheus + Grafana** (metrics/dashboards); **Loki + Grafana** (logs); **Jaeger** (tracing)                         | Prometheus/Grafana: Local scraping/visualization; offline exports to CSV. Trade-off: No cloud integration—manual alerts. Loki: LogQL for queries; pairs with Grafana for Persian log filtering. Jaeger: End-to-end tracing; fully local.                                                                                                                                                                                                                                                           |
| **Backup / Storage**           | **MinIO** (S3-compatible); **Duplicity** (encrypted backups)                                                                 | MinIO: Self-hosted object store; offline replication. Trade-off: S3 API but local only. Duplicity: Incremental encrypted backups to local drives; air-gapped compliant.                                                                                                                                                                                                                                                                                                                             |

**Additional Notes on Tools:** All recommendations are production-ready, open-source, and optimized for offline/CPU use. For Persian, prioritize tools with built-in support (e.g., ICU in OpenSearch). Offline deployment: Use Docker Compose for isolation; pre-download all models/dependencies during setup. Trade-offs evaluated based on benchmarks (e.g., e5-large quantized: 500ms/chunk on 16-core CPU).

### Implementation Note for Persian and Offline Context

In air-gapped environments, establish a local "model vault" directory for all artifacts (e.g., /opt/models); use scripts to verify hashes on import. For Persian accuracy, benchmark normalization pipelines offline: E.g., ZWNJ mishandling can drop recall by 15%—always unify to canonical forms. Ensure OS-level UTF-8 support in containers to handle RTL filenames without corruption. Periodic offline audits (e.g., via custom scripts) simulate internet-free updates.
