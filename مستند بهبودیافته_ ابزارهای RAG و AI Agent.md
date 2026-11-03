# مستند ابزارهای RAG و AI Agent — نسخه ۳.۰ (نهایی)

---

> **راهنمای تصمیم معماری برای سیستم‌های Enterprise**
> نسخه ۳.۰ | فوریه ۲۰۲۶ | محیط هدف: آفلاین، CPU-Only، فارسی‌محور

---

## ۰. پیش از هر چیز: نقشه ذهنی کل مستند

قبل از ورود به جزئیات، این جدول را ببینید. اگر وقت محدود دارید، همین یک جدول کافی است:

| ابزار | دسته واقعی | لایه پیشنهادی در معماری شما | وقتی باید انتخاب کنید |
|---|---|---|---|
| **LlamaIndex** | RAG Framework | Ingestion + Indexing | هر پروژه RAG با اسناد سازمانی |
| **Haystack** | Pipeline Orchestrator | Orchestration (پایدار) | تیم بزرگ، نیاز به Audit، بلندمدت |
| **LangChain** | General Framework | LLM Adapter | نیاز به اتصال سریع به Llama.cpp |
| **LangGraph** | State Machine Engine | Orchestration (پیچیده) | Agent چندمرحله‌ای با حلقه تصمیم |
| **RAGFlow** | End-to-End Platform | کل Pipeline | اسناد پیچیده، تیم کوچک، سرعت راه‌اندازی |
| **DSPy** | Prompt Compiler | Optimization Layer | بهینه‌سازی Prompt، نه ساخت RAG |

> ⚠️ **هشدار طبقه‌بندی:** DSPy یک RAG Framework نیست. این یک کامپایلر Prompt است که روی هر Framework دیگری می‌نشیند. قرار دادن آن کنار LlamaIndex یا Haystack مقایسه سیب با پرتقال است.

---

## ۱. لایه‌بندی معماری و جایگاه هر ابزار

┌─────────────────────────────────────────────────┐
│              لایه Generation                     │
│         (هر LLM از طریق Adapter)                │
├─────────────────────────────────────────────────┤
│           لایه Orchestration                     │
│      Haystack (پایدار) | LangGraph (پیچیده)     │
├─────────────────────────────────────────────────┤
│         لایه Retrieval + Indexing                │
│              LlamaIndex | RAGFlow                │
├─────────────────────────────────────────────────┤
│           لایه Ingestion + NLP                   │
│    PersianTextSplitter + Hazm/DadmaTools         │
└─────────────────────────────────────────────────┘


**قانون طلایی این معماری:**

> هیچ ابزاری نباید مستقیم در Domain Logic نشیند. همه ابزارها در لایه Infrastructure قرار می‌گیرند و از طریق Interface با هسته ارتباط دارند.

---

## ۲. تحلیل تفصیلی هر ابزار

### ۲.۱ — LlamaIndex | ستون فقرات RAG شما

**در یک جمله:** اگر پروژه شما درباره اسناد سازمانی است، LlamaIndex اولین ابزاری است که باید نصب کنید.

#### چرا LlamaIndex، نه LangChain؟

LangChain یک ابزار عمومی است که RAG هم بلد است. LlamaIndex یک ابزار RAG است که بقیه کارها را هم بلد است. برای محیط سازمانی با اسناد پیچیده، این تفاوت حیاتی است.

| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| آفلاین | ✅ کامل | ONNX + HuggingFace بدون اینترنت |
| CPU-Only | ✅ قابل قبول | نیاز به تنظیم batch_size |
| فارسی | ⚠️ نیاز به تنظیم | multilingual-e5 + Hazm |
| Audit | ✅ خوب | query logging داخلی |
| یادگیری | متوسط | ۲-۳ هفته برای تسلط |
| پایداری API | متوسط | migration گاه‌به‌گاه |

#### قابلیت‌های کلیدی برای محیط شما

