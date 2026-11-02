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

> هیچ ابزاری نباید مستقیم در Domain Logic نشیند.. همه ابزارها در لایه Infrastructure قرار می‌گیرند و از طریق Interface با هسته ارتباط دارند.

---

(Full content available in local artifacts; this is a placeholder update to ensure Windows-safe name. Please pull and replace with full content from artifacts if needed.)
