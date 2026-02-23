# SINA — Roadmap کلان (نسخه ۲.۰)
### Secure Intelligent Network Assistant | با Milestone و Quality Gate کامل | 1404/12/04

---

## ۱. چشم‌انداز و اهداف استراتژیک

### چشم‌انداز محصول
> **SINA** یک دستیار هوش مصنوعی سازمانی کاملاً آفلاین است که کارکنان را قادر می‌سازد در کمتر از ۳۰ ثانیه، پاسخ دقیق با ارجاع سند از میان هزاران فایل سازمانی طبقه‌بندی‌شده دریافت کنند — بدون هیچ وابستگی به اینترنت یا سرویس ابری.

### اهداف کمی (Success Metrics)

| هدف | معیار | زمان سنجش |
|---|---|---|
| دقت پاسخ | $\geq 75\%$ روی سوالات تعریف‌شده | پایان Phase 1 |
| زمان پاسخ | $\leq 30$ ثانیه برای $95\%$ درخواست‌ها | پایان Phase 1 |
| پوشش اسناد | $\geq 1000$ فایل PDF/Word ایندکس‌شده | پایان Phase 1 |
| Uptime | $\geq 99\%$ در ساعات کاری | پایان Phase 2 |
| دقت OCR | $\geq 85\%$ روی اسناد اسکن‌شده فارسی | پایان Phase 2 |
| Audit Coverage | $100\%$ دسترسی‌ها ثبت‌شده | از Sprint 1 |

---

## ۲. نمای زمانی کلان

هفته    1    4    8    12   16   20   24   28   32   36   40
        │    │    │    │    │    │    │    │    │    │    │
Phase 0 ████████
Phase 1      ████████████████████████████████
Phase 2                                   ████████████████
Phase 3                                                  ████████
        │    │    │    │    │    │    │    │    │    │    │
Gates   G0        M1.1      M1.2 G1   M2.1      M2.2 G2       G3


---

## ۳. فاز صفر — Foundation & Setup

**بازه:** هفته ۱ تا ۴ | **تعداد Sprint:** 2 | **تیم اصلی:** Backend/Infra

---

### Milestoneهای Phase 0

#### M0.1 — محیط توسعه یکپارچه (پایان هفته ۲)

هدف: تمام اعضای تیم روی همان Stack کار کنند

خروجی‌های اجباری:
  ✦ Docker Compose با تمام سرویس‌ها UP
  ✦ Gitea (self-hosted) + Branch Strategy مصوب
  ✦ PyPI Mirror آفلاین (نصب بدون اینترنت)
  ✦ GPU Passthrough در Docker تست شده

خروجی‌های اختیاری:
  ◎ Portainer برای مدیریت Container
  ◎ Prometheus + Grafana (نسخه اولیه)


#### M0.2 — Stack پایه نصب و تست (پایان هفته ۴)

هدف: مدل‌ها روی سرور هستند و پاسخ می‌دهند

خروجی‌های اجباری:
  ✦ Qwen2.5-7B-GGUF لود شده و Hello World پاسخ داد
  ✦ BGE-M3 تبدیل به ONNX و روی GPU تست شد
  ✦ Qdrant راه‌اندازی و یک Vector ذخیره/بازیابی شد
  ✦ CI Pipeline: هر Push → تست خودکار
  ✦ مستند ADR نسخه ۱ (Architecture Decision Records)
  ✦ فرآیند HDD Update مستند و یک بار تست شد


---

### Quality Gates — Phase 0

> **Gate 0 (پایان هفته ۴):** بدون تأیید این Gate، Phase 1 شروع نمی‌شود.

| # | معیار سنجش | حد قابل قبول | روش تست | تصمیم‌گیرنده |
|---|---|---|---|---|
| QG0.1 | همه Container در Docker Compose بالا می‌آیند | $100\%$ بدون خطا | `docker compose up` | Tech Lead |
| QG0.2 | مدل GGUF یک سوال فارسی پاسخ می‌دهد | پاسخ منطقی | تست دستی | Tech Lead |
| QG0.3 | Embedding روی GPU اجرا می‌شود | زمان $\leq 2$ ثانیه برای یک متن | Benchmark Script | Backend Lead |
| QG0.4 | نصب آفلاین از PyPI Mirror کار می‌کند | بدون نیاز به اینترنت | تست روی شبکه ایزوله | Backend Lead |
| QG0.5 | CI Pipeline در هر Push اجرا می‌شود | حداکثر ۵ دقیقه اجرا | Push یک کامیت تست | Tech Lead |
| QG0.6 | فرآیند آپدیت HDD مستند و تست شده است | Rehearsal موفق | اجرای یک بار کامل | IT + Backend |