- **Hierarchical Indexing:** اسناد طولانی را به درخت سلسله‌مراتبی تبدیل می‌کند. برای آیین‌نامه‌ها و دستورالعمل‌های سازمانی که فصل‌بندی دارند، بازیابی را تا ۴۰٪ دقیق‌تر می‌کند
- **Hybrid Retrieval:** ترکیب Vector Search و BM25 در یک Query
- **Qdrant Integration:** بهینه‌ترین Connector موجود برای Qdrant

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Recall در RAG سنگین | ~5% بهتر از LangChain | مجموعه ۱۰k سند، GPU T4 |
| Latency CPU | 45-120ms | Llama-3-8B، RAM 32GB |
| منبع | MTEB Leaderboard 2025 | قابل تکرار در GitHub |

---

### ۲.۲ — Haystack | انتخاب تیم‌های جدی

**در یک جمله:** اگر کد شما باید ۳ سال دیگر هم کار کند و هر تغییری Audit شود، Haystack را انتخاب کنید.

#### چرا Haystack از LangChain پایدارتر است؟

LangChain یک chain از اشیاء است که داده درون آن جریان دارد — اما جریان پنهان است. Haystack یک DAG صریح است که هر گره و هر لبه را می‌توانید ببینید، لاگ کنید، و تست کنید.

LangChain:  chain.invoke() → ... → output  (جریان پنهان)
Haystack:   Node_A → Node_B → Node_C     (جریان صریح و قابل Audit)


| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| آفلاین | ✅ کامل | بدون وابستگی cloud |
| فارسی | ✅ بهترین گزینه | ICU plugin + RTL/ZWNJ داخلی |
| Audit | ✅ ذاتی | DAG قابل trace کامل |
| Breaking Changes | ✅ کم | API نسبتاً پایدار |
| یادگیری | متوسط | آسان‌تر از LangChain |
| جامعه | | کوچک‌تر | اما enterprise-focused |

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Latency | 5.9ms | Pipeline ساده، CPU |
| Uptime در Production | بالا | گزارش Deepset 2025 |

#### کِی Haystack را انتخاب کنید

- تیم بیش از ۳ نفر دارید
- نیاز به Auditability سیستماتیک دارید
- پروژه بلندمدت (بیش از ۱ سال) است
- نمی‌خواهید هر چند ماه یک‌بار Migration کنید

---

### ۲.۳ — LangChain | ابزار همه‌کاره با هزینه پنهان

**در یک جمله:** LangChain سریع‌ترین راه برای Prototype است، اما در Production یک ریسک معماری است.

#### هشدار معماری — مهم‌ترین بخش این فصل

❌ اشتباه رایج:
    MyService.query() → langchain.chain.invoke()
    
✅ معماری صحیح (Hexagonal):
    MyService.query() → ILLMAdapter.complete()
                              ↓ (Adapter Layer)
                     LangChainAdapter.complete()
                              ↓
                     langchain.chain.invoke()


اگر Domain Logic شما مستقیم LangChain import کند، در نسخه بعدی API که Breaking Change بیاید، کل codebase شما باید بازنویسی شود.

| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| آفلاین | ✅ خوب | Llama.cpp integration عالی |
| فارسی | ⚠️ نیاز به تنظیم | Hazm tokenizer سفارشی |
| Breaking Changes | ❌ مکرر | هر ۶-۸ هفته یک‌بار |
| Abstraction | ❌ زیاد | Debug سخت |
| Ecosystem | ✅ بزرگ‌ترین | بیش از ۱۰۰k ستاره |

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Latency RAG ساده | ~10ms | LangChain v0.3، CPU |
| Breaking Changes | هر ۶-۸ هفته | بررسی Changelog رسمی |

#### کِی LangChain انتخاب درستی است

- Prototype در کمتر از ۲ هفته می‌خواهید
- تیم به LangChain آشنا است
- **به شرط اینکه** آن را پشت یک Interface مخفی کنید

---

### ۲.۴ — LangGraph | موتور تصمیم برای Agent‌های پیچیده

**در یک جمله:** وقتی Agent شما باید تصمیم بگیرد، شکست بخورد، دوباره تلاش کند و حافظه داشته باشد — LangGraph تنها گزینه جدی است.

#### LangGraph یک Extension نیست — یک موتور State Machine است

معرفی LangGraph به عنوان "extension of LangChain" اشتباه است. LangGraph یک موتور State Machine مستقل است که کنار LangChain هم می‌تواند کار کند:

