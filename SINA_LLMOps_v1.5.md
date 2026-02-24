# SINA — Secure Intelligent Network Assistant

## LLMOps / MLOps Framework

### استقرار، نگهداری و نظارت مدل‌های AI در محیط Air-Gapped

| مورد | مقدار |
|------|--------|
| نسخه | 1.5 — Draft |
| تاریخ | بهمن ۱۴۰۴ / فوریه ۲۰۲۶ |
| محیط | Air-Gapped / CPU-Only / آفلاین کامل |
| مخاطب | Backend Team / ML Engineers / DevOps |
| مرجع | هم‌راستا با **SINA_Roadmap_v1.5**، **SINA_SprintPlan** و **SINA_RiskQA**؛ مسیر Model Vault، معیارهای کیفیت و Observability با نقشه راه و برنامه Sprint یکسان است. |

---

## ۱. مقدمه — LLMOps در محیط Air-Gapped

LLMOps (Large Language Model Operations) مجموعه‌ای از فرآیندها، ابزارها و best practiceها است که چرخه حیات مدل‌های زبانی را از انتخاب تا استقرار، نظارت و به‌روزرسانی مدیریت می‌کند.

در محیط Air-Gapped پروژه SINA، این چالش‌ها به شدت تشدید می‌شوند:

- هیچ دسترسی به HuggingFace Hub، Weights & Biases، یا هیچ سرویس ابری وجود ندارد
- به‌روزرسانی مدل‌ها نیاز به فرآیند Manual Transfer دارد (مطابق نقشه راه: Local Model Registry، Manual Update Pipeline، فرآیند HDD Update)
- تمام ابزارهای Monitoring باید Local اجرا شوند
- Versioning و Registry باید به صورت Self-hosted پیاده‌سازی شود

### ۱.۱ چرخه حیات مدل در SINA

| مرحله | نام | توضیح در محیط Air-Gapped |
|-------|-----|---------------------------|
| 1 | Model Selection & Import | انتخاب مدل در محیط آنلاین، دانلود با Hash تأیید، انتقال به Air-Gapped Vault |
| 2 | Validation & Registration | اعتبارسنجی SHA-256، ثبت در Local Model Registry، Tag با version و metadata |
| 3 | Optimization (ONNX/GGUF) | تبدیل به فرمت بهینه CPU، Quantization INT8، Benchmark قبل از استقرار |
| 4 | Staging Deployment | استقرار در محیط Staging، Golden Query Test، Performance Validation |
| 5 | Production Deployment | Zero-downtime Rollout، Alias Switching، Rollback Plan آماده (مطابق Gate 2 نقشه راه: QG2.4) |
| 6 | Monitoring & Drift Detection | نظارت مستمر Offline، Embedding Drift، Quality Metrics |
| 7 | Retirement / Update | فرآیند کنترل‌شده Deprecation، Re-embedding با مدل جدید |

---

## ۲. Local Model Vault — مخزن مدل‌های آفلاین

Model Vault یک ساختار پوشه‌ای استاندارد شده در سرور است که تمام مدل‌های AI سیستم SINA را نگهداری می‌کند. این Vault جایگزین کامل HuggingFace Hub در محیط Air-Gapped است. *در برنامه Sprint (Phase 0) مسیر `/opt/models/llm` و `/opt/models/embedding` برای لود مدل استفاده می‌شود؛ می‌توان آن‌ها را به همین ساختار زیر `/opt/sina/models/` نگاشت کرد.*

### ۲.۱ ساختار پوشه‌ای Model Vault

```
/opt/sina/models/
├── embedding/
│   ├── multilingual-e5-base-onnx-int8/
│   │   └── model.onnx | tokenizer.json | config.json | metadata.json
│   └── bge-m3-onnx-int8/          # فاز ۴ — مطابق نقشه راه
├── llm/
│   ├── llama-3-8b-instruct-q4_k_m.gguf
│   └── mistral-7b-instruct-q4_k_m.gguf   # (جایگزین)
├── reranker/
│   └── cross-encoder-ms-marco-minilm-onnx/
├── nlp/
│   ├── hazm-models/
│   ├── dadmatools-models/         # مطابق نقشه راه: Hazm + DadmaTools
│   └── stanza-fa/
└── registry/
    ├── model_registry.json
    └── checksums.sha256
```

### ۲.۲ ساختار metadata.json برای هر مدل

هر مدل باید یک فایل `metadata.json` داشته باشد:

