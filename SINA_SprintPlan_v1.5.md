# SINA — Secure Intelligent Network Assistant

## برنامه Sprint و چرخه‌های Agile

### Agile Sprint Plan — Phase 0, 1 & 2

**هفته ۱ تا ۴۴ / فاز صفر + ماه ۱ تا ۱۱**

| مورد | مقدار |
|------|--------|
| نسخه مستند | 1.5 — هم‌راستا با SINA_Roadmap_v1.5 |
| تاریخ | بهمن ۱۴۰۴ / فوریه ۲۰۲۶ |
| متدولوژی | Scrum — Sprint دو هفته‌ای |
| پوشش | Phase 0 (S1–S2) + Phase 1 (S3–S12) + Phase 2 (S13–S22) |
| تیم | Backend/Infra + Frontend/UI (ML/DevOps/QA جاسازی‌شده) |
| مرجع اصلی | SINA_Roadmap_v1.5 — تمام Gate‌ها، تعریف Done و Milestone‌ها از نقشه راه |

---

## ۱. چارچوب Scrum در پروژه SINA

پروژه SINA از Scrum با Sprint‌های دو هفته‌ای پیروی می‌کند. با توجه به محیط Air-Gapped و تیم Backend-Centric، تطبیق‌های خاصی اعمال شده که در این بخش توضیح داده می‌شود.

### ۱.۱ ساختار Sprint

| رویداد | مدت | توضیح |
|--------|------|--------|
| Sprint Planning | روز اول — ۴ ساعت | تعریف Sprint Goal، انتخاب User Stories، تخمین Story Points |
| Daily Standup | هر روز — ۱۵ دقیقه | دیروز چه کردم؟ امروز چه می‌کنم؟ Blocker دارم؟ |
| Sprint Review | روز آخر — ۲ ساعت | Demo خروجی Sprint به تمام Stakeholderها |
| Sprint Retrospective | روز آخر — ۱.۵ ساعت | چه خوب بود؟ چه بهبود یابد؟ Action Item مشخص |
| Backlog Refinement | میانه Sprint — ۲ ساعت | پاکسازی و اولویت‌بندی User Stories Sprint بعدی |

### ۱.۲ تعریف Done — مطابق SINA_Roadmap_v1.5

این تعریف Done مستقیماً از بخش ۱۰ نقشه راه (سطح Task و Sprint) اخذ شده است:

| سطح | معیار | توضیح تکمیلی |
|-----|--------|----------------|
| Task | کد + Unit Test (≥70%) + Code Review + CI موفق | حداقل یک Reviewer غیر از نویسنده |
| Task | Integration Test در Docker Compose موفق | بدون دسترسی به اینترنت |
| Task | Logging مناسب — Audit Coverage 100% از Sprint 1 | هر دسترسی به سند باید ثبت شود |
| Task | مستند فنی: Docstring یا README بخش | برای Developer جدید قابل درک باشد |
| Sprint | همه Task‌ها Done؛ Sprint Review برگزار شده | بدون Bug بحرانی باز |
| Sprint | مستندات به‌روز شده؛ Backlog Refinement انجام شده | برای Sprint بعد آماده |

---

## ۲. نقش‌ها و مسئولیت‌ها

| نقش | مسئول | مسئولیت‌های کلیدی |
|-----|--------|-------------------|
| Product Owner | مدیر پروژه / کارفرما | اولویت‌بندی Backlog، تأیید Sprint Goal، تصمیم Gate 1 (QG1.1) |
| Scrum Master | ارشدترین Backend Dev | رفع Blocker، برگزاری Ceremonies، هماهنگی Gate‌ها |
| Tech Lead | Senior Backend Dev | تصمیم‌های معماری، تأیید Gate 0 (QG0.1، QG0.2، QG0.5) |
| Backend Lead | Backend Developer ارشد | Code Review، ML/AI Tasks، تأیید QG0.3، QG0.4، QG1.2، QG1.3 |
| Backend Dev(s) | Backend Developers | پیاده‌سازی APIs، Pipeline، Ingestion، Storage، NLP، Embedding |
| Frontend Dev(s) | Frontend Developers | UI Components، Chat Interface، Dashboard — فعال از S7 به بعد |
| QA (جاسازی‌شده) | هر Backend Dev | نوشتن Test، Acceptance Criteria، Golden Query Set |
| Security | Backend Lead / تیم امنیت | تأیید QG1.5 (Audit Log)، بررسی ACL |