LangGraph State Machine:
    
    [کاربر] → [Agent Node] → آیا جواب کافی است؟
                                   ↓ خیر
                            [Search Node] → [Re-rank] → [Agent Node]
                                   ↓ بله
                            [Generation Node] → [کاربر]


| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| Stateful Agents | ✅ بهترین | حافظه بین چرخه‌ها |
| Multi-Agent | ✅ عالی | coordination داخلی |
| یادگیری | ❌ سخت | نیاز به درک OOP و Graph |
| Scaling | ⚠️ پیچیده | durable execution کمک می‌کند |
| CPU-Only | ✅ خوب | مانند LangChain |

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Efficiency Score | 7.5/10 | مقایسه با CrewAI و AutoGen |
| منبع | AgentBench 2025 | محیط Multi-step tasks |

#### کِی LangGraph را انتخاب کنید

- Agent باید چندین مرحله به هم وابسته اجرا کند
- شکست در یک مرحله باید به مرحله قبل برگردد
- نیاز به Memory بین Session دارید
- **فقط** اگر Haystack یا LlamaIndex پاسخگو نیستند — پیچیدگی LangGraph را دست کم نگیرید

---

### ۲.۵ — RAGFlow | قدرتمندترین گزینه برای اسناد پیچیده

**در یک جمله:** اگر اسناد شما PDF پیچیده، جدول، تصویر، یا ساختار غیرخطی دارد، RAGFlow تنها گزینه‌ای است که این چالش را جدی گرفته.

#### چرا RAGFlow دست‌کم گرفته می‌شود؟

اکثر مستندات RAGFlow را به عنوان "ابزار آسان‌تر" معرفی می‌کنند. این اشتباه است. RAGFlow پیشرفته‌ترین پردازش سند را ارائه می‌دهد:

**TreeRAG** — رویکرد اختصاصی RAGFlow:

سند PDF:
    فصل ۱ (Node)
        ├── بند ۱.۱ (Node)
        │       └── جمله‌های کلیدی (Leaf)
        └── جدول ۱.۲ (Node)  ← اینجا فریم‌ورک‌های دیگر شکست می‌خورند
                └── سلول‌های تحلیل‌شده (Leaf)


| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| اسناد پیچیده | ✅ بهترین | PDF با جدول، تصویر، فرمول |
| آفلاین | ✅ کامل | Docker-based، بدون cloud |
| Hybrid Search | ✅ ذاتی | Vector + BM25 از پایه |
| فارسی | ⚠️ در حال بهبود | multilingual parsing، RTL نیاز به تنظیم |
| UI بصری | ✅ عالی | No-code workflow builder |
| تیم کوچک | ✅ عالی | سریع‌ترین Time-to-Production |

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Accuracy اسناد پیچیده | بالاترین | مقایسه با LlamaIndex، Haystack |
| Time-to-Production | کمترین | نسبت به Framework-based approaches |
| منبع | RAGFlow Benchmark Suite 2025 | |

#### کِی RAGFlow انتخاب می‌کنید

- اسناد PDF پیچیده با جدول و تصویر دارید
- تیم کوچک است و نمی‌خواهید از صفر بسازید
- می‌خواهید ظرف ۲ هفته سیستم کامل داشته باشید
- آمادگی تنظیم فارسی روی Backend را دارید

---

### ۲.۶ — DSPy | این یک RAG Framework نیست

**در یک جمله:** DSPy Prompt شما را بهینه می‌کند — مثل کامپایلر برای دستورالعمل‌های زبانی.

#### اصلاح یک سوءتفاهم رایج

DSPy را نمی‌توان با LlamaIndex یا Haystack مقایسه کرد چون در لایه متفاوتی قرار دارد:

┌─ Framework Layer ─────────────────┐
│  LlamaIndex / Haystack / LangChain │
└────────────────────────────────────┘
        ↑ (DSPy روی اینها می‌نشیند)
┌─ Optimization Layer ───────────────┐
│  DSPy: Prompt را Compile می‌کند   │
└────────────────────────────────────┘


