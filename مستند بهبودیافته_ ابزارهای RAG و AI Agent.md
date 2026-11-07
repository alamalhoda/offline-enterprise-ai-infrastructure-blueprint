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
| جامعه | کوچک‌تر | اما enterprise-focused |

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
| Latency | 3.53ms | DSPy compiled module، GPU |
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
    وابستگی: hazm >= 0.9.0
    
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
        current_sentences: List[str] = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            # جمله‌ای که به تنهایی از حد مجاز بزرگ‌تر است
            if sentence_len > self._chunk_size:
                # ابتدا Chunk فعلی را ذخیره کن
                if current_sentences:
                    chunks.append(" ".join(current_sentences))
                    current_sentences = self._extract_overlap(current_sentences)
                    current_length = sum(len(s) for s in current_sentences)

                # جمله بزرگ را به تنهایی اضافه کن
                chunks.append(sentence)
                current_sentences = []
                current_length = 0
                continue

            # اگر جمله جدید Chunk فعلی را پر می‌کند
            if current_length + sentence_len > self._chunk_size and current_sentences:
                chunks.append(" ".join(current_sentences))
                # Overlap: آخرین جملات را نگه دار
                current_sentences = self._extract_overlap(current_sentences)
                current_length = sum(len(s) for s in current_sentences)

            current_sentences.append(sentence)
            current_length += sentence_len

        # آخرین Chunk
        if current_sentences:
            chunks.append(" ".join(current_sentences))

        return [c for c in chunks if c.strip()]

    def _extract_overlap(self, sentences: List[str]) -> List[str]:
        """
        از آخر لیست جملات را انتخاب می‌کند تا به chunk_overlap برسیم.
        """
        overlap_sentences: List[str] = []
        overlap_length = 0

        for sentence in reversed(sentences):
            if overlap_length + len(sentence) <= self._chunk_overlap:
                overlap_sentences.insert(0, sentence)
                overlap_length += len(sentence)
            else:
                break

        return overlap_sentences
```

### ۳.۳ Adapter به LlamaIndex

```python
from llama_index.core.node_parser import NodeParser
from llama_index.core.schema import BaseNode, TextNode, Document
from typing import List, Sequence


class PersianNodeParser(NodeParser):
    """
    اتصال PersianTextSplitter به LlamaIndex.
    
    استفاده:
        parser = PersianNodeParser(chunk_size=512, chunk_overlap=50)
        index = VectorStoreIndex.from_documents(docs, node_parser=parser)
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self._splitter = PersianTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def get_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
    ) -> List[BaseNode]:
        nodes: List[BaseNode] = []

        for doc in documents:
            chunks = self._splitter.split_text(doc.text)
            for i, chunk in enumerate(chunks):
                node = TextNode(
                    text=chunk,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "source_doc_id": doc.doc_id,
                    },
                )
                nodes.append(node)

        return nodes
```

### ۳.۴ Adapter به Haystack

```python
from haystack import component, Document
from typing import List


@component
class PersianDocumentSplitter:
    """
    Component بومی Haystack برای پردازش فارسی.
    
    استفاده در Pipeline:
        pipeline.add_component("splitter", PersianDocumentSplitter())
        pipeline.connect("converter.documents", "splitter.documents")
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self._splitter = PersianTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]) -> dict:
        result: List[Document] = []

        for doc in documents:
            if not doc.content:
                continue

            chunks = self._splitter.split_text(doc.content)
            for i, chunk in enumerate(chunks):
                result.append(
                    Document(
                        content=chunk,
                        meta={
                            **doc.meta,
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                        },
                    )
                )

        return {"documents": result}
