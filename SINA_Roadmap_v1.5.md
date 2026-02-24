# SINA — نقشه راه یکپارچه (Unified Roadmap)

### Secure Intelligent Network Assistant | CPU-Only / Air-Gapped | با Quality Gate و تعریف Done

---

| مورد | مقدار |
|------|--------|
| نسخه مستند | 1.5 — تلفیقی (از RoadMap v1.0 + RoadMap v2.0) |
| تاریخ تهیه | بهمن ۱۴۰۴ / فوریه ۲۰۲۶ |
| محیط هدف | Air-Gapped / CPU-Only / آفلاین |
| افق زمانی | فاز صفر ۴ هفته + ۱۸+ ماه (۴ فاز اصلی) |
| مخاطبان | تیم فنی / مدیریت ارشد / کارفرما |

---

## ۱. چشم‌انداز و اهداف

### ۱.۱ چشم‌انداز محصول

> **SINA** یک دستیار هوش مصنوعی سازمانی کاملاً آفلاین است که کارکنان را قادر می‌سازد در کمتر از ۳۰ ثانیه (هدف)، پاسخ دقیق با ارجاع سند از میان هزاران فایل سازمانی دریافت کنند — بدون وابستگی به اینترنت یا سرویس ابری و **بدون نیاز به GPU** در محیط Production.

### ۱.۲ اهداف کلیدی پروژه

- استقرار یک سیستم RAG کاملاً آفلاین با پشتیبانی کامل از زبان فارسی
- معماری مدولار و لایه‌بندی‌شده برای جایگزینی اجزا بدون توقف سیستم
- پردازش بهینه روی **CPU** با مدل‌های کوانتیزه‌شده (ONNX / GGUF)
- Hybrid Search (BM25 + Vector) برای دقت بالا در جستجوی اسناد فارسی
- رعایت الزامات امنیتی، Audit Logging و Data Governance سازمانی
- مقیاس‌پذیری افقی از Single-Node تا Multi-Node بدون تغییر معماری

### ۱.۳ اهداف کمی (Success Metrics)

| هدف | معیار | زمان سنجش |
|-----|--------|-----------|
| دقت پاسخ | ≥ 75% روی سوالات تعریف‌شده | پایان Phase 1 (MVP) |
| زمان پاسخ | ≤ 30 ثانیه برای 95% درخواست‌ها (روی CPU) | پایان Phase 1 |
| پوشش اسناد | ≥ 1000 فایل PDF/Word ایندکس‌شده | پایان Phase 1 |
| Recall@5 (فارسی) | > 70% حداقل؛ هدف > 85% | Phase 2 و بعد |
| Uptime | ≥ 99% در ساعات کاری | Phase 2 به بعد |
| Audit Coverage | 100% دسترسی‌ها ثبت‌شده | از Sprint 1 |

---

## ۲. محدودیت‌های کلیدی (Constraints)

| محدودیت | جزئیات | راهکار معماری |
|---------|--------|----------------|
| Air-Gapped / آفلاین | بدون دسترسی به اینترنت در محیط Production | Local Model Registry، Manual Update Pipeline، Offline Docker Images |
| CPU-Only | بدون GPU در سرور Production | ONNX INT8 Quantization، Batch Processing، GGUF LLM Format |
| زبان فارسی | RTL، ZWNJ، کاراکترهای عربی/فارسی | Hazm + DadmaTools، Persian-aware Chunking، NFKC Normalization |
| تیم Backend-Centric | ML/AI و DevOps در تیم Backend ادغام شده | Role Rotation، Cross-training، مستندات فنی دقیق |

---

## ۳. نمای زمانی کلان

| فاز | نام | مدت | خروجی کلیدی | Gate |
|-----|-----|-----|-------------|------|
| **Phase 0** | Foundation & Setup | ۴ هفته | محیط توسعه، مدل‌ها روی CPU، CI، ADR | **Gate 0** |
| **Phase 1** | Foundation & Infrastructure | ماه ۱–۶ | Ingestion، NLP، Storage، Embedding، E2E Alpha | — |
| **Phase 2** | Core RAG Engine | ماه ۷–۱۱ | Hybrid Search، LLM، RAG E2E، API، Beta | **Gate 1** |
| **Phase 3** | Enterprise Hardening | ماه ۱۲–۱۵ | RBAC، Audit، Observability، Backup، Production v1.0 | **Gate 2** |
| **Phase 4** | Optimization & Scale | ماه ۱۶+ | DSPy، Agent، Fine-tune، Scale | — |