---

## ۳. نگاشت فازها، Milestone‌ها و Gate‌ها

جدول زیر تناظر دقیق بین فازهای نقشه راه v1.5، Sprint‌ها، Milestone‌ها و نقاط Gate را نشان می‌دهد:

| فاز (نقشه راه) | Sprint‌ها | بازه زمانی | Milestone‌های نقشه راه | نقطه تصمیم |
|-----------------|----------|------------|------------------------|------------|
| Phase 0 — Foundation & Setup | S1–S2 | هفته ۱–۴ (پیش از ماه ۱) | M0.1 (هفته ۲)، M0.2 (هفته ۴) | Gate 0 (پایان S2) |
| Phase 1 — Foundation & Infrastructure | S3–S12 | ماه ۱–۶ (هفته ۵–۲۴) | M1.1→S3، M1.2a→S3-S4، M1.3→S3-S4، M1.4→S5-S6، M1.5→S7-S8، M1.2b→S9-S10، M1.6→S11-S12 | — |
| Phase 2 — Core RAG Engine | S13–S22 | ماه ۷–۱۱ (هفته ۲۵–۴۴) | M2.1→S13-S14، M2.2→S15-S16، M2.3→S17-S18، M2.4→S19-S20، M2.5→S21-S22، M2.6→S21-S22 | Gate 1 (پایان S22) |
| Phase 3 — Enterprise Hardening | S23–S32 | ماه ۱۲–۱۵ (هفته ۴۵–۶۴) | M3.1–M3.5 (Placeholder) | Gate 2 (پایان ماه ۱۵) |

- **Phase 0** خارج از شمارش ماه‌های اصلی است — ۴ هفته پیش از ماه ۱ انجام می‌شود. Phase 1 از ماه ۱ (هفته ۵) شروع می‌شود.
- **M1.2** به دو بخش تقسیم شده: **M1.2a** (Storage پایه در S3–S4) و **M1.2b** (Integration کامل + Data Quality در S9–S10).
- هیچ فازی بدون تأیید صریح Gate شروع نمی‌شود — مطابق نقشه راه v1.5.

---

## ۴. Phase 0 — Foundation & Setup (پیش از ماه ۱ / هفته ۱–۴)

Phase 0 خارج از شمارش ماه‌های اصلی پروژه است و به عنوان یک پیش‌نیاز اجباری پیش از شروع Phase 1 انجام می‌شود. هدف: تمام اعضای تیم روی همان Stack کار کنند؛ مدل‌ها روی CPU پاسخ دهند.

- **Phase 0 = S1–S2.** پس از Gate 0، Phase 1 از ماه ۱ (هفته ۵) شروع می‌شود — هیچ همپوشانی زمانی با Phase 1 وجود ندارد.

### Sprint 1–2: Dev Environment & Project Setup

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | محیط توسعه کامل آماده باشد — هر Developer بتواند روز اول کد بزند و مدل‌ها روی CPU پاسخ دهند |
| **بازه زمانی** | هفته ۱–۴ (پیش از ماه ۱) |
| **نقشه راه v1.5** | M0.1 (هفته ۲): Docker Compose، Gitea، PyPI Mirror آفلاین. M0.2 (هفته ۴): مدل GGUF + Embedding ONNX روی CPU، Qdrant، CI، ADR. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | راه‌اندازی Gitea self-hosted و Branch Strategy (main/develop/feature) | Backend | 3 | Push موفق، Branch Protection Rule فعال |
| 2 | ساخت Docker Compose اولیه (PostgreSQL، Redis، MinIO، Qdrant) | Backend | 5 | docker-compose up بدون خطا، health check تمام service‌ها |
| 3 | پیکربندی PyPI Mirror آفلاین و آرشیو Docker Images | Backend | 5 | نصب پکیج بدون اینترنت ممکن؛ image از tar.gz لود می‌شود |
| 4 | تعریف Database Schema اولیه (documents، chunks، audit_log) | Backend | 3 | Migration موفق؛ CRUD پایه تست شده؛ audit_log جدول آماده |
| 5 | ساخت CI Pipeline محلی (بدون اینترنت — local runner) | Backend | 3 | هر Push → Test Suite اجرا می‌شود، حداکثر ۵ دقیقه |
| 6 | تعریف Interface‌های اصلی (IDocumentRepo، IEmbeddingService، ILLMService) | Backend | 3 | Interface‌ها موجود؛ هیچ import مستقیم از ابزار خارجی در Domain Logic |
| 7 | بارگذاری مدل GGUF روی CPU — تست Hello World فارسی | Backend | 5 | مدل از /opt/models/llm لود می‌شود؛ پاسخ فارسی در کمتر از ۶۰ ثانیه |
| 8 | بارگذاری Embedding ONNX روی CPU — تست یک Batch کوچک | Backend | 5 | مدل از /opt/models/embedding لود؛ ۱۰ جمله فارسی embed در < ۱۰ ثانیه |
| 9 | مستند ADR نسخه ۱ و مستندسازی فرآیند HDD Update | Backend Lead | 2 | ADR در Git؛ فرآیند HDD Update یک بار end-to-end تست شده |