| فیلد | نمونه مقدار | توضیح |
|------|-------------|--------|
| model_id | e5-base-int8-v2.1 | شناسه یکتا در Registry |
| model_name | multilingual-e5-base | نام اصلی مدل |
| version | 2.1.0 | نسخه Semantic (Major.Minor.Patch) |
| format | onnx-int8 | فرمت: onnx-fp32 / onnx-int8 / gguf-q4 |
| sha256_hash | a3f7...b92c | هش کنترل یکپارچگی |
| import_date | 2026-02-22 | تاریخ انتقال به Vault |
| source_url | hf://intfloat/e5... | منبع اصلی (برای audit) |
| dimensions | 768 | ابعاد بردار خروجی |
| max_tokens | 512 | حداکثر طول ورودی |
| languages | ['fa', 'en'] | زبان‌های پشتیبانی‌شده |
| benchmark_recall | 0.84 | نتیجه Golden Query Set |
| status | active | active / staging / deprecated |

### ۲.۳ فرآیند Import مدل جدید (Air-Gapped)

1. **دانلود در محیط آنلاین:** دانلود مدل با huggingface-cli، محاسبه SHA-256  
2. **انتقال امن:** کپی به USB/Drive رمزنگاری‌شده، انتقال به شبکه ایزوله  
3. **اعتبارسنجی:** مقایسه SHA-256 با مقدار اعلام‌شده در منبع  
4. **Optimization:** اجرای ONNX Export و INT8 Quantization  
5. **Benchmark:** اجرای Golden Query Set روی مدل جدید  
6. **Registration:** افزودن به model_registry.json و ثبت در PostgreSQL  
7. **Staging Deploy:** استقرار در Staging و تأیید نهایی  

*مطابق برنامه Sprint (Phase 0): فرآیند HDD Update مستند و یک بار end-to-end تست شده است.*

---

## ۳. Model Versioning & Registry

سیستم Versioning مدل‌های SINA بر اساس Semantic Versioning و با ذخیره‌سازی در PostgreSQL پیاده‌سازی می‌شود. این سیستم جایگزین MLflow در محیط Air-Gapped است.

### ۳.۱ Schema جدول model_registry

| ستون | نوع داده | توضیح |
|------|----------|--------|
| id | UUID PK | شناسه یکتا |
| model_id | VARCHAR(100) UNIQUE | شناسه کوتاه (e.g., e5-base-int8-v2.1) |
| model_type | ENUM | embedding / llm / reranker / nlp |
| version | VARCHAR(20) | Semantic Version (2.1.0) |
| format | VARCHAR(20) | onnx-int8 / gguf-q4 / ... |
| file_path | TEXT | مسیر کامل در /opt/sina/models/ |
| sha256_hash | CHAR(64) | هش یکپارچگی فایل |
| dimensions | INTEGER | برای مدل‌های Embedding |
| benchmark_recall | FLOAT | نتیجه آخرین ارزیابی |
| benchmark_date | TIMESTAMP | تاریخ آخرین ارزیابی |
| status | ENUM | staging / active / deprecated / retired |
| deployed_at | TIMESTAMP | تاریخ استقرار Production |
| created_by | VARCHAR(100) | کاربر ثبت‌کننده (Audit) |
| notes | TEXT | یادداشت‌های migration و breaking changes |

### ۳.۲ استراتژی Migration ایندکس

هر بار که مدل Embedding تغییر کند، تمام Vectorهای ذخیره‌شده باید Re-embed شوند. فرآیند Zero-Downtime به صورت زیر است (مطابق ریسک R-010 در RiskQA و نقشه راه):

1. **ایجاد Collection جدید** در Qdrant با prefix v{version}  
2. **Background Re-embedding** در Low-Priority Workers (شبانه)  
3. **A/B Validation:** ۱۰% Queryها به Index جدید، مقایسه MRR  
4. **Atomic Cutover:** تغییر active_model_id در PostgreSQL  
5. **Grace Period:** نگهداری Index قدیمی ۳۰ روز  
6. **Cleanup:** حذف Index قدیمی پس از تأیید  

---

## ۴. Deployment Pipeline در محیط Air-Gapped

پروژه SINA از Docker Compose برای استقرار Single-Node استفاده می‌کند. تمام Image‌ها به صورت tar.gz در Vault نگهداری می‌شوند. *مطابق نقشه راه و برنامه Sprint: محیط‌های Dev، Staging و Production با Gateهای مشخص.*

### ۴.۱ محیط‌های استقرار

| محیط | هدف | ابزار | تأیید قبل از Promote |
|------|-----|--------|------------------------|
| Development | توسعه روزانه | Docker Compose (Local) | Unit Tests موفق |
| Staging | تست یکپارچه‌سازی | Docker Compose (Staging Server) | Integration Tests + Golden Query Set |
| Production | محیط واقعی | Docker Compose (Production Server) | Manual Approval + Load Test (Gate 2: QG2.2) |

### ۴.۲ Checklist استقرار Production

قبل از هر استقرار Production، این Checklist باید تکمیل شود (هم‌خوان با Quality Gate 2 نقشه راه):