```

---

## ۴. درخت تصمیم — کدام ابزار را انتخاب کنم؟

آیا پروژه شما RAG سند‌محور است؟
│
├── بله
│    │
│    ├── آیا اسناد پیچیده (PDF با جدول، تصویر) دارید؟
│    │    ├── بله → RAGFlow (سریع‌ترین راه‌اندازی)
│    │    └── خیر ↓
│    │
│    ├── آیا تیم بزرگ و پروژه بلندمدت دارید؟
│    │    ├── بله → Haystack + LlamaIndex (پایدارترین ترکیب)
│    │    └── خیر → LlamaIndex به تنهایی
│    │
│    └── آیا Agent چندمرحله‌ای با حلقه تصمیم نیاز دارید؟
│         ├── بله → LangGraph روی Haystack
│         └── خیر → همان انتخاب قبلی
│
└── خیر — می‌خواهید کیفیت Prompt را بهبود دهید؟
     └── DSPy (روی هر Framework موجود)


---

## ۵. ترکیب پیشنهادی برای محیط شما

بر اساس قیدهای **آفلاین، CPU-Only، فارسی‌محور، و نیاز به Audit**:

### ترکیب توصیه‌شده

لایه Ingestion:
    PersianTextSplitter (Hazm) → PersianNodeParser

لایه Indexing:
    LlamaIndex + Qdrant (Hybrid: Vector + BM25)

لایه Orchestration:
    Haystack Pipeline (DAG صریح، قابل Audit)

لایه LLM:
    LangChain Adapter → Llama.cpp (CPU-Optimized)

لایه بهینه‌سازی (اختیاری، مرحله دوم):
    DSPy برای Prompt Compilation


### معماری Hexagonal — جایگاه ابزارها

┌─────────────────────────────────────────────────────┐
│                  Domain Logic                        │
│         (هیچ import از LangChain/LlamaIndex)         │
│                                                     │
│   IDocumentRepository    ILLMService                │
│         ↑                    ↑                       │
└─────────│────────────────────│────────────────────────┘
          │                    │
  ┌───────┴──────┐    ┌────────┴──────┐
  │  LlamaIndex  │    │  LangChain    │
  │  + Haystack  │    │  Adapter      │
  │  Adapter     │    │  → Llama.cpp  │
  └──────────────┘    └───────────────┘


---

## ۶. جدول مرجع نهایی

| معیار | LlamaIndex | Haystack | LangChain | LangGraph | RAGFlow | DSPy |
|---|---|---|---|---|---|---|
| آفلاین | ✅ عالی | ✅ عالی | ✅ خوب | ✅ خوب | ✅ عالی | ✅ عالی |
| CPU-Only | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| فارسی | ⚠️ تنظیم | ✅ ICU | ⚠️ تنظیم | ⚠️ تنظیم | ⚠️ در حال بهبود | ⚠️ تنظیم |
| Audit | ✅ خوب | ✅ ذاتی | ❌ ضعیف | ✅ خوب | ✅ خوب | ➖ |
| پایداری API | ⚠️ متوسط | ✅ بالا | ❌ پایین | ❌ پایین | ✅ خوب | ✅ خوب |
| یادگیری | متوسط | متوسط | متوسط | ❌ سخت | ✅ آسان | متوسط |
| اسناد پیچیده | ✅ خوب | ✅ خوب | ⚠️ متوسط | ➖ | ✅ بهترین | ➖ |
| لایه پیشنهادی | Ingestion/Index | Orchestration | LLM Adapter | Agent Engine | کل Pipeline | Optimization |

---

## ۷. نتیجه‌گیری — سه قانون برای تصمیم‌گیری

**قانون ۱ — لایه‌بندی قبل از انتخاب:**
ابتدا تصمیم بگیرید هر لایه معماری چه کاری انجام می‌دهد. سپس ابزار آن لایه را انتخاب کنید. برعکس این کار نکنید.

**قانون ۲ — هیچ ابزاری در Domain Logic:**
Domain Logic شما نباید هیچ ابزار خارجی را مستقیم import کند. همه ابزارها پشت Interface و Adapter هستند. این قانون امنیت معماری شما در برابر Breaking Changes است.

**قانون ۳ — فارسی از روز اول:**
PersianTextSplitter را از روز اول در Pipeline قرار دهید. اضافه کردن آن در وسط پروژه نیاز به Reindex کامل دارد که در پروژه‌های بزرگ هزینه بالایی دارد.

---


# مستند جامع معماری و پیاده‌سازی ابزارهای RAG و AI Agent
**تاریخ:** 1404/12/03 | 2026/02/22
**محیط استقرار:** Enterprise, Air-Gapped (Offline), CPU-Only
**زبان هدف:** فارسی / انگلیسی

## ۱. چارچوب مفهومی: طبقه‌بندی ابزارها بر اساس لایه معماری
بزرگترین خطای استراتژیک در طراحی سیستم‌های هوش مصنوعی، مقایسه ابزارهایی است که در لایه‌های متفاوتی کار می‌کنند. در یک معماری اصولی، جایگاه ابزارها به شرح زیر است:

| لایه معماری سیستم | ابزار پیشنهادی (کاندیداها) | وظیفه اصلی |
| :--- | :--- | :--- |
| **لایه بهینه‌سازی (Optimization)** | **DSPy** | یادگیری و کامپایل کردن Promptهای بهینه (این یک RAG Framework نیست). |
| **لایه هماهنگ‌سازی (Orchestration)** | **Haystack, LangGraph, LangChain** | مدیریت جریان داده، اتصال کامپوننت‌ها به یکدیگر و مدیریت وضعیت (State). |
| **لایه هسته داده (RAG Core)** | **LlamaIndex, RAGFlow** | استخراج متن از فایل‌ها، قطعه‌بندی (Chunking)، ایندکس‌گذاری و بازیابی وکتوری. |

---

## ۲. تحلیل تفصیلی و انتخاب ابزارها برای محیط آفلاین و CPU-Only

### ۲.۱ LlamaIndex (ستون فقرات داده و RAG)
این فریم‌ورک بهترین انتخاب برای سیستم‌های سندمحور (Document-Heavy) سازمانی است.
*   **مزیت برای محیط شما:** دارای استراتژی‌های پیشرفته `Hierarchical Indexing` (ایجاد درخت از اسناد) است. ماژول‌های بسیار بهینه‌ای برای اتصال به دیتابیس `Qdrant` دارد.
*   **قابلیت آفلاین و CPU:** پشتیبانی کامل از مدل‌های Local (HuggingFace/ONNX) بدون نیاز به اینترنت.
*   **وضعیت زبان فارسی:** نیاز به اتصال به ابزارهای جانبی (مانند Hazm) برای قطعه‌بندی صحیح دارد.
*   **نتیجه‌گیری:** انتخاب **قطعی** برای لایه Ingestion و Indexing.

### ۲.۲ Haystack (هماهنگ‌کننده پایدار و سازمانی)
اگر کد شما باید سال‌ها با کمترین هزینه نگهداری کار کند، Haystack (محصول Deepset) بهترین گزینه است.
*   **مزیت برای محیط شما:** معماری آن بر اساس گراف‌های جهت‌دار غیرمدور (DAG) است. مصرف RAM آن بسیار پایین است (ایده‌آل برای CPU-Only) و لاگ‌گیری شفافی دارد که برای ممیزی (Auditability) در سازمان‌ها حیاتی است.
*   **وضعیت زبان فارسی:** بهترین پشتیبانی ذاتی از زبان‌های راست‌به‌چپ (RTL) و افزونه‌های ICU را دارد.
*   **نتیجه‌گیری:** انتخاب **اصلی** برای لایه Orchestration تیم‌های بزرگ.

### ۲.۳ LangChain (پلی ارتباطی با ریسک معماری)
محبوب‌ترین ابزار بازار، اما نیازمند احتیاط در استفاده سازمانی.
*   **مزیت برای محیط شما:** راحت‌ترین و سریع‌ترین روش برای اتصال به مدل‌های `Llama.cpp` (مدل‌های GGUF روی CPU) را فراهم می‌کند.
*   **هشدار معماری:** نرخ تغییرات (Breaking Changes) در این ابزار بالاست و کدهای شما را مستهلک می‌کند. 
*   **نتیجه‌گیری:** هرگز منطق اصلی (Domain Logic) خود را به LangChain وابسته نکنید. از آن فقط به عنوان یک Adapter در لایه زیرساخت (معماری ۶ ضلعی) استفاده کنید.

### ۲.۴ LangGraph (موتور تصمیم‌گیری چرخه‌ای)
این ابزار یک اکستنشن ساده نیست، بلکه یک موتور ماشین وضعیت (State Machine) است.
*   **کاربرد اصلی:** فقط زمانی استفاده کنید که سیستم باید چرخه تصمیم‌گیری داشته باشد (مثلاً: جستجو کن $\rightarrow$ اگر جواب ضعیف بود $\rightarrow$ دوباره با کوئری جدید جستجو کن).
*   **نتیجه‌گیری:** برای RAG خطی نیازی به آن نیست، اما برای Agentهای پیشرفته ضروری است.

### ۲.۵ DSPy (کامپایلر Prompt)
این ابزار یک تغییر پارادایم است. به جای اینکه Prompt را دستی بنویسید، ورودی و خروجی را به DSPy می‌دهید تا خودش با یادگیری ماشین، بهترین Prompt را برای مدل شما بسازد.
*   **نتیجه‌گیری:** این ابزار روی LlamaIndex یا Haystack قرار می‌گیرد (رقیب آن‌ها نیست) و برای فاز دوم پروژه (پس از استقرار اولیه) جهت افزایش دقت پاسخ‌ها عالی است.

### ۲.۶ RAGFlow (موتور End-to-End اسناد پیچیده)
یک پلتفرم کامل مبتنی بر Docker.
*   **مزیت کلیدی:** از تکنولوژی `TreeRAG` استفاده می‌کند. اگر اسناد شما پر از جداول، نمودارها و فرمت‌های پیچیده تودرتو است، RAGFlow بهتر از هر ابزار دیگری ساختار سند را درک می‌کند.
*   **نتیجه‌گیری:** اگر زمان راه‌اندازی سریع می‌خواهید و رم کافی (حداقل 16GB) روی سرور دارید، عالی است؛ اما سفارشی‌سازی کد در آن سخت‌تر از Haystack است.

---

## ۳. راهکار اجرایی برای چالش زبان فارسی (Production Code)

همان‌طور که بررسی شد، Text Splitterهای پیش‌فرض این ابزارها با فاصله انگلیسی کار می‌کنند و در مواجهه با نیم‌فاصله‌های فارسی (ZWNJ) یا ساختار جملات، خروجی‌های نامعتبری تولید می‌کنند. 

کد زیر، هسته اصلی پردازش متن فارسی شماست که باید در لایه Ingestion قرار گیرد:

```python
import unicodedata
import re
from typing import List, Optional
import logging