نتیجه Gate 0:
  ✅ همه معیارها → Phase 1 شروع می‌شود
  ⚠️ ۱-۲ مورد ناموفق → تمدید تا ۱ هفته
  ❌ بیش از ۲ مورد → بازبینی Stack و تأخیر Phase 1


---

## ۴. فاز یک — Core RAG MVP

**بازه:** هفته ۵ تا ۲۰ | **تعداد Sprint:** 8 | **تیم:** هر دو تیم

---

### Milestoneهای Phase 1

#### M1.1 — Ingestion Pipeline کامل (پایان هفته ۱۰)

هدف: اسناد وارد سیستم شوند و ایندکس شوند

Sprint 5-6: Ingestion Pipeline
  ✦ خواندن PDF Searchable با PyMuPDF
  ✦ خواندن فایل‌های Word با python-docx
  ✦ PersianTextSplitter (Hazm + ZWNJ) پیاده‌سازی شد
  ✦ Metadata استخراج: نام فایل، صفحه، تاریخ، security_level
  ✦ Deduplication با SHA-256 (جلوگیری از ایندکس تکراری)
  ✦ Message Queue (Redis) برای پردازش Async

Sprint 7-8: Embedding + Vector Index
  ✦ BGE-M3 روی GPU Embedding تولید می‌کند
  ✦ Batch Processing برای ۱۰۰۰ فایل (شبانه)
  ✦ Qdrant: ذخیره Vector + Payload (متن فارسی)
  ✦ BM25 Index برای Keyword Search ایجاد شد
  ✦ Metadata در PostgreSQL ذخیره شد


**Quality Check M1.1:**

| معیار | حد قابل قبول |
|---|---|
| ۱۰۰۰ فایل ایندکس می‌شوند | بدون خطای اسکریپت |
| هیچ فایلی دوبار ایندکس نمی‌شود | تست با فایل تکراری |
| Metadata در PostgreSQL کامل است | $100\%$ فایل‌ها دارای `security_level` |
| PersianSplitter نیم‌فاصله را حفظ می‌کند | تست با ۱۰ سند نمونه |

---

#### M1.2 — Hybrid Search + LLM (پایان هفته ۱۶)

هدف: سوال فارسی بپرسی، پاسخ با ارجاع بگیری

Sprint 9-10: Hybrid Search
  ✦ جستجوی Vector (Qdrant Dense Search)
  ✦ جستجوی BM25 (Keyword Exact Match)
  ✦ RRF Fusion برای ادغام نتایج
  ✦ Metadata Filtering بر اساس security_level
  ✦ Fallback: اگر Score < 0.65 → "یافت نشد"

Sprint 11-12: LLM Integration
  ✦ Prompt Template فارسی (System + Context + User)
  ✦ پاسخ با ارجاع (نام سند + شماره صفحه)
  ✦ Streaming Response (SSE)
  ✦ Fallback صریح "نمی‌دانم"

Sprint 13-14: API + Security + Audit
  ✦ REST API (FastAPI)
  ✦ JWT Authentication
  ✦ Access Control بر اساس security_level
  ✦ Audit Log: ۱۰۰٪ query‌ها ثبت می‌شوند
  ✦ Rate Limiting


**Quality Check M1.2:**

| معیار | حد قابل قبول |
|---|---|
| Recall Hybrid Search | $\geq 70\%$ روی ۵۰ سوال نمونه |
| پاسخ شامل ارجاع سند است | $\geq 90\%$ پاسخ‌ها |
| Fallback فعال می‌شود | وقتی Score $< 0.65$ |
| کاربر بدون دسترسی سند محرمانه نمی‌بیند | تست نفوذ دستی |
| همه query‌ها در Audit Log ثبت شدند | $100\%$ |

---

