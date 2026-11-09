Version: 1.0
Updated: ۱۴۰۴/۰۸/۱۶ (2026-11-07)

# خلاصه گفت‌وگو: آشنایی با Data Lake و افزودن آن به پروژه
## offline-enterprise-ai-infrastructure-blueprint

**تاریخ شروع گفت‌وگو:** اکتبر ۲۰۲۶  
**هدف:** درک مفهوم Data Lake و بررسی نحوه یکپارچه‌سازی آن با معماری هفت‌لایه موجود پروژه

---

## ۱. مقدمه و تعریف اولیه Data Lake

**Data Lake (دریاچه داده)** یک مخزن مرکزی و مقیاس‌پذیر است که داده‌ها را در شکل خام و اصلی خود (Structured، Semi-structured و Unstructured) ذخیره می‌کند.

### تفاوت با مفاهیم نزدیک

| مفهوم | نوع داده | ساختاردهی | کاربرد اصلی |
|-------|----------|-----------|-------------|
| Data Lake | خام و متنوع | Schema-on-Read | ذخیره و آماده‌سازی برای AI/ML و تحلیل |
| Data Warehouse | ساختاریافته | Schema-on-Write | گزارش‌گیری و BI |
| Data Lakehouse | ترکیبی | ترکیبی | هم تحلیل و هم ML پیشرفته |

### کاربرد در هوش مصنوعی
- نگهداری حجم بالای داده‌های متنوع برای آموزش و RAG
- انعطاف‌پذیری بالا برای فرمت‌های مختلف
- مناسب برای داده‌های شرکتی و شخصی در محیط On-premise

---

## ۲. نیازمندی‌های پروژه کاربر

- **نوع داده:** اسناد Word، Excel، PDF + دیتابیس‌های نرم‌افزارهای سازمانی
- **هدف اصلی:** RAG و استفاده با مدل‌های آماده
- **زیرساخت:** کاملاً On-premise (Air-Gapped)
- **حساسیت داده:** اطلاعات شرکتی و شخصی ← نیاز به امنیت و کنترل دسترسی بالا

---

## ۳. معماری پیشنهادی اولیه (قبل از بررسی ریپو)

### اجزای اصلی پیشنهادی On-premise

| لایه | ابزار پیشنهادی | نقش |
|------|----------------|-----|
| ذخیره‌سازی خام (Data Lake) | MinIO | ذخیره فایل‌ها و خروجی دیتابیس‌ها |
| استخراج اسناد | Unstructured + PyMuPDF + ... | استخراج متن و جداول |
| Vector Database | Qdrant یا Milvus | ذخیره Embedding برای RAG |
| چارچوب RAG | LlamaIndex یا LangChain | مدیریت بازیابی و تولید |
| سرویس‌دهی مدل | vLLM یا Ollama | اجرای مدل‌های آماده |
| هویت و دسترسی | Keycloak | احراز هویت و RBAC |

### نکات امنیتی کلیدی
- رمزنگاری در حال انتقال و سکون
- جداسازی Collectionها بر اساس دپارتمان
- اصل حداقل دسترسی
- Audit Log کامل
- مدیریت اسرار با Vault

---

## ۴. ذخیره داده‌های دیتابیسی در Data Lake

### روش استاندارد
1. استخراج داده از دیتابیس‌های سازمانی (Full یا Incremental)
2. تبدیل به فرمت **Parquet**
3. ذخیره در MinIO با ساختار Partitioned

### ساختار پوشه‌بندی پیشنهادی
```text
company-data/
└── databases/
    ├── erp/
    │   ├── customers/
    │   │   └── year=2025/month=10/
    │   ├── orders/
    │   └── products/
    ├── crm/
    └── hr/
```

### بهترین روش‌ها
- **Partitioning:** بر اساس تاریخ + منبع داده
- **فشرده‌سازی:** zstd یا snappy
- **Incremental Load:** اولویت نسبت به Full Load
- **مدیریت Schema:** ترجیحاً ثابت یا با پشتیبانی Schema Evolution
- **نام‌گذاری منظم** و ثبت متادیتا

### قابلیت SQL روی Object Storage
- بله، با ابزارهایی مثل DuckDB، Trino، Spark
- در بلندمدت توصیه به استفاده از Apache Iceberg روی MinIO

