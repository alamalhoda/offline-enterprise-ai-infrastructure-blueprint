
# معماری پلتفرم هوش مصنوعی سازمانی آفلاین (Enterprise Offline AI Architecture)

### مقدمه و فلسفه طراحی

معماری پیشنهادی برای این اکوسیستم، از الگوی **«معماری لایه‌ای مدولار» (Modular Layered Architecture)** پیروی می‌کند. برخلاف راه‌حل‌های یکپارچه (Monolithic) که در آن‌ها تغییر یک بخش منجر به بازنویسی کل سیستم می‌شود، این طراحی بر اساس اصل **«تفكیک دغدغه‌ها» (Separation of Concerns)** بنا شده است.

در محیط‌های ایزوله (Air-gapped) که دسترسی به منابع ابری و دیباگ آنلاین وجود ندارد، پایداری و قابلیت اطمینان (Reliability) اولویت اول است. این معماری به گونه‌ای مهندسی شده که جریان داده را از لحظه ورود فایل تا استخراج دانش، در یک خط لوله (Pipeline) کنترل‌شده هدایت می‌کند. هر لایه به عنوان یک "جعبه سیاه" با ورودی و خروجی مشخص عمل می‌کند، که پیچیدگی‌های داخلی را از سایر لایه‌ها مخفی نگه می‌دارد.

### اصول کلیدی و مزایای معماری

این طراحی سه مزیت رقابتی عمده برای سازمان به همراه دارد:

#### ۱. اتصال سست و ماژولار بودن (Loose Coupling & Modularity)

در دنیای هوش مصنوعی، مدل‌ها و تکنولوژی‌ها با سرعت نور تغییر می‌کنند.

* **مزیت:** این معماری به ما اجازه می‌دهد اجزا را بدون تخریب کل سیستم تعویض کنیم.
* **مثال:** اگر فردا مدل `Llama-3` با مدل قوی‌تر `Mistral` جایگزین شود، یا اگر بخواهیم موتور OCR را از `Tesseract` به `PaddleOCR` تغییر دهیم، تنها کافیست «لایه پردازش» یا «ارکستراتور» را به‌روزرسانی کنیم. لایه‌های دیتابیس، API و رابط کاربری هیچ تغییری نخواهند کرد. این یعنی **چابکی در عین پایداری**.

#### ۲. مقیاس‌پذیری افقی (Horizontal Scalability)

با توجه به محدودیت استفاده از CPU، گلوگاه اصلی سیستم پردازش سنگین فایل‌هاست.

* **مزیت:** معماری مبتنی بر صف (Queue-based) در لایه‌های Ingestion و Processing به ما اجازه می‌دهد بار ترافیک را مدیریت کنیم.
* **روش کار:** اگر تعداد اسناد ورودی از ۱۰۰ به ۱۰,۰۰۰ برسد، نیازی به ارتقای سخت‌افزاری سرور اصلی (Vertical Scaling) نیست. ما می‌توانیم تعداد "Worker"های لایه پردازش را افزایش دهیم تا روی هسته‌های CPU بیشتری به صورت موازی کار کنند. سیستم بدون قطعی (Downtime) مقیاس‌پذیر می‌شود.

#### ۳. رویت‌پذیری و حاکمیت داده (Observability & Data Governance)

در یک سیستم آفلاین، "ندانستن" بزرگترین دشمن است.

* **مزیت:** لایه اختصاصی Observability مانند یک "جعبه سیاه هواپیما" عمل می‌کند.
* **کارکرد:** ما دقیقاً می‌دانیم کدام فایل در چه مرحله‌ای گیر کرده است، کدام کاربر چه سوالی پرسیده و دقت پاسخ‌ها چقدر است. همچنین، مکانیسم‌های Audit Log تضمین می‌کنند که تمام دسترسی‌ها طبق پروتکل‌های امنیتی سازمان ثبت می‌شوند که برای محیط‌های Enterprise حیاتی است.