try:
    from hazm import Normalizer, sent_tokenize
    HAZM_AVAILABLE = True
except ImportError:
    HAZM_AVAILABLE = False
    logging.warning("Please install hazm: pip install hazm")

class EnterprisePersianSplitter:
    """
    قطعه‌ساز متون فارسی سازگار با محیط‌های Enterprise
    طراحی شده برای قرارگیری در لایه Domain/Core (مستقل از فریم‌ورک‌ها)
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if HAZM_AVAILABLE:
            self.normalizer = Normalizer()
        
    def normalize_text(self, text: str) -> str:
        """پاکسازی و استانداردسازی کاراکترهای فارسی"""
        if not text: return ""
        text = unicodedata.normalize("NFC", text)
        if HAZM_AVAILABLE:
            text = self.normalizer.normalize(text)
        # اصلاح کشیدگی و فاصله‌های مضاعف
        text = re.sub(r"ـ+", "", text)
        text = re.sub(r" {2,}", " ", text)
        return text.strip()

    def split_text(self, text: str) -> List[str]:
        """شکستن متن بر اساس منطق جملات فارسی با رعایت Overlap دقیق"""
        normalized = self.normalize_text(text)
        if not normalized: return []

        # استفاده از مدل‌های زبانی برای تشخیص پایان جمله
        sentences = sent_tokenize(normalized) if HAZM_AVAILABLE else re.split(r'[.!?؟]\s+', normalized)
        
        chunks = []
        current_chunk = []
        current_len = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            
            if current_len + sentence_len > self.chunk_size and current_chunk:
                # ذخیره چانک فعلی
                chunks.append(" ".join(current_chunk))
                
                # محاسبه Overlap برای چانک بعدی
                overlap_len = 0
                overlap_sentences = []
                for s in reversed(current_chunk):
                    if overlap_len + len(s) <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_len += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_len = sum(len(s) for s in overlap_sentences)

            current_chunk.append(sentence)
            current_len += sentence_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

# ==========================================
# Adapter Pattern: اتصال هسته فارسی به LlamaIndex
# این بخش باید در لایه Infrastructure قرار گیرد
# ==========================================
from llama_index.core.node_parser import TextSplitter as LlamaTextSplitter

class LlamaIndexPersianAdapter(LlamaTextSplitter):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self._persian_splitter = EnterprisePersianSplitter(chunk_size, chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        return self._persian_splitter.split_text(text)
```

---

## ۴. معماری نهایی، Stack پیشنهادی و جریان داده

برای محیط کاملاً ایزوله (Offline)، مبتنی بر CPU و متمرکز بر زبان فارسی، معماری زیر بهینه‌ترین حالت ممکن است:

### الف) Stack تکنولوژی پیشنهادی
*   **پردازش و Ingestion اسناد:** `LlamaIndex` + کلاس `EnterprisePersianSplitter` (برای درک دقیق ساختار فایل و زبان فارسی).
*   **مدل Embedding:** مدل `BGE-M3` (اجرا روی CPU - بهترین درک دوزبانه فارسی/انگلیسی).
*   **ذخیره‌سازی (Vector Store):** دیتابیس `Qdrant` (بر پایه زبان Rust، مصرف منابع بسیار کم، فوق‌العاده سریع روی پردازنده مرکزی).
*   **هماهنگ‌سازی (Orchestration):** فریم‌ورک `Haystack` (پایپ‌لاین‌های کاملاً قابل ردیابی و مصرف رم مدیریت شده).
*   **مدل زبانی تولید متن (LLM):** مدل `Llama-3-8B` (یا مدل‌های مشابه با فرمت `GGUF`) اجرا شده توسط `Llama.cpp` از طریق یک Adapter در LangChain.

### ب) جریان داده در زمان پرسش (Query Data Flow)
1. کاربر سوال را (به فارسی) ارسال می‌کند.
2. سوال توسط ابزار نرمال‌ساز فارسی تمیز می‌شود.
3. پایپ‌لاین `Haystack` سوال را به مدل Embedding می‌فرستد تا وکتور آن تولید شود.
4. جستجوی هیبریدی (BM25 + Vector) درون `Qdrant` انجام می‌شود.
5. نتایج بازیابی شده همراه با سوال کاربر در یک Prompt سفارشی قرار می‌گیرند.
6. مدل `Llama.cpp` روی CPU متن را پردازش کرده و پاسخ نهایی فارسی را تولید می‌کند.


---

## شرح تفصیلی معماری نهایی و جریان داده (Deep Dive)

### الف) منطق مهندسی و هم‌افزایی (Synergy) در Stack پیشنهادی

چرا این ترکیب خاص از ابزارها برای محیط **Offline / CPU-Only / زبان فارسی** بی‌نظیر است؟

1. **LlamaIndex (فقط برای Ingestion):** ما از این ابزار برای ساخت پایپ‌لاین پرسش‌وپاسخ استفاده نمی‌کنیم، بلکه فقط از موتور **پارس کردن اسناد** آن بهره می‌بریم. LlamaIndex می‌تواند یک فایل PDF ۵۰۰ صفحه‌ای را بخواند، ساختار درختی آن (فصل، بخش، پاراگراف) را درک کند و همراه با متادیتا استخراج کند.
2. **کلاس سفارشی PersianSplitter:** متن خامِ استخراج‌شده توسط LlamaIndex، قبل از تبدیل شدن به وکتور، وارد این کلاس می‌شود. این کلاس مطمئن می‌شود که نیم‌فاصله‌ها حفظ شده و جملات فارسی از وسط شکسته نشده‌اند (جلوگیری از قطع شدن Context).
3. **مدل BGE-M3:** این مدل ساخت آکادمی هوش مصنوعی پکن (BAAI) است. چرا این مدل؟ زیرا **M3** مخفف Multi-Lingual (پشتیبانی از ۱۰۰ زبان از جمله فارسی با کیفیت استثنایی)، Multi-Granularity (درک متون کوتاه تا ۸۱۹۲ توکن) و Multi-Function (تولید همزمان بردارهای متراکم و تُنک) است.
4. **دیتابیس Qdrant:** چون سرور شما فقط CPU دارد، اجرای دیتابیس‌هایی مثل Milvus یا Pinecone (که ابری است) غیرمنطقی یا ناممکن است. Qdrant با زبان Rust نوشته شده و الگوریتم HNSW آن برای اجرا روی پردازنده‌های مرکزی (CPU) به شدت بهینه‌سازی شده است.
5. **ارکستراتور Haystack:** به عنوان مدیر این ارکستر عمل می‌کند. وقتی کوئری کاربر می‌آید، Haystack با مصرف حداقل RAM، جریان داده را مدیریت می‌کند تا به جواب برسد.
6. **مدل Llama.cpp + GGUF:** برای اجرای یک مدل ۸ میلیارد پارامتری (مثل Llama-3-8B) روی CPU، ما از تکنیک کوانتیزاسیون (Quantization) با فرمت `GGUF` (مثلاً نسخه `Q4_K_M`) استفاده می‌کنیم. این کار باعث می‌شود مدل به جای ۱۶ گیگابایت، تنها حدود ۵.۵ تا ۶ گیگابایت از RAM (System Memory) را اشغال کند و روی CPU با سرعت قابل قبولی (حدود ۱۰ تا ۱۵ توکن بر ثانیه) متن تولید کند.

---

### ب) کالبدشکافی گام‌به‌گام جریان داده (Query Data Flow)

بیایید مسیر یک سوال را از لحظه تایپ شدن توسط کاربر تا تولید جواب بررسی کنیم:

### گام ۱: دریافت کوئری کاربر
کاربر سوالی می‌پرسد: *"شرایط مرخصی زایمان در آیین‌نامه سال ۱۴۰۲ چیست؟"*

### گام ۲: نرمال‌سازی (Normalization)
متن بالا ممکن است با کیبورد عربی تایپ شده باشد (مثلاً «آیين‌نامه» با «ي» عربی) یا کاربر به جای نیم‌فاصله، از فاصله استفاده کرده باشد.
کلاس `PersianTextNormalizer` کوئری را به فرمت استاندارد تبدیل می‌کند: *"شرایط مرخصی زایمان در آیین‌نامه سال ۱۴۰۲ چیست؟"* (ی یکپارچه، نیم‌فاصله اصلاح‌شده). 
**اهمیت:** اگر کوئری نرمال نشود، مدل Embedding بردار متفاوتی تولید می‌کند و اسناد مرتبط در دیتابیس پیدا نمی‌شوند.

### گام ۳: تبدیل کوئری به بردار (Embedding)
Haystack متن نرمال‌شده را به مدل BGE-M3 می‌دهد. مدل روی CPU پردازش را انجام داده و یک آرایه عددی (مثلاً با ابعاد ۱۰۲۴) تولید می‌کند که نشان‌دهنده **معنای** سوال است.

### گام ۴: جستجوی هیبریدی در Qdrant (مهم‌ترین گام در معماری RAG)
در محیط‌های سازمانی، جستجوی برداری (Vector/Semantic Search) به تنهایی کافی نیست. ما به **جستجوی هیبریدی (Hybrid Search)** نیاز داریم که ترکیب دو مکانیزم زیر است:

*   **الف) جستجوی معنایی (Dense Vector Search):**
    مفهوم کوئری را پیدا می‌کند. مثلاً اگر کاربر بگوید "قوانین وضع حمل"، سیستم به صورت معنایی می‌فهمد که این معادل "مرخصی زایمان" است.
*   **ب) جستجوی کلمات کلیدی (Sparse Search / BM25):**
    برای کلمات کلیدی دقیق، اعداد و شناسه‌ها (مثل "سال ۱۴۰۲" یا "شماره بخشنامه 14/ب")، جستجوی برداری ضعیف عمل می‌کند. الگوریتم BM25 دقیقاً به دنبال همین کلمات می‌گردد.

**مکانیزم ادغام (Reciprocal Rank Fusion - RRF):**
Qdrant نتایج هر دو جستجو را می‌گیرد و با فرمول ریاضی زیر ترکیب می‌کند تا بهترین اسناد را استخراج کند:
$$RRF Score = \frac{1}{k + Rank_{Dense}} + \frac{1}{k + Rank_{Sparse}}$$
*(معمولاً ثابت $k = 60$ در نظر گرفته می‌شود).*
خروجی این گام، استخراج ۵ تا ۱۰ تکه از مرتبط‌ترین متون (Chunks) از میان میلیون‌ها خط سند است.

### گام ۵: ساخت Prompt سفارشی (Prompt Assembly)
حالا Haystack وارد عمل می‌شود و تکه متون پیدا شده را همراه با دستورات سیستمی در یک قالب قرار می‌دهد:

```text
[System]
شما یک دستیار سازمانی دقیق هستید. فقط بر اساس اطلاعات زیر به زبان فارسی حرفه‌ای پاسخ دهید. اگر پاسخ در اطلاعات نیست بگویید "نمی‌دانم".

[Context]
سند ۱: بر اساس آیین‌نامه ۱۴۰۲، مرخصی زایمان ۹ ماه است...
سند ۲: ...

[User]
شرایط مرخصی زایمان در آیین‌نامه سال ۱۴۰۲ چیست؟
```

### گام ۶: تولید پاسخ روی CPU (Generation)
این Prompt غول‌پیکر (شاید حاوی ۲۰۰۰ کلمه) از طریق LangChain (به عنوان یک Adapter) به `Llama.cpp` ارسال می‌شود. 
*   **معماری سخت‌افزاری در این لحظه:** `Llama.cpp` از تکنولوژی `mmap` (Memory Mapped Files) استفاده می‌کند تا وزن‌های مدل را از هارد SSD به RAM منتقل کند و با استفاده از تمام هسته‌های CPU (با کتابخانه OpenBLAS یا مشابه آن) شروع به پیش‌بینی کلمه بعدی (Token prediction) می‌کند.
*   پاسخ نهایی به صورت Stream (کلمه‌به‌کلمه) به کاربر نمایش داده می‌شود تا کاربر احساس کند سیستم بسیار سریع است.

---

## ج) الزامات پیاده‌سازی این بخش برای تیم فنی

برای اینکه این جریان داده به درستی کار کند، تیم فنی شما باید موارد زیر را در کد پیاده‌سازی کند:

1. **جداسازی Payload از Vector:** در Qdrant، متن اصلی فارسی (Payload) را ذخیره کنید اما در زمان جستجو فقط بردارها را لود کنید تا RAM پر نشود.
2. **تنظیم Threadهای CPU:** در `Llama.cpp` تعداد Threadها را نباید بیشتر از تعداد هسته‌های فیزیکی (Physical Cores) سرور تنظیم کنید. اگر Hyper-threading فعال است، استفاده از هسته‌های مجازی (Logical) برای LLM معمولاً باعث کندی می‌شود.
3. **مکانیزم Fallback:** در Haystack یک مسیر شرطی بسازید که اگر `Score` نتایج استخراج شده از Qdrant در گام ۴ کمتر از حد مشخصی (مثلاً 0.65) بود، سیستم اصلاً کوئری را به LLM نفرستد و مستقیماً به کاربر بگوید: "در اسناد سازمانی یافت نشد". (این کار بار پردازشی CPU را به شدت کاهش می‌دهد).

## ۵. قوانین طلایی معماری برای تیم توسعه (مهم)
1. **قانون معماری ۶ ضلعی:** در هیچ‌کجای سیستم، کلمات `import langchain` یا `import llama_index` نباید در فایل‌های منطق کسب‌وکار (Domain Logic) شما دیده شود. همیشه یک `Interface` بنویسید و ابزارها را پشت آن پنهان کنید.
2. **قانون قطعه‌بندی:** هیچ سندی نباید بدون عبور از کلاس سفارشی `EnterprisePersianSplitter` وارد دیتابیس برداری شود. در غیر این صورت دقت بازیابی (Recall) به شدت افت خواهد کرد.
3. **قانون منابع:** در سیستم‌های CPU-Only، در زمان راه‌اندازی (Ingestion) اسناد بزرگ، پردازش را به صورت Batchهای شبانه انجام دهید تا سرور دچار اختلال در پاسخگویی به کاربران نشود.

> **نسخه ۳.۰** | تاریخ: فوریه ۲۰۲۶
