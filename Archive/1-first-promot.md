You are a Principal AI Architect, Lead Infrastructure Engineer, and Distributed Systems Expert specializing in secure, air-gapped, production-grade AI systems for enterprise environments.

Your task is to design a future-proof, enterprise-level AI infrastructure.

============================================================

1. CONTEXT & ENVIRONMENT
   ============================================================

Environment characteristics:

- Fully offline / air-gapped (no internet access)
- CPU-only inference required (GPU optional in future roadmap)
- Large-scale document corpus (PDF, DOCX, structured & unstructured data)
- Multilingual support required (e.g., Persian + English)
- Backend-agnostic (e.g., Django-compatible but not framework-dependent)
- High reliability, auditability, and long-term maintainability required
- Designed for enterprise production deployment

Primary Goal:
Design a complete AI-powered Document Intelligence + RAG ecosystem that:

- Ingests and processes documents
- Extracts structured and unstructured content
- Normalizes multilingual text
- Stores metadata and content
- Generates embeddings locally
- Maintains versioned vector indexes
- Supports hybrid retrieval (BM25 + Vector)
- Powers a Retrieval-Augmented Generation (RAG) assistant
- Enables safe model evolution and index migration
- Ensures auditability, governance, and resilience

No superficial explanations.
No tutorial-style answers.
Think and answer like an enterprise architect.

============================================================
2. REQUIRED ARCHITECTURAL SECTIONS
==================================

You MUST address the following areas in depth:

---

A. Layered System Architecture
------------------------------

- Clear logical layers (Ingestion, Processing, Storage, Indexing, Retrieval, Orchestration, API, Observability, Governance)
- Responsibilities per layer
- Separation of concerns
- Extensibility strategy

---

B. Text-Based Component Diagram
-------------------------------

Provide a structured description of components and how they connect.
Include:

- Data flow
- Control flow
- Background pipelines
- Index routing

---

C. End-to-End Data Flow
-----------------------

Step-by-step workflow:

1. Document ingestion
2. Change detection
3. Parsing & normalization
4. Chunking
5. Embedding generation
6. Vector indexing
7. Hybrid indexing
8. Query flow
9. RAG orchestration
10. Response generation

Include edge cases.

---

D. Ingestion & Document Update Detection
----------------------------------------

- File hashing strategy
- Content-based fingerprinting
- Chunk-level diff detection
- Partial re-indexing
- Tombstone strategy for deletions
- Version history tracking
- Idempotent ingestion design

---

E. Semantic Deduplication
-------------------------

- Exact duplicate detection
- Near-duplicate detection via embedding similarity
- LSH or clustering strategy
- Cross-document deduplication
- Multilingual normalization impact
- Storage optimization techniques

---

F. Hybrid Search Architecture (BM25 + Vector)
---------------------------------------------

- Unified vs separate index trade-offs
- Score fusion (RRF, weighted scoring, learned ranking optional)
- Query planner design
- Retrieval pipeline
- Trade-offs between:
  - Elasticsearch/OpenSearch
  - PostgreSQL + pgvector + FTS
  - Dedicated vector DB + search engine

---

G. Index Versioning Strategy
----------------------------

- Index version registry design
- Embedding model version tracking
- Metadata schema for index lifecycle
- Rolling index migration
- Zero-downtime index switching
- Backward compatibility handling

---

H. Re-Embedding Strategy (Model Evolution)
------------------------------------------

- Full vs incremental re-embedding
- Background parallel index creation
- Consistency guarantees (strong vs eventual)
- Atomic index cutover strategy
- Query routing during migration
- Performance optimization

---

I. Persian / Multilingual NLP Challenges
----------------------------------------

- Unicode normalization
- ZWNJ (half-space) handling
- Character variants (ي/ی, ك/ک)
- Tokenization issues
- Stopword strategy
- Morphology & stemming
- RTL considerations
- Multilingual embedding alignment
- Chunking heuristics for Persian text

---

J. CPU-Only Performance & Cost Optimization
-------------------------------------------

- Embedding batch sizing
- Quantization strategies (e.g., ONNX runtime)
- Index type selection (HNSW, IVF, Flat)
- Memory footprint control
- Storage layout optimization
- Concurrency model
- Caching strategy
- Cold start mitigation
- Disk vs RAM trade-offs

---

K. Observability & Auditability
-------------------------------

- Structured logging strategy
- Metrics and monitoring in offline mode
- Index health monitoring
- Embedding drift detection
- Retrieval quality monitoring
- Audit trail for document and index changes
- Failure tracing strategy

---

L. Data Governance & Compliance
-------------------------------

- Data lineage tracking
- Document-level access control (ACL)
- Sensitive data tagging
- Retention policy
- Role-based access model
- Index-level security boundaries

---

M. Consistency & Reliability Model
----------------------------------

- Strong vs eventual consistency trade-offs
- Atomic index switching mechanism
- Read/write isolation during reindex
- Idempotent background jobs
- Failure recovery design
- Retry & dead-letter queue strategy

---

N. Backup & Disaster Recovery (Offline Context)
-----------------------------------------------

- Index snapshotting strategy
- Raw document canonical storage
- Rebuild-from-source design
- Cold vs hot backup trade-offs
- Recovery time objectives

---

O. Evaluation & Quality Control
-------------------------------

- Retrieval evaluation metrics (Recall@k, MRR, NDCG)
- Golden query test set design
- Embedding benchmarking
- Drift detection over time
- Continuous validation pipeline (offline)

---

P. Scalability Roadmap
----------------------

- Single-node production architecture
- Vertical scaling strategy
- Horizontal scaling evolution
- Cluster-ready design
- Future GPU integration strategy

---

Q. Storage & Data Schema Design
-------------------------------

- Raw file storage layout
- Processed text storage
- Metadata schema (SQL)
- Vector DB schema
- Index version registry schema
- Deduplication registry

---

R. Background Processing Architecture
-------------------------------------

- Task queue design
- Job orchestration model
- Parallelism strategy
- Failure recovery
- Idempotency guarantees

---

S. Open-Source Tooling Recommendations
--------------------------------------

Recommend production-ready open-source tools optimized for:

- Offline use
- CPU inference
- Persian NLP
- Vector storage
- Hybrid search
- Observability
- Background processing

Explain trade-offs for each selection.

============================================================
3. OUTPUT FORMAT REQUIREMENTS
=============================

Your output must be:

- A professional Technical Architecture Document
- Structured in Markdown
- Organized by sections above
- Deeply analytical
- Production-oriented
- Explicit about trade-offs
- Future-proof
- No shallow summaries

Think like you are designing infrastructure for a large enterprise with long lifecycle requirements.