### Quality Gate 0 — مطابق SINA_Roadmap_v1.5 بخش ۴.۲

| # | معیار | حد قابل قبول | تصمیم‌گیرنده |
|---|--------|---------------|---------------|
| QG0.1 | همه Container در Docker Compose بالا می‌آیند | 100% بدون خطا | Tech Lead |
| QG0.2 | مدل GGUF یک سوال فارسی روی CPU پاسخ می‌دهد | پاسخ فارسی در < ۶۰ ثانیه | Tech Lead |
| QG0.3 | Embedding ONNX روی CPU اجرا می‌شود | ۱۰ chunk در < ۱۰ ثانیه | Backend Lead |
| QG0.4 | نصب آفلاین از PyPI Mirror کار می‌کند | بدون نیاز به اینترنت | Backend Lead |
| QG0.5 | CI Pipeline در هر Push اجرا می‌شود | حداکثر ۵ دقیقه | Tech Lead |

**نتیجه:** ✅ همه موفق → Phase 1 از ماه ۱ (هفته ۵) شروع | ⚠️ ۱–۲ مورد ناموفق → تمدید تا ۱ هفته | ❌ بیش از ۲ مورد → بازبینی Stack. در صورت عدم عبور Gate 0، Phase 1 (Sprint 3) شروع نشود.

---

## ۵. Phase 1 — Foundation & Infrastructure (ماه ۱–۶ / Sprint 3–12)

Phase 1 از ماه ۱ (هفته ۵) شروع می‌شود — بلافاصله پس از تأیید Gate 0. این فاز ۱۰ Sprint (S3–S12) دارد. هدف: پایه‌های فنی محکم تا رسیدن به E2E Alpha اولیه.

- **M1.2** به دو بخش تقسیم شده: **M1.2a** (Storage پایه — S3–S4) و **M1.2b** (Integration کامل + Data Quality — S9–S10). این تقسیم از نقشه راه v1.5 بخش ۵.۲ برگرفته شده.

---

### Sprint 3–4: Ingestion Layer (M1.1 + M1.2a + M1.3)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | فایل PDF/DOCX فارسی آپلود شود، hash بخورد، scan شود و در Queue قرار گیرد؛ Storage پایه آماده باشد |
| **بازه زمانی** | هفته ۵–۸ (ماه ۱–۲) |
| **نقشه راه v1.5** | M1.1: Docker Compose healthy. M1.2a: MinIO bucket، PostgreSQL schema، Qdrant collection؛ ذخیره/بازیابی ساده موفق. M1.3: PDF/DOCX → hash → scan → Queue. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | راه‌اندازی MinIO Bucket و PostgreSQL Schema (documents, chunks, audit_log) | Backend | 3 | Bucket آماده؛ Schema migration موفق؛ CRUD تست شده |
| 2 | راه‌اندازی Qdrant Collection و ذخیره/بازیابی یک Vector آزمایشی | Backend | 3 | Collection ایجاد؛ یک بردار ذخیره و بازیابی موفق |
| 3 | پیاده‌سازی File Upload Endpoint با MIME Validation | Backend | 3 | فقط PDF/DOCX قبول می‌شود؛ فایل در MinIO ذخیره می‌شود |
| 4 | SHA-256 Hashing و Idempotency Check | Backend | 3 | فایل تکراری → لینک قبلی برمی‌گردد؛ پردازش تکراری نمی‌شود |
| 5 | اتصال ClamAV برای Offline Virus Scan | Backend | 5 | فایل آلوده → Quarantine؛ فایل سالم → Queue؛ ثبت در audit_log |
| 6 | پیاده‌سازی Task Queue با Celery + Redis | Backend | 5 | Task ارسال، پردازش، نتیجه در PostgreSQL ثبت می‌شود |
| 7 | Dead Letter Queue برای خطاها | Backend | 3 | پس از ۳ Retry → DLQ؛ ثبت با جزئیات در audit_log |
| 8 | پیاده‌سازی Directory Watcher با Watchdog | Backend | 3 | فایل جدید در پوشه watched → خودکار به Queue اضافه می‌شود |