هیچ فازی بدون **تأیید صریح Gate** (در جاهایی که تعریف شده) شروع نمی‌شود. جزئیات Sprintها و User Storyها در **SINA_SprintPlan_v1.0** آمده است.

---

## ۴. فاز صفر — Foundation & Setup (هفته ۱ تا ۴)

**هدف:** تمام اعضای تیم روی همان Stack کار کنند؛ مدل‌ها روی سرور (CPU) هستند و پاسخ می‌دهند.

### ۴.۱ Milestoneهای Phase 0

- **M0.1 — محیط توسعه یکپارچه (پایان هفته ۲)**  
  Docker Compose با تمام سرویس‌ها UP، Gitea + Branch Strategy، PyPI Mirror آفلاین.  
  *(بدون شرط GPU؛ در صورت وجود GPU اختیاری برای توسعه قابل استفاده است.)*

- **M0.2 — Stack پایه نصب و تست (پایان هفته ۴)**  
  - مدل LLM (مثلاً GGUF) لود شده و Hello World روی **CPU** پاسخ داد  
  - مدل Embedding (مثلاً multilingual-e5 یا BGE-M3) به ONNX و روی **CPU** تست شد  
  - Qdrant راه‌اندازی و یک Vector ذخیره/بازیابی شد  
  - CI Pipeline: هر Push → تست خودکار  
  - مستند ADR نسخه ۱؛ فرآیند HDD Update مستند و یک بار تست شد  

### ۴.۲ Quality Gate 0 (پایان هفته ۴)

| # | معیار | حد قابل قبول | تصمیم‌گیرنده |
|---|--------|---------------|---------------|
| QG0.1 | همه Container در Docker Compose بالا می‌آیند | 100% بدون خطا | Tech Lead |
| QG0.2 | مدل GGUF یک سوال فارسی روی CPU پاسخ می‌دهد | پاسخ منطقی | Tech Lead |
| QG0.3 | Embedding روی CPU اجرا می‌شود | زمان قابل قبول برای یک متن (مثلاً < ۱۰ ثانیه برای batch کوچک) | Backend Lead |
| QG0.4 | نصب آفلاین از PyPI Mirror کار می‌کند | بدون نیاز به اینترنت | Backend Lead |
| QG0.5 | CI Pipeline در هر Push اجرا می‌شود | حداکثر ۵ دقیقه | Tech Lead |

**نتیجه Gate 0:** ✅ همه معیارها → Phase 1 شروع | ⚠️ ۱–۲ مورد ناموفق → تمدید تا ۱ هفته | ❌ بیش از ۲ مورد → بازبینی Stack. *ارزیابی Gate 0 پس از Sprint 2 در برنامه Sprint (SINA_SprintPlan_v1.0) انجام می‌شود.*

---

## ۵. فاز ۱ — Foundation & Infrastructure (ماه ۱ تا ۶)

هدف: پایه‌های محکم فنی؛ Ingestion، NLP فارسی، Storage، Embedding روی CPU، E2E Alpha.

### ۵.۱ اهداف فاز ۱

- راه‌اندازی محیط توسعه کامل (Docker Compose، Local Registries)
- Ingestion Layer با PDF/DOCX و Hashing؛ Persian NLP (Hazm + DadmaTools + ONNX)
- Storage: MinIO + PostgreSQL + Qdrant
- Embedding Service با مدل multilingual-e5 (یا BGE-M3) کوانتیزه ONNX روی CPU
- Task Queue با Celery + Redis
- تست E2E: آپلود فایل فارسی → Embed → ذخیره در Qdrant

### ۵.۲ Milestoneهای فاز ۱ (خلاصه)