---

### نمای شماتیک لایه‌ها (Architectural Blueprint)

این نمودار جریان منطقی و فیزیکی داده‌ها را در ۷ لایه مصوب نمایش می‌دهد:

```mermaid
graph TD
    %% Define Styles
    classDef layer fill:#f9f9f9,stroke:#333,stroke-width:2px,rx:5,ry:5;
    classDef db fill:#e1f5fe,stroke:#0277bd,stroke-width:2px;
    classDef obs fill:#fff3e0,stroke:#ff6f00,stroke-width:2px,stroke-dasharray: 5 5;

    subgraph "External World (Users & Systems)"
        User[Admin / End User]
        ExtApp[3rd Party Apps]
    end

    subgraph "Layer 7: Observability & Governance (Cross-Cutting)"
        Logger[Audit Logs & Tracing]
        Monitor[Resource Monitor]
    end

    subgraph "Layer 6: API Layer (Gateway)"
        API[REST / gRPC Interface]
        Auth[Auth & Rate Limiting]
    end

    subgraph "Layer 1: Ingestion Layer"
        Upload[File Receiver]
        Validator[Sanitization & Deduplication]
        Queue[Message Queue (RabbitMQ/Redis)]
    end

    subgraph "Layer 2: Processing & NLP Layer (CPU Optimized)"
        Router[Format Router]
        OCR[OCR Engine]
        Norm[Persian Normalizer]
        Chunk[Semantic Chunker]
    end

    subgraph "Layer 3: Embedding Layer"
        Embed[Embedding Model (ONNX)]
    end

    subgraph "Layer 4: Hybrid Index Layer"
        VecDB[(Vector DB - Qdrant)]
        KwdDB[(Keyword DB - BM25)]
        MetaDB[(SQL Metadata)]
    end

    subgraph "Layer 5: RAG Orchestrator"
        Fusion[RRF Fusion & Re-ranking]
        Gen[LLM Generation (Llama/Gemma)]
        Context[Context Builder]
    end

    %% Flow Connections
    User --> API
    ExtApp --> API
    API --> Upload
    API <--> Context
  
    Upload --> Validator
    Validator --> Queue
    Queue --> Router
  
    Router --> OCR
    Router --> Norm
    OCR --> Norm
    Norm --> Chunk
    Chunk --> Embed
  
    Embed --> VecDB
    Chunk -- Text --> KwdDB
  
    Context --> Fusion
    Fusion <--> VecDB
    Fusion <--> KwdDB
    Fusion --> Gen
    Gen --> API

    %% Observability Connections (Conceptual)
    API -.-> Logger
    Queue -.-> Monitor
    Gen -.-> Logger

    %% Apply Styles
    class Logger,Monitor obs;
    class VecDB,KwdDB,MetaDB db;
```

### توضیح جریان در نمودار:

1. **جریان سمت چپ (Ingestion):** داده‌ها از بالا وارد شده، تمیز می‌شوند، در صف قرار می‌گیرند، پردازش شده و در نهایت به دیتابیس (لایه ۴) می‌رسند.
2. **جریان سمت راست/مرکز (Retrieval):** درخواست کاربر از API به **RAG Orchestrator** می‌رسد، ارکستراتور با لایه دیتابیس صحبت می‌کند (Hybrid Search) و سپس پاسخ نهایی را تولید و بازمی‌گرداند.
3. **پوشش سراسری (Observability):** لایه نظارت (کادر نارنجی فرضی) بر تمام این تراکنش‌ها نظارت دارد.

1. **Ingestion Layer** (لایه دریافت و ورود داده)
2. **Processing & NLP Layer** (لایه پردازش و NLP)
3. **Embedding Layer** (لایه امبدینگ / بردارسازی)
4. **Hybrid Index Layer** (لایه ایندکس ترکیبی)
5. **RAG Orchestrator** (ارکستراتور RAG)
6. **API Layer** (لایه رابط برنامه‌نویسی)
7. **Observability & Governance** (لایه نظارت و حاکمیت)