---

### Sprint 5–6: Persian NLP Pipeline (M1.4)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | متن فارسی از فایل خام استخراج، نرمال‌سازی و تقسیم‌بندی معنادار شود |
| **بازه زمانی** | هفته ۹–۱۲ (ماه ۳) |
| **نقشه راه v1.5** | M1.4: متن نرمال‌سازی، ZWNJ حل شده، Chunk‌های معنادار تولید می‌شوند. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | پیاده‌سازی Format Router (PDF متنی vs اسکن‌شده) | Backend | 3 | تشخیص خودکار نوع فایل؛ routing به parser مناسب |
| 2 | استخراج متن با PyMuPDF + pdfplumber | Backend | 5 | متن فارسی صحیح استخراج؛ جداول preserve شده |
| 3 | پیاده‌سازی EnterprisePersianNormalizer (Hazm + DadmaTools) | Backend | 5 | ZWNJ، ی/ک عربی-فارسی، اعداد — تست با ۱۰۰ جمله نمونه |
| 4 | پیاده‌سازی PersianTextSplitter (Chunk-aware RTL) | Backend | 5 | جملات فارسی از وسط نمی‌شکنند؛ Overlap رعایت می‌شود |
| 5 | تست Chunking با Golden Dataset فارسی (۵۰۰ صفحه) | Backend/QA | 3 | < 5% Chunk نامعنادار؛ نتایج در PostgreSQL ثبت می‌شوند |
| 6 | ذخیره Chunk‌ها در PostgreSQL با metadata کامل | Backend | 3 | هر Chunk با doc_id، position، lang، page_num ذخیره می‌شود |

---

### Sprint 7–8: Embedding Service (M1.5) + Frontend شروع

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | Chunk‌های فارسی به بردار تبدیل و در Qdrant ذخیره شوند؛ تیم Frontend کار را آغاز کند |
| **بازه زمانی** | هفته ۱۳–۱۶ (ماه ۴) |
| **نقشه راه v1.5** | M1.5: مدل ONNX لود، Batch Embedding روی CPU < 5 ثانیه برای ۱۰ chunk. Frontend: شروع Component‌های پایه UI. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | بارگذاری مدل multilingual-e5-base (ONNX INT8) از /opt/models | Backend | 5 | مدل لود بدون اینترنت؛ SHA-256 تأیید شده |
| 2 | پیاده‌سازی INT8 Quantization Pipeline | Backend | 5 | سرعت > 2x نسبت به FP32؛ دقت < 2% افت |
| 3 | Batch Embedding Service با Adaptive Batch Size | Backend | 5 | ۱۰ Chunk در < ۵ ثانیه روی CPU 8-core؛ Batch تطبیقی با RAM |
| 4 | اتصال Qdrant — ذخیره Vector + Payload (lang, acl, doc_id, model_ver) | Backend | 3 | بردار + metadata در Collection ذخیره و بازیابی موفق |
| 5 | Version Registry برای مدل Embedding در PostgreSQL | Backend | 3 | هر بردار با model_version tag شده؛ قابل Re-embed |
| 6 | Embedding Worker در Celery Pipeline | Backend | 3 | Async؛ Retry خودکار؛ ثبت در audit_log |
| 7 | [Frontend] ساخت Project Structure و Design System پایه | Frontend | 3 | پروژه React/Vue initialized؛ Component library اولیه |
| 8 | [Frontend] پیاده‌سازی File Upload UI و نمایش وضعیت Ingestion | Frontend | 5 | Upload فایل؛ نمایش Progress؛ خطاها نمایش داده می‌شوند |