#### M1.3 — MVP Demo آماده (پایان هفته ۲۰)

هدف: نمایش به مدیریت ارشد

Sprint 15-16: Frontend MVP
  ✦ Chat UI (React/Vue)
  ✦ Document Viewer با Highlight صفحه
  ✦ Auth UI (Login + سطح دسترسی)
  ✦ Persona Selector (حداقل ۳ شخصیت)

Sprint 17-18: Performance + UAT
  ✦ بهینه‌سازی: زمان پاسخ ≤ 30 ثانیه
  ✦ UAT با ۵ کاربر آزمایشی
  ✦ رفع Bugهای حیاتی

Sprint 19-20: مستندسازی + Demo Pack
  ✦ Demo Script نهایی
  ✦ Release Notes نسخه MVP
  ✦ مستند راهنمای کاربر اولیه


**Quality Check M1.3:**

| معیار | حد قابل قبول |
|---|---|
| ۵ کاربر آزمایشی تأیید کردند | امتیاز $\geq 3.5/5$ |
| Demo بدون خطا اجرا شد | حداقل ۲ Run موفق |
| زمان پاسخ اندازه‌گیری شد | $P_{95} \leq 30$ ثانیه |
| Persona تغییر می‌کند | تست دستی |

---

### Quality Gates — Phase 1

> **Gate 1 (پایان هفته ۲۰):** نقطه تصمیم مدیریت ارشد.

| # | معیار سنجش | حد قابل قبول | روش اندازه‌گیری | تصمیم‌گیرنده |
|---|---|---|---|---|
| QG1.1 | دقت پاسخ روی سوالات تعریف‌شده | $\geq 75\%$ | ارزیابی دستی ۲۰ سوال | Product Owner |
| QG1.2 | زمان پاسخ (Latency) | $P_{95} \leq 30$ ثانیه | Load Test با ۵ کاربر همزمان | Backend Lead |
| QG1.3 | پوشش اسناد | $\geq 1000$ فایل ایندکس‌شده | Query از Qdrant | Backend Lead |
| QG1.4 | Recall جستجو | $\geq 70\%$ روی ۵۰ سوال | تست با کوئری‌های آماده | Tech Lead |
| QG1.5 | کنترل دسترسی امنیتی | $100\%$ موارد تست | تست نفوذ ۱۰ سناریو | Security |
| QG1.6 | Audit Log | $100\%$ query‌ها ثبت‌شده | بررسی لاگ بعد از ۵۰ query | Security |
| QG1.7 | Fallback "نمی‌دانم" | $\geq 90\%$ موارد مناسب | تست ۲۰ سوال خارج از اسناد | Product Owner |
| QG1.8 | تأیید کاربران آزمایشی | امتیاز $\geq 3.5/5$ | فرم UAT از ۵ کاربر | Product Owner |
| QG1.9 | پایداری سیستم | بدون Crash در ۴۸ ساعت | Uptime Monitor | Backend Lead |

نتیجه Gate 1:
  ✅ QG1.1 تا QG1.6 همه موفق → Demo به مدیریت + Phase 2 شروع
  ⚠️ QG1.1 یا QG1.2 ناموفق → تمدید ۲ Sprint (بدون Demo)
  ❌ QG1.5 یا QG1.6 ناموفق → Phase 2 متوقف، بازبینی امنیتی


---

## ۵. فاز دو — Intelligence & OCR

**بازه:** هفته ۲۱ تا ۳۲ | **تعداد Sprint:** 6 | **تیم:** هر دو تیم

---

### Milestoneهای Phase 2

#### M2.1 — OCR Pipeline فارسی (پایان هفته ۲۶)

هدف: اسناد اسکن‌شده هم قابل جستجو باشند

Sprint 21-22: OCR Engine
  ✦ PaddleOCR + Tesseract (fallback)
  ✦ روتر هوشمند: PDF متنی → PyMuPDF / اسکن → OCR
  ✦ Post-processing فارسی روی خروجی OCR
  ✦ کیفیت‌سنجی خودکار (Confidence Score)

Sprint 23-24: بهبود جستجو
  ✦ Query Rewriting (بازنویسی سوال برای بهتر جستجو شدن)
  ✦ Re-ranking پیشرفته (Cross-Encoder)
  ✦ Contextual Compression