| Milestone | ماه | Definition of Done |
|-----------|-----|---------------------|
| M1.1 — Dev Env | ۱ | Docker Compose up بدون خطا، تمام service‌ها healthy |
| M1.2 — Storage | ۲ | MinIO، PostgreSQL schema، Qdrant collection آماده؛ Integration Test اولیه (ذخیره/بازیابی) موفق. *Integration Test کامل و Data Quality در S9–S10 (برنامه Sprint) تکمیل می‌شود.* |
| M1.3 — Ingestion | ۳ | PDF/DOCX فارسی آپلود → hash → scan → Queue |
| M1.4 — NLP | ۴ | متن نرمال‌سازی، ZWNJ حل شده، Chunk‌های معنادار |
| M1.5 — Embedding | ۵ | مدل ONNX لود، Batch Embedding روی CPU < 5 ثانیه برای ۱۰ chunk |
| M1.6 — E2E Alpha | ۶ | فایل فارسی → embed → Qdrant → query اولیه جواب دهد |

**نگاشت با برنامه Sprint (SINA_SprintPlan_v1.0):** M0.1/M0.2 → S1–S2؛ M1.1 → S1–S2؛ M1.2/M1.3 → S3–S4؛ M1.4 → S5–S6؛ M1.5 → S7–S8؛ Storage Integration & Data Quality → S9–S10؛ M1.6 → S11–S12.

### ۵.۳ Stack فنی فاز ۱

| لایه | ابزار | توضیح |
|------|--------|-------|
| Document Parser | PyMuPDF + pdfplumber | استخراج متن/جدول از PDF بدون GPU |
| Persian NLP | Hazm + DadmaTools | نرمال‌سازی، ZWNJ |
| Embedding | multilingual-e5-base (ONNX INT8) | کوانتیزه روی CPU |
| Vector DB | Qdrant | HNSW، کم‌مصرف روی CPU |
| Metadata DB | PostgreSQL 16 | ACID، JSONB |
| Object Store | MinIO | S3-compatible، offline |
| Task Queue | Celery + Redis | Async، Retry، DLQ |

---

## ۶. فاز ۲ — Core RAG Engine (ماه ۷ تا ۱۱)

هدف: موتور RAG کامل؛ Hybrid Search، LLM روی CPU، API، Beta.

### ۶.۱ اهداف فاز ۲

- Hybrid Search (BM25 + Vector + RRF)؛ Re-ranking با Cross-Encoder روی CPU
- LLM (Llama.cpp + GGUF) برای Generation روی CPU
- RAG Orchestrator (Haystack)؛ API با FastAPI (REST + SSE)؛ JWT
- Persian Query Normalization و Query Expansion؛ تست دقت با Golden Query Set

### ۶.۲ Milestoneهای فاز ۲ (خلاصه)

| Milestone | ماه | Definition of Done |
|-----------|-----|---------------------|
| M2.1 — BM25 | ۷ | Keyword Search با Persian Analyzer؛ Recall@10 > 80% |
| M2.2 — Hybrid | ۸ | RRF Fusion؛ MRR Hybrid > MRR Vector-only |
| M2.3 — LLM | ۸ | Llama.cpp GGUF روی CPU؛ > 8 token/sec؛ پاسخ فارسی منسجم |
| M2.4 — Orchestrator | ۹ | Query → Normalize → Embed → Hybrid → Rerank → LLM → Response |
| M2.5 — API | ۱۰ | REST، SSE، JWT، Swagger |
| M2.6 — Beta | ۱۱ | Recall@5 > 75%، Latency E2E < 30 sec، ۱۰ کاربر همزمان |

### ۶.۳ معیارهای کیفیت فاز ۲

| معیار | حداقل | هدف |
|--------|--------|------|
| Recall@5 (فارسی) | > 70% | > 85% |
| E2E Latency (CPU) | < 45 sec | < 20 sec |
| Hallucination Rate | < 20% | < 10% |
| Concurrent Users | ≥ 5 | ≥ 15 |

### ۶.۴ Quality Gate 1 (پایان ماه ۱۱ / قبل از فاز ۳)

| # | معیار | حد قابل قبول | تصمیم‌گیرنده |
|---|--------|---------------|---------------|
| QG1.1 | دقت پاسخ روی سوالات تعریف‌شده | ≥ 75% | Product Owner |
| QG1.2 | زمان پاسخ (P95) روی CPU | ≤ 30 ثانیه | Backend Lead |
| QG1.3 | پوشش اسناد | ≥ 1000 فایل ایندکس | Backend Lead |
| QG1.4 | Recall جستجو | ≥ 70% روی Golden Set | Tech Lead |
| QG1.5 | کنترل دسترسی و Audit Log | 100% query‌ها ثبت | Security |