---

### Sprint 9–10: Storage Integration & Data Quality (M1.2b)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | تمام لایه‌های Storage یکپارچه کار کنند؛ Data Quality و Lineage تضمین شود |
| **بازه زمانی** | هفته ۱۷–۲۰ (ماه ۵) |
| **نقشه راه v1.5** | M1.2b: تکمیل Integration Test کامل Storage + Data Quality. این بخش دوم M1.2 است — پایه آن در S3–S4 (M1.2a) آماده شد. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | پیاده‌سازی Deduplication (SHA-256 exact + Cosine > 0.95 → flag) | Backend | 5 | فایل تکراری flag می‌شود؛ پردازش مجدد نمی‌شود |
| 2 | Index Version Registry در PostgreSQL | Backend | 3 | جدول index_versions با model_hash، build_date، status |
| 3 | Tombstone Strategy برای حذف اسناد (deleted_at + Qdrant propagate) | Backend | 3 | deleted_at flag؛ background job Vector را از Qdrant حذف می‌کند |
| 4 | MinIO Bucket Policy و Versioning (Retention 90 روز) | Backend | 3 | Bucket versioned؛ Object قدیمی‌تر از ۹۰ روز auto-expire |
| 5 | Data Lineage Tracking (Raw → Normalized → Embedded) | Backend | 5 | هر Chunk قابل trace تا source file اصلی است |
| 6 | Integration Test Suite کامل Storage Layer (≥ 50 Test) | Backend/QA | 3 | Coverage > 80%؛ تمام 50 Test موفق؛ بدون خطای بحرانی |
| 7 | [Frontend] پیاده‌سازی Document List و وضعیت ایندکس‌گذاری | Frontend | 3 | لیست فایل‌های آپلودشده؛ وضعیت هر فایل (pending/done/error) |
| 8 | [Frontend] طراحی Chat Interface اولیه (بدون Backend اتصال) | Frontend | 3 | UI اولیه Chat قابل نمایش؛ Mock Data برای Preview |

---

### Sprint 11–12: Phase 1 Alpha — E2E Test (M1.6)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | تست E2E کامل: فایل فارسی وارد → پردازش → ذخیره → Query اولیه جواب دهد |
| **بازه زمانی** | هفته ۲۱–۲۴ (ماه ۶) |
| **نقشه راه v1.5** | M1.6: فایل فارسی → embed → Qdrant → query اولیه جواب دهد. نقشه راه این را پایان Phase 1 می‌داند. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | Query Endpoint اولیه (Vector Search فقط) | Backend | 5 | سوال فارسی → بردار → Qdrant → Top-5 Chunk برمی‌گردد |
| 2 | E2E Test Suite با ۲۰ سند فارسی واقعی (≥ ۱۰۰ صفحه) | Backend/QA | 5 | Pipeline کامل در < ۲ دقیقه برای سند ۱۰۰ صفحه |
| 3 | Performance Profiling روی CPU — شناسایی Bottleneck | Backend | 3 | Bottleneck مستند شده؛ زمان هر مرحله ثبت در Prometheus |
| 4 | Logging اولیه و Error Tracking (همه خطاها با stack trace) | Backend | 3 | هر خطا در Loki ذخیره؛ قابل جستجو |
| 5 | مستندات فنی Phase 1 (README، API Docs، Setup Guide) | Backend | 3 | Developer جدید می‌تواند در ۲ ساعت محیط را راه‌اندازی کند |
| 6 | [Frontend] اتصال Chat UI به Query Endpoint اولیه | Frontend | 5 | سوال فارسی ارسال؛ Top-5 Chunk نمایش داده می‌شود |
| 7 | Demo آماده‌سازی Phase 1 Review برای Stakeholders | همه | 2 | Demo ۱۵ دقیقه‌ای آماده؛ Slides تهیه شده |

---

## ۶. Phase 2 — Core RAG Engine (ماه ۷–۱۱ / Sprint 13–22)

Phase 2 بلافاصله پس از پایان Phase 1 شروع می‌شود. ۱۰ Sprint (S13–S22) دارد. هدف: موتور RAG کامل با Hybrid Search، LLM روی CPU، API Layer و Beta Release.