| # | آیتم | مسئول | وضعیت |
|---|------|--------|--------|
| 1 | Golden Query Set با نتایج مورد انتظار اجرا شده | Backend Lead | ☐ تأیید |
| 2 | SHA-256 تمام مدل‌ها تأیید شده | Backend Dev | ☐ تأیید |
| 3 | Backup کامل از PostgreSQL و Qdrant تهیه شده | Backend Dev | ☐ تأیید |
| 4 | Rollback Plan مستند و تست شده (QG2.4) | Backend Lead | ☐ تأیید |
| 5 | Load Test با ۲۰ کاربر همزمان موفق (QG2.2) | QA | ☐ تأیید |
| 6 | Audit Logging فعال و تست شده (100% از Sprint 1) | Backend Dev | ☐ تأیید |
| 7 | Monitoring Dashboard Active | Backend Dev | ☐ تأیید |
| 8 | مستندات Release Notes تکمیل شده | Scrum Master | ☐ تأیید |
| 9 | Product Owner تأیید نهایی داده | Product Owner | ☐ تأیید |

---

## ۵. Monitoring & Observability (آفلاین)

در محیط Air-Gapped، Monitoring Stack کاملاً Local است. *نقشه راه: Observability Layer از فاز ۱ (حتی ابتدایی)؛ فاز ۳: Prometheus + Grafana + Loki + Jaeger. RiskQA: Prometheus Alert از Sprint 1.*

### ۵.۱ Stack Monitoring

| ابزار | نقش | پیکربندی کلیدی |
|-------|-----|-----------------|
| Prometheus | جمع‌آوری Metrics | Scrape هر ۱۵ ثانیه، Retention 90 روز، Export به CSV |
| Grafana | Dashboard نمایش | Local Docker، بدون Cloud، Dashboard از JSON import |
| Loki | Log Aggregation | LogQL queries، فیلتر فارسی، Rotate 30 روزه |
| Jaeger | Distributed Tracing | Trace کامل هر Request از API تا LLM |
| Prometheus Alertmanager | Alerting Local | Email/Webhook داخلی، بدون PagerDuty |

### ۵.۲ Metricsهای کلیدی SINA

*آستانه‌ها با Quality Gateهای نقشه راه و NFR در RiskQA هم‌خوان هستند.*

| Metric | نوع | آستانه Alert | توضیح |
|--------|-----|--------------|--------|
| sina_query_latency_seconds | Histogram | > 60s | زمان پاسخ E2E از API تا Generation (هدف Gate 1: ≤ 30s) |
| sina_embedding_latency_seconds | Histogram | > 10s | زمان Embed یک Chunk |
| sina_retrieval_recall_at5 | Gauge | < 0.70 | دقت بازیابی در Golden Set (حداقل نقشه راه: > 70%) |
| sina_cpu_usage_percent | Gauge | > 85% | مصرف CPU سرور |
| sina_ram_usage_percent | Gauge | > 90% | مصرف RAM سرور |
| sina_ingestion_queue_size | Gauge | > 500 | تعداد Task در Queue |
| sina_vector_drift_score | Gauge | > 0.10 | میزان Drift ایندکس برداری |
| sina_llm_tokens_per_second | Gauge | < 5 | سرعت تولید متن LLM (هدف Sprint: > 8 token/sec روی CPU) |
| sina_failed_tasks_total | Counter | > 50/hr | تعداد Task شکست‌خورده |
| sina_audit_events_total | Counter | — | تعداد رویدادهای Audit (فقط مانیتورینگ) |

---

## ۶. Embedding Drift Detection

در محیط Air-Gapped، Embedding Drift Detection به صورت Batch Offline انجام می‌شود. Drift یعنی توزیع بردارهای ذخیره‌شده به تدریج از توزیع مورد انتظار فاصله گرفته — نشانه نیاز به Re-embedding. *مطابق RiskQA (R-013) و نقشه راه فاز ۴: Embedding Drift Detection و Continuous Evaluation.*

### ۶.۱ انواع Drift در SINA

- **Data Drift:** تغییر در نوع یا زبان اسناد ورودی  
- **Model Drift:** تفاوت بین نسخه‌های مدل Embedding  
- **Concept Drift:** تغییر معنایی اصطلاحات سازمانی با گذر زمان  
- **Linguistic Drift:** تغییر در سبک نوشتاری یا فارسی رسمی  

### ۶.۲ فرآیند Detection

| فرکانس | روش | اقدام |
|--------|-----|--------|
| هر Sprint (۲ هفته) | Golden Query Recall@5 | اگر افت > 3% → بررسی فوری |
| ماهانه | KS-Test روی Vector Distribution | اگر p-value < 0.05 → Drift تأیید‌شده |
| سه‌ماهه | Centroid Distance Analysis | اگر Persian Cluster Shift > 10% → Re-embedding |
| هر تغییر مدل | A/B Benchmark کامل | Recall جدید باید > Recall قدیمی باشد |