**Quality Check M2.1:**

| معیار | حد قابل قبول |
|---|---|
| دقت OCR فارسی | $\geq 85\%$ روی ۵۰ سند اسکن‌شده نمونه |
| روتر صحیح تشخیص می‌دهد | $\geq 95\%$ صحت تشخیص نوع سند |
| Recall بعد از Query Rewriting | بهبود $\geq 10\%$ نسبت به M1.2 |

---

#### M2.2 — Agent + DSPy + Feedback (پایان هفته ۳۲)

هدف: سیستم هوشمندتر، بهبود مستمر

Sprint 25-26: Agent اولیه (LangGraph)
  ✦ Multi-step Reasoning برای سوالات پیچیده
  ✦ Self-correction: اگر جواب ضعیف → دوباره جستجو
  ✦ ۵ سناریو مستند و تست‌شده

Sprint 27-28: DSPy Optimization
  ✦ Prompt‌های کلیدی با DSPy کامپایل شدند
  ✦ بهبود دقت پاسخ بدون تغییر Architecture
  ✦ مقایسه Before/After ثبت شد

Sprint 29-30: Feedback + Monitoring
  ✦ Thumbs Up/Down در UI
  ✦ Feedback در PostgreSQL ذخیره و قابل گزارش
  ✦ Dashboard: Latency + Token/s + Error Rate
  ✦ Alert: اگر Error Rate > 5% → هشدار خودکار


**Quality Check M2.2:**

| معیار | حد قابل قبول |
|---|---|
| Agent سوالات چندگامی حل می‌کند | ۵ سناریو تست با نتیجه موفق |
| بهبود DSPy روی دقت | $\geq 15\%$ بهبود نسبت به Prompt دستی |
| Feedback Loop ثبت می‌شود | $100\%$ Click‌ها در DB |
| Dashboard زنده است | Latency + Error Rate نمایش داده می‌شود |

---

### Quality Gates — Phase 2

> **Gate 2 (پایان هفته ۳۲):** تصمیم درباره ورود به Enterprise Hardening.

| # | معیار سنجش | حد قابل قبول | روش اندازه‌گیری | تصمیم‌گیرنده |
|---|---|---|---|---|
| QG2.1 | دقت OCR فارسی | $\geq 85\%$ | تست روی ۵۰ سند اسکن‌شده نمونه | Tech Lead |
| QG2.2 | بهبود Recall بعد از Query Rewriting | $\geq 10\%$ نسبت به Phase 1 | مقایسه معیار ثبت‌شده | Backend Lead |
| QG2.3 | Agent سناریوهای چندگامی | ۵ سناریو موفق | اجرای Test Suite | Tech Lead |
| QG2.4 | بهبود DSPy | $\geq 15\%$ بهبود دقت | مقایسه Before/After | ML Dev |
| QG2.5 | Feedback Loop فعال | $100\%$ ثبت در DB | بررسی لاگ بعد از ۱۰۰ Feedback | Backend Lead |
| QG2.6 | Dashboard Monitoring | Latency + Error Rate زنده | بررسی Grafana | DevOps |
| QG2.7 | پایداری کلی سیستم | بدون Crash در ۷۲ ساعت | Uptime Monitor | Backend Lead |
| QG2.8 | دقت پاسخ کلی (با OCR) | $\geq 80\%$ | ارزیابی ۳۰ سوال (شامل اسناد اسکن) | Product Owner |

نتیجه Gate 2:
  ✅ همه موفق → Phase 3 شروع می‌شود
  ⚠️ QG2.1 یا QG2.2 ناموفق → تمدید ۱ Sprint برای بهبود OCR/Search
  ❌ QG2.7 ناموفق → توقف، بررسی معماری


---

## ۶. فاز سه — Enterprise Hardening

**بازه:** هفته ۳۳ تا ۴۰+ | **تعداد Sprint:** 4+ | **تیم:** هر دو تیم + IT

---

### Milestoneهای Phase 3

#### M3.1 — Security + Load Test (پایان هفته ۳۶)

هدف: سیستم در برابر فشار و حملات مقاوم است