### ۱. لایه دریافت و ورود داده (Ingestion Layer)

**نقش:** دروازه‌بان سیستم (The Gatekeeper)
این لایه نقطه تماس اولیه با دنیای بیرون است و مسئولیت مدیریت جریان ورودی را بر عهده دارد تا سیستم زیر بار ترافیک یا فایل‌های معیوب دچار اختلال نشود.

* **وظایف کلیدی:**
  * **Validation & Sanitization:** بررسی نوع فایل (MIME type check) و اطمینان از امن بودن فایل (Malware scan اولیه).
  * **Idempotency & Deduplication:** محاسبه هش فایل (SHA-256) قبل از پردازش. اگر فایل قبلاً آپلود شده باشد، بلافاصله لینک آن بازگردانده می‌شود و پردازش تکراری انجام نمی‌شود (صرفه‌جویی در CPU).
  * **Queue Management:** ارسال درخواست‌ها به صف‌های پردازش (مثل RabbitMQ یا Redis) برای مدیریت Load Balancing و جلوگیری از Back-pressure.

### ۲. لایه پردازش و NLP (Processing & NLP Layer)

**نقش:** پالایشگاه داده (The Refinery)
حیاتی‌ترین بخش برای زبان فارسی. در این لایه، داده‌های خام (Raw Data) به متون تمیز و ساختاریافته تبدیل می‌شوند.

* **وظایف کلیدی:**
  * **Extraction Strategy:** استفاده از روتر هوشمند؛ اگر فایل متنی است از کتابخانه‌های سریع (مثل PyMuPDF) و اگر اسکن شده است از OCR (مثل Tesseract یا PaddleOCR) استفاده می‌کند.
  * **Persian Normalization:**
    * یکسان‌سازی کاراکترها (ک/ی فارسی vs عربی).
    * مدیریت نیم‌فاصله‌ها (ZWNJ) با کتابخانه‌هایی مثل Hazm یا Dadmatools.
    * حذف کاراکترهای کنترلی و Noise Removal.
  * **Advanced Chunking:** تقسیم متن به قطعات کوچک (Chunks). به جای برش ساده، از استراتژی **Recursive Character Splitting** یا **Semantic Chunking** استفاده می‌شود تا جملات فارسی در وسط قطع نشوند.

### ۳. لایه امبدینگ (Embedding Layer)

**نقش:** مترجم معنایی (The Semantic Translator)
این لایه متن تمیز شده را به زبان ریاضی (بردارها) ترجمه می‌کند. از آنجا که GPU نداریم، این لایه باید به شدت بهینه باشد.

* **وظایف کلیدی:**
  * **Model Selection:** استفاده از مدل‌های چندزبانه سبک و قدرتمند (مثل `intfloat/multilingual-e5-base` یا `BGE-M3`).
  * **Optimization:** اجرای مدل‌ها با فرمت **ONNX** و استفاده از **Quantization (int8)** برای افزایش سرعت پردازش روی CPU تا ۳ برابر.
  * **Batch Processing:** تجمیع چندین Chunk و ارسال یکباره آن‌ها به مدل برای کاهش سربار پردازشی (Overhead).

### ۴. لایه ایندکس ترکیبی (Hybrid Index Layer)

**نقش:** حافظه سیستم (The Memory)
قلب تپنده معماری شما. اینجا جایی است که نقاط ضعف Vector Search با دقت Keyword Search پوشش داده می‌شود.