---

## ۷. Backup & Disaster Recovery

در محیط Air-Gapped، Backup باید کاملاً Offline و بدون وابستگی به سرویس ابری باشد. استراتژی SINA بر اساس اصل **3-2-1** (3 نسخه، 2 رسانه مختلف، 1 خارج از سایت) طراحی شده. *RTO/RPO با نقشه راه فاز ۳ (M3.4: RTO < 2 ساعت برای Metadata) و RiskQA هم‌خوان است.*

### ۷.۱ RTO/RPO Targets

| Component | RPO (حداکثر از دست دادن داده) | RTO (زمان بازیابی) | اولویت |
|-----------|--------------------------------|---------------------|--------|
| PostgreSQL (Metadata) | ۱ ساعت | < ۲ ساعت | Critical |
| MinIO (Raw Files) | ۲۴ ساعت | < ۴ ساعت | High |
| Qdrant (Vector Index) | ۴۸ ساعت | < ۲۴ ساعت | Medium |
| Model Vault | N/A (ثابت) | < ۱ ساعت | High |
| Configs & Secrets | Real-time | < ۳۰ دقیقه | Critical |

### ۷.۲ Backup Schedule

- **روزانه (ساعت ۲ شب):** PostgreSQL dump + MinIO incremental sync  
- **هفتگی:** Qdrant snapshot + کل Model Vault به Drive رمزنگاری‌شده  
- **ماهانه:** Full Backup + Disaster Recovery Test در محیط Staging  
- **هر تغییر کد:** Config backup خودکار به Git (private, air-gapped)  

---

## ۸. Continuous Evaluation — ارزیابی مستمر

ارزیابی مستمر در SINA از یک **Golden Query Set** استاندارد استفاده می‌کند که در ابتدای پروژه تعریف شده و در هر Sprint اجرا می‌شود. *مطابق نقشه راه و RiskQA: Golden Query Set از Sprint 1 تعریف می‌شود؛ Recall@5 و معیارهای کیفیت با Gate 1 و NFR یکسان هستند.*

### ۸.۱ ساختار Golden Query Set

- ۱۰۰ سوال فارسی از دامنه‌های مختلف سازمانی  
- ۳۰ سوال با اصطلاحات تخصصی (شناسه‌ها، کدها، شماره‌ها)  
- ۲۰ سوال چندمفهومی (نیاز به ترکیب چند سند)  
- ۲۰ سوال با کلمات نرمال‌سازی‌نشده (ZWNJ، ی/ک عربی)  
- ۱۵ سوال انگلیسی یا ترکیبی فارسی-انگلیسی  
- ۱۵ سوال edge case (پاسخ در سیستم نیست — باید 'یافت نشد' برگرداند)  

### ۸.۲ معیارهای ارزیابی و آستانه‌ها

*هم‌خوان با Quality Gate 1 (QG1.1، QG1.2، QG1.4) و NFR در RiskQA.*

| معیار | آستانه Fail | هدف | توضیح |
|-------|-------------|-----|--------|
| Recall@5 | < 70% | > 85% | درصد سوالات که پاسخ درست در Top-5 است (Gate 1: ≥ 75%) |
| MRR@10 | < 0.65 | > 0.80 | میانگین رتبه معکوس در Top-10 |
| NDCG@5 | < 0.60 | > 0.75 | دقت با وزن‌دهی رتبه |
| Hallucination Rate | > 20% | < 8% | درصد پاسخ‌های غیرواقعی — ارزیابی دستی |
| Not-Found Precision | < 80% | > 95% | وقتی پاسخ نیست، درستی تشخیص 'یافت نشد' (Fallback Score < 0.65) |
| E2E Latency P95 | > 90s | < 30s | صدک ۹۵ زمان پاسخ کامل (هدف نقشه راه: ≤ 30 ثانیه) |

### ۸.۳ فرآیند Regression Gate

در هر Sprint، قبل از Merge به branch develop، این فرآیند اجرا می‌شود:

1. اجرای Golden Query Set به صورت خودکار (CI بدون اینترنت)  
2. مقایسه نتایج با Baseline آخرین Sprint موفق  
3. اگر هر Metric بیش از ۳% افت کرده باشد → Merge مسدود می‌شود  
4. تحلیل دستی و رفع مشکل قبل از Merge  
5. ثبت نتایج در جدول evaluation_history در PostgreSQL  

---

*مستند: SINA LLMOps v1.0 — Draft | هم‌راستا با SINA_Roadmap_v1.5، SINA_SprintPlan و SINA_RiskQA | بهمن ۱۴۰۴ / فوریه ۲۰۲۶*