- **Frontend** از این فاز به صورت موازی فعال است — هر Sprint حداقل یک Task Frontend دارد.
- پس از S22 ارزیابی **Gate 1** انجام می‌شود — مطابق نقشه راه v1.5 بخش ۶.۴.

---

### Sprint 13–14: BM25 & Keyword Search (M2.1)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | جستجوی کلمات کلیدی دقیق برای اصطلاحات، اعداد و شناسه‌های فارسی کار کند |
| **بازه زمانی** | هفته ۲۵–۲۸ (ماه ۷) |
| **نقشه راه v1.5** | M2.1: Keyword Search با Persian Analyzer؛ Recall@10 > 80% روی Golden Set. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | راه‌اندازی Whoosh BM25 با Persian Analyzer | Backend | 5 | Indexing ۱۰۰۰ Chunk در < ۳۰ ثانیه روی CPU |
| 2 | پیاده‌سازی Persian Stemmer در BM25 Index | Backend | 5 | کاهش Index Size 20–30%؛ Recall بهبود یافته |
| 3 | Stopword List فارسی سازمانی (۲۰۰+ کلمه) | Backend | 3 | لیست در Git؛ قابل توسعه توسط تیم Domain |
| 4 | Inverted Index با ZWNJ-aware Tokenizer | Backend | 5 | «نیم‌فاصله» و «نیمفاصله» هر دو یک نتیجه برمی‌گردانند |
| 5 | Benchmark مقایسه BM25 vs Vector روی Golden Set فارسی | Backend/QA | 3 | گزارش Precision/Recall در PostgreSQL ثبت؛ Recall@10 > 80% |
| 6 | [Frontend] Dashboard جستجو — نمایش نتایج BM25 و Vector جداگانه | Frontend | 5 | دو ستون نتایج؛ امتیاز هر نتیجه نمایش داده می‌شود |

---

### Sprint 15–16: Hybrid Search & RRF Fusion (M2.2)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | RRF Fusion کارکند — نتایج Hybrid بهتر از هر روش منفرد باشد |
| **بازه زمانی** | هفته ۲۹–۳۲ (ماه ۸) |
| **نقشه راه v1.5** | M2.2: RRF Fusion؛ MRR Hybrid > MRR Vector-only روی Golden Set. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | پیاده‌سازی RRF Fusion Engine (k=60) | Backend | 5 | فرمول RRF صحیح؛ امتیاز نهایی ترتیب منطقی دارد |
| 2 | Query Planner — تشخیص نوع Query (semantic/keyword/hybrid) | Backend | 5 | سوال با شماره → keyword weight بیشتر؛ سوال معنایی → vector weight بیشتر |
| 3 | Parallel Search (Vector + BM25 همزمان با asyncio) | Backend | 3 | Latency کاهش ≥ 30% نسبت به Sequential |
| 4 | Pre-filter با ACL و Metadata قبل از جستجو | Backend | 3 | فقط Document‌های مجاز (با ACL کاربر) در نتایج |
| 5 | Golden Query Set Evaluation فاز ۲ (۱۰۰ سوال فارسی) | Backend/QA | 3 | MRR Hybrid > MRR Vector در Golden Set؛ نتایج مستند |
| 6 | [Frontend] نمایش نتایج Hybrid و نشانگر منبع هر نتیجه | Frontend | 3 | Source Document و Page Number در هر نتیجه |

---

### Sprint 17–18: LLM Integration — Llama.cpp (M2.3)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | مدل LLM روی CPU لود شود و پاسخ فارسی منسجم تولید کند |
| **بازه زمانی** | هفته ۳۳–۳۶ (ماه ۸–۹) |
| **نقشه راه v1.5** | M2.3: Llama.cpp GGUF روی CPU؛ > 8 token/sec؛ پاسخ فارسی منسجم. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | نصب و پیکربندی Llama.cpp برای CPU (Thread = Physical Cores) | Backend | 5 | > 8 token/sec روی CPU 8-core؛ Hyper-threading غیرفعال |
| 2 | LangChain Adapter پشت ILLMService Interface | Backend | 5 | Domain Logic هیچ import مستقیم از Llama.cpp ندارد |
| 3 | Persian Prompt Template (System Prompt + Context Assembly) | Backend | 3 | System Prompt فارسی؛ Context در ترتیب امتیاز؛ Citation در پاسخ |
| 4 | Fallback Score Threshold (Score < 0.65 → 'یافت نشد') | Backend | 3 | سوال با Score پایین → بدون ارسال به LLM → پیام مناسب |
| 5 | SHA-256 Verification مدل GGUF در هر بارگذاری | Backend | 2 | اگر Hash مطابقت ندارد → خطا؛ ثبت در audit_log |
| 6 | [Frontend] نمایش Fallback Message در UI هنگام 'یافت نشد' | Frontend | 3 | پیام فارسی مناسب؛ پیشنهاد بازنویسی سوال |