Sprint 33-34: Security Hardening
  ✦ Penetration Test (OWASP Top 10 سازگار با محیط داخلی)
  ✦ رفع آسیب‌پذیری‌های یافت‌شده
  ✦ بررسی Audit Log با تیم امنیت سازمان
  ✦ Network Isolation Verification

Sprint 35-36: Performance + Load Test
  ✦ Load Test: ۲۰ کاربر همزمان
  ✦ Stress Test: نقطه شکست سیستم
  ✦ بهینه‌سازی بر اساس نتایج
  ✦ SLA رسمی مستند شد


**Quality Check M3.1:**

| معیار | حد قابل قبول |
|---|---|
| آسیب‌پذیری بحرانی | صفر |
| آسیب‌پذیری متوسط | $\leq 3$ (با Plan رفع) |
| پایداری با ۲۰ کاربر همزمان | Uptime $\geq 99\%$ |
| زمان پاسخ با ۲۰ کاربر | $P_{95} \leq 45$ ثانیه |

---

#### M3.2 — LLMOps + Production Ready (پایان هفته ۴۰)

هدف: تیم IT سیستم را مستقلاً اداره کند

Sprint 37-38: LLMOps + Update Protocol
  ✦ فرآیند رسمی آپدیت مدل از HDD (با Rollback)
  ✦ Runbook عملیاتی (راهنمای IT)
  ✦ فرآیند Reindex اسناد جدید

Sprint 39-40: مستندسازی + آموزش
  ✦ User Manual فارسی
  ✦ Admin Panel برای مدیریت اسناد
  ✦ آموزش تیم IT (دو جلسه ۳ ساعته)
  ✦ آموزش کاربران کلیدی
  ✦ Handover Document


**Quality Check M3.2:**

| معیار | حد قابل قبول |
|---|---|
| تیم IT بدون کمک توسعه آپدیت اجرا کرد | یک Rehearsal موفق |
| Runbook کامل است | تأیید Tech Lead + IT |
| آموزش کاربران انجام شد | $\geq 80\%$ رضایت در فرم |
| Admin Panel کار می‌کند | تست توسط یک Admin کاربر |

---

### Quality Gates — Phase 3

> **Gate 3 (پایان هفته ۴۰):** تصمیم Production Release.

| # | معیار سنجش | حد قابل قبول | روش اندازه‌گیری | تصمیم‌گیرنده |
|---|---|---|---|---|
| QG3.1 | Security Audit | بدون آسیب‌پذیری بحرانی | گزارش Penetration Test | امنیت سازمان |
| QG3.2 | Load Test (۲۰ کاربر همزمان) | Uptime $\geq 99\%$ در ۴ ساعت | ابزار Load Test | Backend Lead |
| QG3.3 | زمان پاسخ تحت بار | $P_{95} \leq 45$ ثانیه | اندازه‌گیری در Load Test | Backend Lead |
| QG3.4 | تیم IT مستقل عمل می‌کند | Rehearsal بدون کمک توسعه | مشاهده مستقیم | Tech Lead |
| QG3.5 | User Manual کامل و تأیید شده | تأیید نماینده کاربران | بررسی مستند | Product Owner |
| QG3.6 | آموزش کاربران کلیدی | $\geq 80\%$ رضایت | فرم ارزیابی | Product Owner |
| QG3.7 | Rollback مدل آزمایش شده | موفق در کمتر از ۳۰ دقیقه | Rehearsal | Backend Lead |
| QG3.8 | دقت پاسخ نهایی | $\geq 80\%$ | ارزیابی ۵۰ سوال | کارفرما |

نتیجه Gate 3:
  ✅ همه موفق → Production Release 🚀
  ⚠️ QG3.1 ناموفق → تعلیق تا رفع مشکل امنیتی
  ⚠️ QG3.2 یا QG3.3 ناموفق → تمدید ۱ Sprint بهینه‌سازی
  ❌ QG3.8 < 75% → بازبینی معماری RAG


---

## ۷. نمای یکپارچه — همه Milestone و Gate

هفته  │  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
──────┼──────────────────────────────────────────────────────────────────────────────
Ph.0  │  ████████████████
Ph.1  │                  ████████████████████████████████████████████████████████████
──────┼──────────────────────────────────────────────────────────────────────────────
M     │       M0.1  M0.2                     M1.1                          M1.2
Gate  │                 [G0]
──────┴──────────────────────────────────────────────────────────────────────────────