| قابلیت | وضعیت | جزئیات عملی |
|---|---|---|
| آفلاین | ✅ کامل | Local LMs |
| فارسی | ⚠️ نیاز به تنظیم | Custom normalizer |
| یادگیری | متوسط | مناسب ML devs آشنا به PyTorch |
| کاربرد اصلی | Prompt Optimization | نه جایگزین RAG Framework |

#### بنچمارک مرجع

| معیار | نتیجه | شرایط آزمایش |
|---|---|---|
| Latency inter_token | 3.53ms | DSPy compiled module، GPU |
| بهبود کیفیت Prompt | 15-30% | نسبت به دستی |
| منبع | Stanford DSPy Paper 2024 | |

#### کِی DSPy را اضافه می‌کنید

- سیستم RAG دارید و می‌خواهید کیفیت پاسخ‌ها را **بدون تغییر Architecture** بهبود دهید
- تیم ML دارید که با PyTorch آشناست
- **نه** به عنوان جایگزین Framework اصلی

---

## ۳. پیاده‌سازی فارسی — مهم‌ترین چالش فنی

### ۳.۱ مشکل اصلی

Text Splitterهای پیش‌فرض همه این ابزارها برای فارسی طراحی نشده‌اند. آن‌ها متن را بر اساس Space انگلیسی می‌شکنند و با نیم‌فاصله (ZWNJ) آشنا نیستند. نتیجه: Chunk‌های نامعنی که دقت RAG را به شدت کاهش می‌دهند.

### ۳.۲ راهکار: PersianTextSplitter کامل

```python
import unicodedata
from typing import List, Optional
from langchain.text_splitter import TextSplitter
from hazm import sent_tokenize, Normalizer


class PersianTextSplitter(TextSplitter):
    """
    Text Splitter بهینه برای زبان فارسی.
    
    جایگاه در معماری: لایه Ingestion (قبل از Embedding)
       واب    وابستگی: hazm >= 0.9.0
    
    مثال استفاده:
        splitter = PersianTextSplitter(chunk_size=512, chunk_overlap=50)
        chunks = splitter.split_text(persian_document)
    """

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        normalizer: Optional[Normalizer] = None,
    ):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # Normalizer برای حل مشکلات ZWNJ، یکسان‌سازی اعداد و نقطه‌گذاری
        self._normalizer = normalizer or Normalizer()

    # ─── Public Interface ────────────────────────────────────────────────

    def split_text(self, text: str) -> List[str]:
        """
        متن فارسی را به Chunk‌های معنادار تبدیل می‌کند.
        هر Chunk مرز جمله را رعایت می‌کند — نه مرز کاراکتر.
        """
        if not text or not text.strip():
            return []

        normalized = self._normalize(text)
        sentences = self._tokenize_sentences(normalized)

        if not sentences:
            return []

        return self._build_chunks(sentences)

    # ─── Private Helpers ─────────────────────────────────────────────────

    def _normalize(self, text: str) -> str:
        """
        مرحله ۱: نرمال‌سازی
        - یکسان‌سازی نیم‌فاصله (ZWNJ)
        - تبدیل اعداد عربی به فارسی
        - حذف کاراکترهای کنترلی اضافه
        """
        text = self._normalizer.normalize(text)
        # حذف کاراکترهای کنترلی به جز newline
        text = "".join(
            ch for ch in text
            if unicodedata.category(ch) != "Cc" or ch == "\n"
        )
        return text.strip()

    def _tokenize_sentences(self, text: str) -> List[str]:
        """
        مرحله ۲: تقطیع جمله‌ای
        - ابتدا پاراگراف‌ها را حفظ می‌کند
        - سپس درون هر پاراگراف جمله‌بندی می‌کند
        """
        sentences: List[str] = []
        for paragraph in text.split("\n"):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            tokenized = sent_tokenize(paragraph)
            sentences.extend(s.strip() for s in tokenized if s.strip())
        return sentences

    def _build_chunks(self, sentences: List[str]) -> List[str]:
        """
        مرحله ۳: ساخت Chunk با رعایت Overlap
        
        الگوریتم:
        1. جملات را یکی‌یکی اضافه کن تا chunk_size پر شود
        2. هنگام بستن Chunk، آخرین جملات را به عنوان Overlap نگه دار
        3. جمله‌ای که از chunk_size بزرگ‌تر است، به تنهایی یک Chunk می‌شود
        """
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length = 0

        for sentence in sentences:
            sent_len = len(sentence)

            # جمله خیلی بلند — تنهایی یک Chunk
            if sent_len > self._chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_length = 0
                chunks.append(sentence)
                continue

            # اگر اضافه کردن جمله باعث overflow شود
            if current_length + sent_len + 1 > self._chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))

                # Overlap: آخرین جملات را نگه دار
                overlap_sentences: List[str] = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    if overlap_len + len(s) > self._chunk_overlap:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s) + 1

                current_chunk = overlap_sentences
                current_length = overlap_len

            current_chunk.append(sentence)
            current_length += sent_len + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
```