---

### Sprint 19–20: RAG Orchestrator — Haystack (M2.4)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | Pipeline کامل RAG: Query → Normalize → Embed → Hybrid Search → Rerank → LLM → Response |
| **بازه زمانی** | هفته ۳۷–۴۰ (ماه ۹–۱۰) |
| **نقشه راه v1.5** | M2.4: Query → Normalize → Embed → Hybrid → Rerank → LLM → Response. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | پیاده‌سازی Haystack Pipeline (DAG صریح — هر Node مستقل) | Backend | 5 | Pipeline قابل trace کامل؛ هر Node لاگ جداگانه دارد |
| 2 | Cross-Encoder Re-ranker روی CPU (Top-10 → Top-3) | Backend | 5 | Re-ranking در < ۲ ثانیه؛ کیفیت نتایج بهبود یافته |
| 3 | Query Normalization و Persian Query Expansion (دیکشنری local) | Backend | 3 | کوئری normalize؛ synonym expansion با دیکشنری سازمانی |
| 4 | Context Assembly با Window Strategy (Prompt < 4096 token) | Backend | 3 | مرتبط‌ترین Chunk‌ها اول؛ Prompt Size کنترل می‌شود |
| 5 | Pipeline Test Suite با Mock Components (Unit + Integration) | Backend/QA | 3 | Unit Test هر Node؛ Integration Test کل Pipeline موفق |
| 6 | [Frontend] نمایش مسیر پاسخ (از کدام سند، صفحه چند، امتیاز چقدر) | Frontend | 5 | Citation پایین هر پاسخ؛ Link به سند اصلی |

---

### Sprint 21–22: API Layer + Phase 2 Beta (M2.5 + M2.6)

| مورد | مقدار |
|------|--------|
| **Sprint Goal** | API Layer با SSE Streaming کارکند — Beta Release داخلی آماده باشد |
| **بازه زمانی** | هفته ۴۱–۴۴ (ماه ۱۰–۱۱) |
| **نقشه راه v1.5** | M2.5: REST، SSE، JWT، Swagger. M2.6: Recall@5 > 75%، Latency E2E < 30 sec روی CPU، ۱۰ کاربر همزمان. |

| # | User Story / Task | تیم | SP | Acceptance Criteria |
|---|-------------------|-----|-----|---------------------|
| 1 | FastAPI REST Endpoints (Query، Ingest، Status، Health) | Backend | 5 | Swagger/OpenAPI docs؛ تمام Endpoints test شده |
| 2 | SSE Streaming برای LLM Generation | Backend | 5 | کاربر کلمه‌به‌کلمه پاسخ می‌بیند؛ قطعی اتصال مدیریت می‌شود |
| 3 | JWT Authentication + Rate Limiting (10 req/min per user) | Backend | 3 | درخواست بدون Token رد؛ Rate Limit با HTTP 429 |
| 4 | Load Test — ۱۰ کاربر همزمان با Locust | Backend/QA | 3 | E2E Latency < 45 sec؛ بدون Crash؛ CPU < 85% |
| 5 | Audit Logging کامل — 100% Query‌ها ثبت (QG1.5) | Backend | 3 | هر Query با user_id، timestamp، doc_accessed ثبت؛ قابل Export |
| 6 | [Frontend] Chat UI کامل با SSE Streaming | Frontend | 5 | پاسخ Streaming؛ نمایش Citation؛ History چند مکالمه |
| 7 | [Frontend] صفحه Admin — آپلود، وضعیت ایندکس، آمار | Frontend | 3 | Admin می‌تواند فایل آپلود و وضعیت ایندکس را ببیند |
| 8 | Phase 2 Beta Demo و Release Notes | همه | 2 | Demo کامل؛ Known Issues ثبت؛ Stakeholders تأیید کردند |