**نتیجه Gate 1:** ✅ همه موفق → Phase 3 شروع | ⚠️ QG1.1 یا QG1.2 ناموفق → تمدید ۲ Sprint | ❌ QG1.5 ناموفق → توقف، بازبینی امنیتی. *ارزیابی Gate 1 پس از Sprint 22 در برنامه Sprint انجام می‌شود.*

---

## ۷. فاز ۳ — Enterprise Hardening (ماه ۱۲ تا ۱۵)

هدف: RBAC، Audit، Observability، Backup، Production v1.0.

### ۷.۱ اهداف و Milestoneهای فاز ۳ (خلاصه)

| Milestone | ماه | Definition of Done |
|-----------|-----|---------------------|
| M3.1 — Security | ۱۲ | RBAC و ACL؛ هر درخواست بدون Token رد شود |
| M3.2 — Audit | ۱۲ | هر دسترسی به سند ثبت؛ گزارش ۳۰ روزه قابل Export |
| M3.3 — Observability | ۱۳ | Grafana با ۱۰ metric؛ Alert CPU > 80% |
| M3.4 — Backup | ۱۴ | RTO < 2 ساعت؛ Recovery Test موفق |
| M3.5 — Production | ۱۵ | Security Audit passed؛ Load Test 20 users؛ مستندات کامل |

### ۷.۲ Quality Gate 2 (پایان ماه ۱۵ — تصمیم Production)

| # | معیار | حد قابل قبول | تصمیم‌گیرنده |
|---|--------|---------------|---------------|
| QG2.1 | Security Audit | بدون آسیب‌پذیری بحرانی | امنیت سازمان |
| QG2.2 | Load Test (۲۰ کاربر همزمان) | Uptime ≥ 99% | Backend Lead |
| QG2.3 | زمان پاسخ تحت بار | P95 ≤ 45 ثانیه | Backend Lead |
| QG2.4 | Rollback مدل آزمایش شده | موفق در < 30 دقیقه | Backend Lead |
| QG2.5 | دقت پاسخ نهایی | ≥ 80% | کارفرما |

**نتیجه Gate 2:** ✅ همه موفق → Production Release 🚀 | ⚠️ QG2.1 ناموفق → تعلیق تا رفع امنیتی.

---

## ۸. فاز ۴ — Optimization & Scale (ماه ۱۶+)

- DSPy Prompt Optimization؛ Fine-tuning Embedding فارسی؛ LangGraph Agent
- Horizontal Scaling؛ (اختیاری) GPU Roadmap؛ Index Versioning؛ Embedding Drift Detection

| ابزار | فاز ورود | هدف |
|-------|----------|-----|
| DSPy | M16–M17 | بهبود ۱۵–۳۰% کیفیت پاسخ |
| LangGraph | M17–M18 | Multi-step Agent |
| BGE-M3 Fine-tuned | M16+ | دقت Embedding اصطلاحات سازمانی |
| Kubernetes | در صورت نیاز | Horizontal Scale |

---

## ۹. لایه‌های معماری و تناظر با فازها

| لایه | فاز ۱ | فاز ۲ | فاز ۳ | فاز ۴ | ابزار کلیدی |
|------|-------|-------|-------|-------|--------------|
| Layer 1: Ingestion | ✅ | — | بهبود | — | Celery+Redis |
| Layer 2: NLP | ✅ | بهبود | — | Fine-tune | Hazm+ONNX |
| Layer 3: Embedding | ✅ پایه | بهبود | — | Fine-tune | E5/BGE-M3 |
| Layer 4: Hybrid Index | پایه | ✅ | — | Drift Det. | Qdrant+BM25 |
| Layer 5: RAG Orchestrator | — | ✅ | بهبود | Agent+DSPy | Haystack |
| Layer 6: API | — | ✅ | Security | — | FastAPI |
| Layer 7: Observability | Logging اولیه | — | ✅ | بهبود | Prometheus |