هفته  │ 20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40
──────┼──────────────────────────────────────────────────────────────────────────────────
Ph.1  │ ██
Ph.2  │    ████████████████████████████████████████████████████████████
Ph.3  │                                                  ████████████████████████████████
──────┼──────────────────────────────────────────────────────────────────────────────────
M     │ M1.3                         M2.1                    M2.2    M3.1          M3.2
Gate  │  [G1]                                                  [G2]            [G3→🚀]


---

## ۸. ریسک هر Gate و استراتژی مقابله

| Gate | ریسک اصلی | احتمال | تأثیر | پیشگیری |
|---|---|---|---|---|
| **Gate 0** | مدل GGUF دیر می‌رسد | متوسط | بالا | سفارش مدل قبل از Sprint 1 |
| **Gate 0** | GPU Passthrough کار نمی‌کند | کم | بالا | تست GPU در روز اول Phase 0 |
| **Gate 1** | دقت $< 75\%$ | متوسط | بالا | ارزیابی دستی هر Sprint |
| **Gate 1** | کنترل دسترسی شکست می‌خورد | کم | بحرانی | Security Test در Sprint 13 |
| **Gate 2** | OCR فارسی $< 85\%$ | بالا | متوسط | تست OCR روی نمونه در Sprint 21 |
| **Gate 2** | Agent پیچیدگی بالاست | متوسط | متوسط | سناریوهای ساده اول |
| **Gate 3** | تیم IT آماده نیست | متوسط | بالا | آموزش از Sprint 37 |
| **Gate 3** | Security Audit ناموفق | کم | بحرانی | Security Review مداوم |

---

## ۹. تعریف "Done" برای هر سطح

تعریف Done در سطح Task:
  ✅ کد نوشته شد
  ✅ Unit Test نوشته شد (Coverage ≥ 70%)
  ✅ Code Review توسط همتا
  ✅ CI Pipeline موفق

تعریف Done در سطح Sprint:
  ✅ همه Task‌های Sprint Done هستند
  ✅ Sprint Review برگزار شد
  ✅ مستند فنی به‌روز شد
  ✅ هیچ Bug بحرانی باز نیست

تعریف Done در سطح Milestone:
  ✅ همه خروجی‌های اجباری Milestone موجود است
  ✅ Quality Check Milestone پاس شد
  ✅ Tech Lead تأیید کرد

تعریف Done در سطح Gate:
  ✅ همه معیارهای Quality Gate پاس شدند
  ✅ گزارش مکتوب تهیه شد
  ✅ تصمیم‌گیرنده امضا کرد


---

## ۱۰. خلاصه اجرایی (Executive Summary)

> **برای مدیریت ارشد**

**SINA** در ۴ فاز با **۱۳ Milestone** و **۴ نقطه تصمیم کلیدی (Gate)** توسعه می‌یابد:

| فاز | بازه | هدف | Gate |
|---|---|---|---|
| **Phase 0** | هفته ۱-۴ | زیربنای فنی آفلاین | Gate 0: محیط آماده |
| **Phase 1** | هفته ۵-۲۰ | سیستم RAG کامل + MVP Demo | Gate 1: مدیریت ارشد |
| **Phase 2** | هفته ۲۱-۳۲ | OCR + Agent + بهینه‌سازی | Gate 2: Tech Lead |
| **Phase 3** | هفته ۳۳-۴۰ | امنیت + مستندسازی + Production | Gate 3: کارفرما |

هیچ فازی بدون **تأیید صریح Gate** شروع نمی‌شود.

---

## ✅ وضعیت مستند

نسخه:        2.0 (ارتقا از 1.0 — افزوده شد: Milestone + Quality Gate)
تاریخ:       1404/12/04
وضعیت:       پیش‌نویس — در انتظار تأیید
مرحله بعد:   Sprint Plan (Phase 0 + Phase 1)


---

> **آماده برای بررسی هستم.**
> هر بخشی که نیاز به اصلاح یا تغییر دارد مشخص کنید.
> پس از تأیید، **مستند دوم — Sprint Plan** را آغاز می‌کنیم.v