### Quality Gate 1 — مطابق SINA_Roadmap_v1.5 بخش ۶.۴

| # | معیار | حد قابل قبول | تصمیم‌گیرنده |
|---|--------|---------------|---------------|
| QG1.1 | دقت پاسخ روی سوالات تعریف‌شده | ≥ 75% | Product Owner |
| QG1.2 | زمان پاسخ P95 روی CPU | ≤ 30 ثانیه | Backend Lead |
| QG1.3 | پوشش اسناد ایندکس‌شده | ≥ 1000 فایل | Backend Lead |
| QG1.4 | Recall جستجو روی Golden Set | ≥ 70% | Tech Lead |
| QG1.5 | کنترل دسترسی و Audit Log | 100% query‌ها ثبت | Security |

**نتیجه:** ✅ همه موفق → Phase 3 (Enterprise Hardening) شروع | ⚠️ QG1.1 یا QG1.2 ناموفق → تمدید ۲ Sprint | ❌ QG1.5 ناموفق → توقف کامل، بازبینی امنیتی.

---

## ۷. Product Backlog — فاز ۳ و ۴ (Placeholder)

آیتم‌های زیر در Backlog هستند و پس از Gate 1 در Sprint Planning فازهای بعدی تفصیل می‌یابند.

### ۷.۱ فاز ۳ — Enterprise Hardening (ماه ۱۲–۱۵ / S23–S32)

| Milestone نقشه راه | ماه | خروجی کلیدی (Definition of Done) |
|-------------------|-----|----------------------------------|
| M3.1 — Security (RBAC + ACL) | ۱۲ | هر درخواست بدون Token رد؛ ACL در سطح Document اعمال می‌شود |
| M3.2 — Audit Logging | ۱۲ | هر دسترسی به سند ثبت؛ گزارش ۳۰ روزه قابل Export |
| M3.3 — Observability | ۱۳ | Grafana با ۱۰ metric کلیدی؛ Alert برای CPU > 80% |
| M3.4 — Backup & Recovery | ۱۴ | RTO < 2 ساعت؛ Recovery Test موفق در Staging |
| M3.5 — Production Release v1.0 | ۱۵ | Security Audit passed؛ Load Test 20 users؛ مستندات کامل |

**Gate 2 (پایان ماه ۱۵):** QG2.1 Security Audit، QG2.2 Load Test 20 کاربر، QG2.3 P95 ≤ 45 sec، QG2.4 Rollback مدل، QG2.5 دقت ≥ 80%. تصمیم‌گیرنده نهایی: کارفرما. ✅ همه موفق → Production Release 🚀

### ۷.۲ فاز ۴ — Optimization & Scale (ماه ۱۶+)

| ابزار / هدف | فاز ورود (نقشه راه) | هدف |
|-------------|---------------------|-----|
| DSPy Prompt Optimization | M16–M17 | بهبود ۱۵–۳۰% کیفیت پاسخ بدون تغییر معماری |
| LangGraph Multi-step Agent | M17–M18 | سوالات پیچیده چندمرحله‌ای |
| BGE-M3 Fine-tuned (فارسی سازمانی) | M16+ | دقت Embedding اصطلاحات تخصصی |
| Kubernetes (Horizontal Scale) | در صورت نیاز | Scale افقی Worker Node بدون Downtime |
| Embedding Drift Detection | M16+ | KS-Test ماهانه؛ Trigger Re-embedding |

### ۷.۳ Velocity Baseline

| معیار | تخمین اولیه | توضیح |
|-------|-------------|--------|
| Velocity هر Sprint | ۳۰–۴۵ Story Points | بسته به تعداد Developer فعال |
| Capacity هر Developer | ۶–۸ SP در Sprint | احتساب Meeting‌ها و Overhead |
| Buffer برای ریسک فنی ML | ۲۰% Capacity | ML/AI Tasks Uncertainty بالا دارند |
| Spike Story | حداکثر ۱ در Sprint | برای Research/PoC؛ Time-boxed ۱ روز |
| Frontend Capacity | ۱۵–۲۰% کل Velocity | از S7 به بعد؛ موازی با Backend |

---

*مستند: SINA Sprint Plan v1.2 — هم‌راستا با SINA_Roadmap_v1.5 | بهمن ۱۴۰۴ / فوریه ۲۰۲۶*