---

## ۱۰. تعریف «Done» برای هر سطح

- **Task:** کد + Unit Test (Coverage ≥ 70%) + Code Review + CI موفق  
- **Sprint:** همه Taskهای Sprint Done؛ Sprint Review؛ مستند به‌روز؛ بدون Bug بحرانی  
- **Milestone:** همه خروجی‌های اجباری موجود؛ Quality Check Milestone پاس؛ تأیید Tech Lead  
- **Gate:** همه معیارهای Quality Gate پاس؛ گزارش مکتوب؛ امضای تصمیم‌گیرنده  

---

## ۱۱. ریسک‌های کلان و ریسک هر Gate

### ۱۱.۱ ریسک‌های کلان (از SINA Roadmap v1.0)

| ریسک | احتمال | تأثیر | استراتژی کاهش |
|------|--------|-------|----------------|
| دقت NLP فارسی پایین | متوسط | بالا | Golden Query Set از ابتدا؛ Benchmark هر Sprint |
| CPU Bottleneck در Embedding | بالا | متوسط | Batch شبانه، Queue Priority، ONNX INT8 |
| نبود تخصص ML در Backend | بالا | بالا | Cross-training، مستندات، Pair Programming |
| API Breaking Changes | بالا | متوسط | Hexagonal Architecture |
| Disk/RAM Overflow | متوسط | بالا | Monitoring از فاز ۱، Retention Policy |
| مهاجرت Index در Production | کم | بالا | Zero-downtime Migration Plan |

### ۱۱.۲ اصل کلیدی مدیریت ریسک

در محیط Air-Gapped بزرگترین ریسک «ندانستن» است. **Observability Layer از فاز اول** (حتی ابتدایی) پیاده‌سازی شود و در هر Sprint یک Logging Checkpoint اضافه شود.

### ۱۱.۳ ریسک هر Gate (خلاصه)

| Gate | ریسک اصلی | پیشگیری |
|------|-----------|----------|
| Gate 0 | مدل/ONNX دیر می‌رسد | سفارش و آماده‌سازی قبل از Sprint 1 |
| Gate 1 | دقت < 75% | ارزیابی دستی هر Sprint؛ Golden Set |
| Gate 1 | کنترل دسترسی شکست | Security Test در Sprint مربوطه |
| Gate 2 | تیم IT آماده نیست | آموزش از فاز ۳؛ Runbook |
| Gate 2 | Security Audit ناموفق | Security Review مداوم |

---

## ۱۲. واژه‌نامه فنی (Glossary)

| اصطلاح | توضیح |
|--------|--------|
| RAG | Retrieval-Augmented Generation — ترکیب بازیابی اسناد با تولید متن LLM |
| Air-Gapped | محیط ایزوله از اینترنت؛ منابع Local |
| ONNX | فرمت استاندارد اجرای مدل ML روی CPU |
| GGUF | فرمت کوانتیزه LLM روی CPU با RAM بهینه |
| BM25 | جستجوی کلمات کلیدی با وزن فرکانسی |
| RRF | ادغام نتایج جستجوی Hybrid |
| ZWNJ | نیم‌فاصله فارسی؛ نیاز به Normalization |
| RBAC / ACL | کنترل دسترسی نقش‌محور / لیست دسترسی سند |
| Hexagonal Architecture | جداسازی Domain Logic از Infrastructure |

---

## ۱۳. خلاصه اجرایی

**SINA** در **فاز صفر (۴ هفته) + ۴ فاز اصلی (۱۸+ ماه)** با **Milestoneهای مشخص** و **۳ نقطه تصمیم کلیدی (Gate 0، Gate 1، Gate 2)** توسعه می‌یابد. محیط **CPU-Only و Air-Gapped** است؛ تمام معیارهای زمان و دقت با این فرض تعریف شده‌اند. ترکیب این سند از دو منبع تضمین می‌کند هم **محدودیت‌ها و معماری** شفاف باشند و هم **اجرا و حکمرانی** (Quality Gate، تعریف Done، ریسک هر Gate) قابل پیگیری باشند.

---

*مستند تلفیقی: SINA Roadmap Unified v1.0 | بهمن ۱۴۰۴ / فوریه ۲۰۲۶*