---

## ۵. مدیریت روابط بین جداول و Entity-Centric Documents

### رویکردهای ممکن
1. نگه‌داشتن Normalized (جداول جدا)
2. Denormalization (تخت کردن)
3. ساختار Nested در Parquet
4. **ساخت Entityهای کسب‌وکاری (توصیه برای RAG)**

### توصیه نهایی برای RAG
- ساخت **سندهای غنی (Rich Documents)** حول موجودیت‌های اصلی
- موجودیت‌های اصلی معمولاً: مشتری، درخواست/سفارش، محصول
- اطلاعات مرتبط داخل همان سند قرار می‌گیرد تا کیفیت بازیابی و پاسخ بالاتر برود

### معیارهای انتخاب موجودیت اصلی
- میزان پرسش کاربران
- نقطه شروع طبیعی جستجو
- اهمیت کسب‌وکاری
- قرار گرفتن در سمت «یک» روابط یک‌به‌چند
- نیاز به زمینه کامل برای پاسخ‌دهی

---

## ۶. بررسی ریپوزیتوری موجود

ریپوزیتوری: `offline-enterprise-ai-infrastructure-blueprint`

### نقاط قوت
- معماری ۷ لایه تمیز و اصولی
- تمرکز عالی روی محیط آفلاین و CPU-first
- پشتیبانی قوی از زبان فارسی (نرمال‌سازی، Chunking، Hybrid Search)
- مستندسازی نسبتاً کامل

### شکاف‌های شناسایی‌شده نسبت به گفت‌وگو
1. نبود تعریف صریح Data Lake — **حل شد: لایه Foundation در معماری ۷ لایه**
2. پوشش ضعیف داده‌های ساختاریافته (دیتابیس‌ها) — **در حال پیاده‌سازی: Partitioned Parquet در Processed Zone**
3. نبود رویکرد Entity-Centric Documents — **Spike در Sprint 5-6 (SINA_SprintPlan_v1.5)**
4. امنیت و کنترل دسترسی قابل تقویت — **MinIO IAM per zone در Sprint 3-4؛ Keycloak در Phase 3**
5. حاکمیت داده (Catalog و Lineage) قابل بهبود — **PostgreSQL Catalog در Phase 1؛ Lineage در Sprint 9-10**
6. نبود قابلیت Lakehouse / SQL روی داده‌های ذخیره‌شده — **DuckDB/Trino PoC در Sprint 5-6؛ Iceberg در Phase 3**

---

## ۷. جایگذاری Data Lake در معماری ۷ لایه

### لایه‌های فعلی پروژه
1. Ingestion / Gatekeeper
2. Processing / Refinery
3. Embedding / Semantic Translator
4. Hybrid Index / Memory
5. RAG Orchestrator
6. API / Interface
7. Observability / Watchtower

### تصمیم معماری
Data Lake به‌عنوان **لایه بنیادین مستقل (Foundational Layer: Data Lake)** در نظر گرفته شد که زیر تمام لایه‌های معماری (۱ تا ۷) قرار می‌گیرد و نه زیرمجموعه لایه Storage. لایه‌های بالاتر (Ingestion, Processing, Embedding, Hybrid Index, RAG Orchestration, API, Observability) از Data Lake استفاده می‌کنند (consumer) و Data Lake منبع حقیقت (Source of Truth) است.

```text
[ لایه ۷: Observability ]
[ لایه ۶: API ]
[ لایه ۵: RAG Orchestrator ]
[ لایه ۴: Hybrid Index ]
[ لایه ۳: Embedding ]
[ لایه ۲: Processing ]
[ لایه ۱: Ingestion ]
────────────────────────────────
[ Foundational Layer: Data Lake ]
   ├── Raw Zone
   ├── Processed Zone
   └── Curated / Entity Zone
```

Data Lake لایه بنیادین مستقل است و لایه‌های بالای آن مصرف‌کننده آن هستند. تمام ایندکس‌ها (Vector + BM25) از روی Data Lake قابل بازسازی هستند (Rebuild-from-source). جزئیات Zones، Partitioning، Entity-Centric، Catalog و ملاحظات Persian-First فقط در این فایل (SSOT) نگهداری می‌شود.