* **وظایف کلیدی:**
  * **Vector Store:** ذخیره بردارهای تولید شده (استفاده از Qdrant یا Milvus). از ایندکس‌های **HNSW** برای جستجوی سریع استفاده می‌شود.
  * **Inverted Index (BM25):** ذخیره کلمات کلیدی متن برای جستجوی دقیق (Exact Match). بسیار حیاتی برای اصطلاحات خاص سازمانی، شماره نامه‌ها و اسامی خاص فارسی.
  * **Metadata Storage:** نگهداری اطلاعات جانبی (نام فایل، صفحه، تاریخ ایجاد) در یک دیتابیس سبک (مثل SQLite یا PostgreSQL) برای فیلترینگ (Metadata Filtering).

### ۵. ارکستراتور RAG (RAG Orchestrator)

**نقش:** مغز متفکر (The Brain)
این لایه تصمیم می‌گیرد چگونه به سوال کاربر پاسخ دهد. اینجاست که "هوش" واقعی اتفاق می‌افتد.

* **وظایف کلیدی:**
  * **Query Transformation:** بازنویسی سوال کاربر (Re-writing) برای بهبود جستجو.
  * **Hybrid Search Execution:** اجرای همزمان جستجو در لایه وکتور و لایه BM25.
  * **Re-ranking (RRF):** ادغام نتایج دو جستجو با الگوریتم **Reciprocal Rank Fusion** برای رسیدن به بهترین اسناد.
  * **Context Assembly:** ساختن پرامپت نهایی برای LLM (ترکیب دستورالعمل سیستم + سوال کاربر + اسناد بازیابی شده).
  * **Generation:** ارسال پرامپت به مدل زبانی (LLM) لوکال (مثل Llama-3-Persian نسخه GGUF) و تولید پاسخ.

### ۶. لایه API (API Layer)

**نقش:** رابط ارتباطی (The Interface)
این لایه سرویس‌ها را در اختیار کلاینت‌ها (Web UI, Mobile App, 3rd Party Apps) قرار می‌دهد.

* **وظایف کلیدی:**
  * **Protocol Support:** ارائه API به صورت REST و در صورت نیاز gRPC برای ارتباطات داخلی سریع.
  * **Streaming Response:** پشتیبانی از Server-Sent Events (SSE) برای اینکه کاربر کلمه به کلمه تایپ شدن جواب را ببیند (تجربه کاربری بهتر).
  * **Auth & Security:** مدیریت توکن‌های دسترسی (JWT) و Rate Limiting برای جلوگیری از حملات DDOS داخلی.

### ۷. نظارت و حاکمیت (Observability & Governance)

**نقش:** برج مراقبت و جعبه سیاه (The Watchtower)
برای یک سیستم سازمانی (Enterprise)، این لایه اختیاری نیست، بلکه الزامی است.

* **وظایف کلیدی:**
  * **Tracing:** ردیابی درخواست از لحظه ورود تا خروجی (بسیار مهم برای دیباگ کردن کندی سیستم).
  * **Audit Logging:** ثبت دقیق اینکه چه کسی به چه سندی دسترسی داشته است (الزامات امنیتی).
  * **Feedback Loop:** جمع‌آوری بازخورد کاربران (Thumbs up/down) برای بهبود کیفیت مدل در آینده.
  * **Cost/Resource Monitoring:** نظارت بر مصرف CPU و RAM برای جلوگیری از Crash کردن سرور.

---

### **جمع‌بندی معماری:**

این تقسیم‌بندی ۷ لایه عالی است زیرا:

1. **Loose Coupling:** اگر بخواهید فردا مدل Embedding را عوض کنید، فقط لایه ۳ تغییر می‌کند و بقیه سیستم دست‌نخورده می‌ماند.
2. **Scalability:** می‌توانید فقط لایه Processing را روی چند سرور مختلف توزیع کنید (Scale-out) بدون اینکه نیاز باشد دیتابیس را تغییر دهید.
3. **Observability:** با جدا کردن لایه‌ها، دقیقاً می‌فهمید خطا در کدام مرحله رخ داده است (مثلاً اگر OCR بد کار کند، در لایه ۲ لاگ می‌شود).