### ۳.۳ نکات پیاده‌سازی فارسی

| موضوع | توصیه |
|---|---|
| نیم‌فاصله (ZWNJ) | با Hazm.normalize یکسان‌سازی شود |
| اعداد | اعداد عربی (٠١٢) به فارسی (۰۱۲) تبدیل شوند |
| جهت متن (RTL) | در Embedding مدل‌های multilingual معمولاً مشکلی ایجاد نمی‌کند |
| Stopwords | لیست فارسی Hazm + کلمات دامنه‌ای سازمان |
| Stemming | برای BM25 مفید است؛ برای Vector Search معمولاً لازم نیست |

---

## ۴. جدول تصمیم نهایی — کدام ابزار را انتخاب کنید؟

| سناریو | ابزار پیشنهادی | دلیل |
|---|---|---|
| پروژه RAG سازمانی با اسناد متنی | **LlamaIndex** | تخصص در Document RAG + Hierarchical Index |
| تیم بزرگ + نیاز به Audit بلندمدت | **Haystack** | DAG صریح + پایداری API |
| Prototype سریع (کمتر از ۲ هفته) | **LangChain** (پشت Interface) | اکوسیستم بزرگ + سرعت توسعه |
| Agent چندمرحله‌ای با حافظه و حلقه تصمیم | **LangGraph** | State Machine واقعی |
| اسناد PDF پیچیده (جدول، تصویر، ساختار غیرخطی) | **RAGFlow** | TreeRAG + پردازش سند پیشرفته |
| بهینه‌سازی کیفیت Prompt بدون تغییر معماری | **DSPy** | لایه Optimization روی Framework موجود |

---

## ۵. توصیه‌های معماری برای محیط آفلاین و CPU-Only

1. **همیشه Interface تعریف کنید** — هیچ Frameworkی را مستقیم در Domain Logic وارد نکنید.
2. **Embedding و LLM را جدا نگه دارید** — امکان تعویض مدل بدون بازنویسی Pipeline.
3. **Batch Size را برای CPU تنظیم کنید** — شروع با ۱۶ و افزایش تدریجی.
4. **مدل‌ها را از قبل دانلود و Quantize کنید** — هیچ دانلود آنلاین در Runtime.
5. **لاگ و Audit را از روز اول فعال کنید** — در محیط آفلاین دیباگ سخت‌تر است.
6. **Index Versioning داشته باشید** — امکان Rollback بدون از دست رفتن داده.

---

## ۶. جمع‌بندی

| ابزار | نقش اصلی | مناسب برای |
|---|---|---|
| LlamaIndex | ستون فقرات RAG | اکثر پروژه‌های سازمانی |
| Haystack | Orchestration پایدار | تیم‌های جدی و بلندمدت |
| LangChain | Adapter لایه LLM | Prototype و اتصال سریع |
| LangGraph | State Machine | Agentهای پیچیده |
| RAGFlow | پردازش اسناد پیچیده | PDFهای سازمانی سنگین |
| DSPy | بهینه‌سازی Prompt | بهبود کیفیت بدون بازنویسی |

> **قانون طلایی:** ابزار را بر اساس «لایه معماری» انتخاب کنید، نه بر اساس محبوبیت GitHub.

---

> **نسخه ۳.۰** | تاریخ: فوریه ۲۰۲۶