---

## ۸. رابطه Data Lake با سایر لایه‌ها

### مناطق داخلی پیشنهادی Data Lake
- **Raw Zone:** فایل‌های اصلی + خروجی خام دیتابیس
- **Processed Zone:** متن تمیز + Parquet
- **Curated / Entity Zone:** سندهای غنی موجودیت‌ها

### جریان ورودی و خروجی

| لایه | ورودی به Data Lake | خروجی از Data Lake |
|------|---------------------|---------------------|
| ۱ - Ingestion | فایل خام + خروجی دیتابیس | - |
| ۲ - Processing | خواندن از Raw Zone | نوشتن متن، Parquet و Entity |
| ۳ - Embedding | خواندن Chunk و Entity | معمولاً ندارد |
| ۴ - Hybrid Index | خواندن متن و متادیتا | معمولاً ندارد |
| ۷ - Observability | متادیتا و Lineage | اطلاعات Audit |

**اصل مهم:** Data Lake منبع حقیقت (Source of Truth) است و ایندکس‌های Vector و BM25 از روی آن قابل بازسازی هستند (Rebuild-from-source).

---

## ۹. ابزارهای پیاده‌سازی Data Lake

### آیا ابزار واحد کافی است؟
**خیر.** Data Lake از ترکیب چند ابزار تشکیل می‌شود.

### پشته پیشنهادی (سازگار با محدودیت‌های پروژه)

| نقش | ابزار پیشنهادی | توضیح |
|-----|----------------|------|
| Object Storage | **MinIO** | هسته اصلی Data Lake |
| فرمت ساختاریافته | Parquet (+ بعداً Iceberg) | ذخیره بهینه جداول |
| موتور SQL | DuckDB (شروع) یا Trino | امکان کوئری روی داده‌ها |
| کاتالوگ متادیتا | PostgreSQL یا Hive Metastore | مدیریت Schema و کشف داده |
| امنیت | MinIO IAM + Keycloak | کنترل دسترسی |
| ارکستراسیون | صف موجود (RabbitMQ/Redis) | هماهنگی با معماری فعلی |

### استراتژی پیاده‌سازی مرحله‌ای
1. **شروع ساده:** MinIO + Parquet + DuckDB
2. **بلوغ:** افزودن Apache Iceberg + کاتالوگ
3. **حاکمیت کامل:** Lineage قوی + سیاست‌های دسترسی پیشرفته

---

## ۱۰. وضعیت فعلی تصمیم‌گیری

- [x] تعریف Data Lake و کاربرد آن مشخص شد
- [x] جایگذاری به‌عنوان لایه بنیادین مستقل (Foundational Layer: Data Lake) تأیید شد
- [x] رابطه با لایه‌های دیگر Clarified شد
- [x] ابزارهای پیشنهادی مشخص شد
- [x] ساختار Buckets (Raw/Processed/Curated) + Partitioning Convention در Sprint 3-4
- [x] جزئیات Pipeline داده‌های دیتابیسی (Parquet + Partitioning) در Sprint 3-4
- [x] نحوه یکپارچه‌سازی Entity-Centric Documents — **Spike در Sprint 5-6**
- [ ] به‌روزرسانی فایل‌های مستندات پروژه — **در حال انجام**
- [ ] MinIO IAM Policies per zone — **Sprint 3-4**
- [ ] Catalog قرار (PostgreSQL به عنوان Metadata Catalog در Phase 1؛ Hive Metastore/Iceberg در Phase 3)
- [ ] Data Lineage Tracking — **Sprint 9-10**
- [ ] Lakehouse évolution (Apache Iceberg) — **Phase 3**

---

## ۱۱. ملاحظات Persian-First در Data Lake

### ۱۱.۱ Encoding و Filename Handling
- تمام نام‌های فایل و مسیرهای MinIO باید UTF-8 باشند
- Container/OS level: `LANG=C.UTF-8` در Docker Compose برای جلوگیری از corruption نام فایل‌های RTL
- MinIO Console و API از UTF-8 native پشتیبانی می‌کنند — نیاز به config اضافه نیست

### ۱۱.۲ Normalization در Pipeline (Raw → Processed)
- **ZWNJ (U+200C) Unification:** پیش از ذخیره در Processed Zone، تمام نیم‌فاصله‌ها یکپارچه شوند (حذف یا تبدیل به space استاندارد)
- **ی/ک عربی → فارسی:** Mapping table برای تبدیل کدپوینت‌های عربی به فارسی (U+06CC → U+06A9، U+064A → U+06A9)
- **اعداد:** اعداد عربی/هندی → فارسی/انگلیسی (پایین‌ریزی به context)
- **NFKC Normalization:** اعمال روی کل متن پیش از Chunking و Embedding

### ۱۱.۳ Partitioning با درک زبان
- Partition Keyها باید language-aware باشند: `lang=fa` به علاوه `date=`
- برای داده‌های mixed: `lang=mixed` + sub-partition بر اساس language detection per row

### ۱۱.۴ Entity Document در Curated Zone
- Entity Documents باید **Rich Persian Documents** باشند:
  - متن کامل موجودیت با نرمال‌سازی کامل
  - متادیتای زبان (`lang: 'fa'`) و جهت (`dir: 'rtl'`)
  - Filters جستجو: ACL، entity_type، business_key
- برای RAG: Entity Documents مستقیماً به عنوان context در LLM Prompt inject می‌شوند

### ۱۱.۵ Catalog و Metadata
- PostgreSQL Catalog: ستون `lang` و `script_direction` در تمام جداول
- Full-text Search در Catalog: استفاده از Persian Stemmer (Hazm/DadmaTools) برای discoverability موجودیت‌ها

---

## ۱۲. تصمیم Catalog: PostgreSQL vs Hive Metastore

**تصمیم Phase 1: PostgreSQL به عنوان Metadata Catalog**
- **علت:** هم‌اکنون PostgreSQL برای Metadata اسناد وجود دارد؛ اضافه کردن جداول Catalog (entities، partitions، schemas) بدون dependency جدید امکان‌پذیر است
- **Schema Catalog در PostgreSQL:**
  ```sql
  CREATE TABLE lake_schemas (
      id UUID PRIMARY KEY,
      zone TEXT, -- raw/processed/curated
      source TEXT, -- erp/crm/hr/manual
      schema_json JSONB, -- Parquet schema (fields, types)
      partition_keys TEXT[], -- e.g., ['date', 'source']
      created_at TIMESTAMP,
      version INTEGER
  );
  CREATE TABLE lake_partitions (
      id UUID PRIMARY KEY,
      schema_id UUID REFERENCES lake_schemas,
      partition_values JSONB, -- e.g., {"date": "2025-10", "source": "erp"}
      path TEXT, -- MinIO path
      row_count BIGINT,
      size_bytes BIGINT,
      created_at TIMESTAMP
  );
  ```
- **Migration Path به Phase 3:** وقتی Volume و Concurrency بالا رفت، به **Apache Iceberg + Hive Metastore (या Nessie)** migrate می‌کنیم. PostgreSQL Catalog داده‌ها را به صورت Iceberg Tables expose می‌کند (via Trino/DuckDB).

---

## ۱۳. گام‌های بعدی پیشنهادی (به‌روزرسانی شده)

1. **Sprint 3-4:** پیاده‌سازی Buckets (Raw/Processed/Curated) + Partitioning Convention + MinIO IAM per zone
2. **Sprint 5-6:** Spike Entity-Centric Pipeline (تحلیل موجودیت‌ها، Schema طراحی، PoC DuckDB → Curated)
3. **Sprint 9-10:** Data Lineage Tracking (Raw → Normalized → Embedded → Entity) + Integration Test کامل Storage
4. **Phase 3:** Apache Iceberg روی MinIO + Hive Metastore/Nessie برای Lakehouse کامل
5. به‌روزرسانی تدریجی فایل‌های معماری پروژه (در حال انجام)

---

*این سند خلاصه‌ای از گفت‌وگوهای انجام‌شده تا تاریخ ۹ نوامبر ۲۰۲۶ است و مبنای ادامه کار برای یکپارچه‌سازی Data Lake با معماری هفت‌لایه پروژه قرار می‌گیرد.*
