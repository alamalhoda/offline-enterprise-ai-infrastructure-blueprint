# SINA — Secure Intelligent Network Assistant

## مدیریت ریسک و ارزیابی کیفیت

### Risk Register & QA Framework

| مورد | مقدار |
|------|--------|
| نسخه | 1.5 — Draft |
| تاریخ | بهمن ۱۴۰۴ / فوریه ۲۰۲۶ |
| وضعیت | Living Document — به‌روزرسانی در هر Sprint |
| مخاطب | تیم فنی / مدیریت ارشد / Product Owner |
| مرجع | هم‌راستا با **SINA_Roadmap_v1.5** و **SINA_SprintPlan**؛ Definition of Done و معیارهای کیفیت با نقشه راه و برنامه Sprint یکسان است. |

---

## ۱. ماتریس ارزیابی ریسک

ریسک‌ها بر اساس دو محور **احتمال وقوع** و **میزان تأثیر** ارزیابی می‌شوند. سطح ریسک از ضرب این دو محور به دست می‌آید:

| احتمال \ تأثیر | بسیار کم (1) | کم (2) | متوسط (3) | بالا (4) | بسیار بالا (5) |
|-----------------|--------------|--------|-----------|----------|----------------|
| **بسیار کم (1)** | 1 — پایین | 2 — پایین | 3 — پایین | 4 — متوسط | 5 — متوسط |
| **کم (2)** | 2 — پایین | 4 — متوسط | 6 — متوسط | 8 — بالا | 10 — بالا |
| **متوسط (3)** | 3 — پایین | 6 — متوسط | 9 — بالا | 12 — بحرانی | 15 — بحرانی |
| **بالا (4)** | 4 — متوسط | 8 — بالا | 12 — بحرانی | 16 — بحرانی | 20 — بحرانی |
| **بسیار بالا (5)** | 5 — متوسط | 10 — بالا | 15 — بحرانی | 20 — بحرانی | 25 — بحرانی |

**راهنما:** بحرانی = امتیاز ۱۲–۲۵ | بالا = امتیاز ۸–۱۱ | متوسط = امتیاز ۴–۷ | پایین = امتیاز ۱–۳

---

## ۲. Risk Register — ثبت ریسک‌ها

این جدول یک **Living Document** است و در هر Sprint Review به‌روزرسانی می‌شود. ریسک‌ها بر اساس سطح بحرانی بودن مرتب شده‌اند. *استراتژی‌های کاهش با بخش ۱۱ نقشه راه (SINA_Roadmap_v1.5) هم‌خوان هستند.*

| ID | دسته | ریسک | احتمال | تأثیر | سطح | استراتژی کاهش | مالک |
|----|------|------|--------|-------|-----|----------------|------|
| R-001 | فنی/NLP | دقت پردازش NLP فارسی پایین‌تر از انتظار (Recall < 70%) | ۴ — بالا | ۵ — بسیار بالا | بحرانی | Golden Query Set از Sprint 1 تعریف شود؛ Benchmark هر Sprint اجرا شود؛ Fallback به BM25-only در صورت افت | Backend Lead |
| R-002 | فنی/NLP | ZWNJ handling نادرست باعث شکست جملات فارسی در Chunking | ۵ — بسیار بالا | ۴ — بالا | بحرانی | PersianTextSplitter/EnterprisePersianNormalizer (Hazm + DadmaTools) پیاده‌سازی و تست شود؛ ۵۰۰ صفحه نمونه فارسی قبل از Deploy | Backend Lead |
| R-003 | سخت‌افزار | CPU Bottleneck در زمان Embedding اسناد حجیم | ۵ — بسیار بالا | ۳ — متوسط | بحرانی | Batch Processing شبانه (Cron Job)؛ Queue Priority؛ ONNX INT8 Quantization؛ Adaptive Batch Size | Backend Lead |
| R-004 | تیم | نبود تخصص ML/AI در تیم Backend | ۵ — بسیار بالا | ۴ — بالا | بحرانی | Cross-training در Sprint 1؛ مستندات فنی دقیق؛ Pair Programming؛ Spike Story هر فاز | Backend Lead |
| R-005 | معماری | Breaking Changes ابزارهای Haystack/LangChain/LlamaIndex | ۴ — بالا | ۴ — بالا | بحرانی | Hexagonal Architecture اجباری — همه ابزارها پشت Interface؛ Version Lock در requirements.txt؛ Upgrade فقط با Test | Backend Lead |
| R-006 | عملیاتی | Disk/RAM Overflow در Production بدون هشدار | ۳ — متوسط | ۵ — بسیار بالا | بحرانی | Prometheus Alert از Sprint 1 (مطابق نقشه راه: Observability از فاز ۱)؛ Retention Policy خودکار؛ Alerting برای RAM > 85% و Disk > 80% | Backend Lead |
| R-007 | امنیت | دسترسی غیرمجاز به اسناد محرمانه | ۲ — کم | ۵ — بسیار بالا | بالا | RBAC کامل از فاز ۳؛ ACL در سطح Document و Chunk؛ Audit Log برای تمام دسترسی‌ها (100% از Sprint 1)؛ JWT Expiry کوتاه | Backend Lead |
| R-008 | فنی/AI | Hallucination بالای LLM در پاسخ‌های فارسی | ۴ — بالا | ۳ — متوسط | بالا | Score Threshold برای Fallback (Score < 0.65 → 'یافت نشد' — مطابق Sprint Plan)؛ Citation در پاسخ؛ ارزیابی دستی ماهانه | Backend Lead |
| R-009 | داده | فساد Index در Qdrant بدون قابلیت بازیابی | ۲ — کم | ۵ — بسیار بالا | بالا | Weekly Snapshot خودکار؛ Rebuild-from-Source Pipeline آزمایش‌شده؛ RTO < 24 ساعت تأیید‌شده | Backend Lead |
| R-010 | معماری | Migration Zero-Downtime Index شکست بخورد | ۳ — متوسط | ۴ — بالا | بالا | Dual-Index Strategy (Old + New همزمان)؛ Alias Switching Atomic؛ Rollback خودکار در صورت A/B Fail | Backend Lead |
| R-011 | تیم | خروج کلیدی‌ترین Backend Developer از تیم | ۲ — کم | ۵ — بسیار بالا | بالا | مستندات Architecture Decision Record (ADR)؛ Knowledge Sharing Session هر ماه؛ Onboarding Guide | Backend Lead |
| R-012 | فنی | Performance Degradation با رشد Corpus (> 100K سند) | ۳ — متوسط | ۳ — متوسط | متوسط | IVF Index به جای HNSW برای Corpus بزرگ؛ Vector Compression (PQ)؛ Performance Test هر Phase | Backend Lead |
| R-013 | فنی/NLP | Embedding Drift تدریجی کاهش کیفیت بازیابی | ۳ — متوسط | ۳ — متوسط | متوسط | KS-Test ماهانه؛ Golden Set هر Sprint؛ Re-embedding Trigger در صورت Drift > 10% | Backend Lead |
| R-014 | عملیاتی | Docker Image Corruption در محیط Air-Gapped | ۲ — کم | ۴ — بالا | متوسط | SHA-256 تمام Image‌ها؛ Checksums نگهداری در Registry؛ دو نسخه از هر Image در Vault | Backend Lead |
| R-015 | زبانی | اسناد با رمزگذاری غیراستاندارد (نه UTF-8) خوانده نشوند | ۳ — متوسط | ۲ — کم | متوسط | MIME Detection و Encoding Detection اولیه؛ Fallback به chardet؛ Error در DLQ با لاگ مشخص | Backend Lead |
| R-016 | تیم | Sprint Velocity پایین‌تر از پیش‌بینی در ML Tasks | ۴ — بالا | ۲ — کم | متوسط | ۲۰% Buffer Capacity برای ML Tasks (مطابق Velocity Baseline در Sprint Plan)؛ Spike Story برای Research؛ MVP-first approach | Backend Lead |

---

## ۳. چارچوب QA — استراتژی کیفیت

با توجه به ساختار **Backend-Centric** تیم SINA، QA به صورت **embedded** در هر Developer پیاده‌سازی می‌شود. هیچ تیم QA مستقلی وجود ندارد — هر Developer مسئول تست کد خود است. *این رویکرد با نقشه راه و برنامه Sprint (QA جاسازی‌شده) سازگار است.*

### ۳.۱ هرم تست (Testing Pyramid)

| لایه تست | ابزار | درصد Coverage هدف | چه چیزی تست می‌شود |
|----------|--------|-------------------|---------------------|
| Unit Tests | pytest + unittest.mock | > 75% | توابع، کلاس‌ها، منطق Business بدون I/O |
| Integration Tests | pytest + Docker Compose | > 60% | تعامل سرویس‌ها: API → Queue → DB → Qdrant |
| Persian NLP Tests | pytest + custom fixtures | > 80% | Normalization، Chunking، Embedding دقت فارسی |
| E2E Tests | pytest + httpx | > 40% | Pipeline کامل از Upload تا Response |
| Performance Tests | locust (offline) | هر Phase | Latency، Throughput، CPU/RAM زیر Load |
| Golden Query Set | custom runner | هر Sprint | کیفیت بازیابی و Generation |

---

## ۴. فرآیندهای QA در Scrum

### ۴.۱ Definition of Ready (پیش‌شرط ورود Story به Sprint)

- Acceptance Criteria واضح و قابل اندازه‌گیری نوشته شده
- Scope مشخص است — Dev می‌داند دقیقاً چه باید بسازد
- Dependencies شناسایی شده‌اند
- Story Points تخمین زده شده
- آیا نیاز به Spike دارد مشخص شده

### ۴.۲ Definition of Done (معیارهای تکمیل هر Story)

*مطابق SINA_Roadmap_v1.5 (بخش ۱۰) و SINA_SprintPlan:*

- کد نوشته، Code Review شده توسط ≥ ۱ نفر دیگر
- Unit Test با Coverage **≥ 70%** نوشته شده
- Integration Test در Docker Compose موفق
- هیچ خطای Linting (flake8/black) در کد
- Logging مناسب برای **Audit** اضافه شده (Audit Coverage 100% از Sprint 1)
- مستند فنی مختصر (Docstring یا README بخش) اضافه شده
- در Branch develop بدون Conflict Merge شده
- برای Stories فارسی: تست با ۵۰ نمونه متن فارسی

### ۴.۳ Code Review Checklist

| # | معیار بررسی | Reviewer | وضعیت |
|---|--------------|-----------|--------|
| 1 | آیا هیچ import مستقیم از LangChain/LlamaIndex/Haystack در Domain Logic وجود دارد؟ | Backend Lead | ☐ |
| 2 | آیا PersianTextSplitter / EnterprisePersianNormalizer (Hazm + DadmaTools) برای تمام متون فارسی استفاده شده؟ | Backend Dev | ☐ |
| 3 | آیا Thread Count برای Llama.cpp <= Physical Core Count است؟ | Backend Dev | ☐ |
| 4 | آیا تمام خطاها Logged می‌شوند با سطح مناسب (ERROR/WARNING)? | Backend Dev | ☐ |
| 5 | آیا هیچ Secret/Password در کد Hard-code شده؟ | Backend Lead | ☐ |
| 6 | آیا ACL Checks در Retrieval Layer وجود دارد؟ | Backend Lead | ☐ |
| 7 | آیا Retry Logic و DLQ برای Task‌های ناموفق پیاده شده؟ | Backend Dev | ☐ |
| 8 | آیا Batch Size برای CPU بهینه شده (نه بزرگتر از ۳۲)؟ | Backend Dev | ☐ |
| 9 | آیا SHA-256 Verification برای مدل‌های لود شده انجام می‌شود؟ | Backend Lead | ☐ |
| 10 | آیا Unit Test برای Edge Case‌های فارسی (ZWNJ، ی/ک عربی) نوشته شده؟ | Backend Dev | ☐ |

---

## ۵. QA ویژه زبان فارسی

بزرگترین چالش کیفی SINA پردازش صحیح زبان فارسی است. این بخش Test Case‌های اختصاصی فارسی را تعریف می‌کند. *ابزارهای مرجع در نقشه راه: Hazm + DadmaTools، Persian-aware Chunking، NFKC Normalization.*

### ۵.۱ Test Caseهای اجباری NLP فارسی

| # | Test Case | ورودی | خروجی مورد انتظار |
|----|-----------|--------|---------------------|
| TC-01 | یکسان‌سازی ی/ک عربی-فارسی | «كتاب» (ک عربی) | «کتاب» (ک فارسی) — تبدیل خودکار |
| TC-02 | مدیریت نیم‌فاصله (ZWNJ) | «می گویم» (بدون نیم‌فاصله) | «می‌گویم» (با نیم‌فاصله صحیح) |
| TC-03 | عدم شکست جمله فارسی از وسط | جمله ۱۵۰ توکنی در Chunk 128 توکنی | جمله کامل حفظ شده، برش در مرز جمله |
| TC-04 | Overlap صحیح فارسی | سند ۱۰۰۰ کاراکتری با overlap 200 | ۲ جمله آخر Chunk قبلی در Chunk بعدی |
| TC-05 | جستجوی ZWNJ-aware | Query: «نیمفاصله» (بدون نیم‌فاصله) | نتیجه: اسنادی که «نیم‌فاصله» دارند پیدا می‌شوند |
| TC-06 | Embedding فارسی منسجم | دو جمله هم‌معنی با کلمات متفاوت | Cosine Similarity > 0.85 |
| TC-07 | کاراکتر کنترلی در متن | متن با کاراکترهای U+200C, U+200B اضافی | حذف شده، متن تمیز |
| TC-08 | اعداد فارسی-عربی | «۱۲۳» vs «123» | هر دو به یک نتیجه ختم می‌شوند |
| TC-09 | متن ترکیبی فارسی-انگلیسی | جمله: «The سیاست کلی است» | تشخیص زبان ترکیبی، Chunking حفظ هر دو |
| TC-10 | RTL در Filename | فایل با نام فارسی: «گزارش مالی.pdf» | Hash صحیح محاسبه، UTF-8 در PostgreSQL |

---

## ۶. قالب‌های Acceptance Criteria

برای یکپارچگی User Storyها، از این قالب‌های استاندارد استفاده می‌شود.

### ۶.۱ قالب Given-When-Then برای SINA

- **Given** [وضعیت اولیه سیستم]
- **When** [اقدام کاربر یا رویداد]
- **Then** [نتیجه مورد انتظار، قابل اندازه‌گیری]

**مثال برای Ingestion Layer:**

- **Given:** یک فایل PDF فارسی ۵۰ صفحه‌ای در پوشه watched قرار می‌گیرد  
- **When:** Directory Watcher تغییر را تشخیص می‌دهد  
- **Then:** در ۳۰ ثانیه Task در Queue قرار گرفته، SHA-256 محاسبه شده، Scan انجام شده، در PostgreSQL ثبت شده  

**مثال برای Query Flow:**

- **Given:** ۱۰۰۰ سند فارسی در سیستم index شده و کاربر با role Reader احراز هویت شده  
- **When:** سوال «مرخصی زایمان چقدر است؟» ارسال می‌شود  
- **Then:** در کمتر از ۴۵ ثانیه (هدف نقشه راه: ≤ 30 ثانیه)، پاسخ فارسی منسجم + شناسه سند منبع + امتیاز اطمینان برگشت داده می‌شود  

### ۶.۲ Non-Functional Acceptance Criteria

*آستانه‌ها با Quality Gateهای نقشه راه (QG1.x، QG2.x) و Success Metrics هم‌خوان هستند.*

| NFR Category | معیار اندازه‌گیری | آستانه قابل قبول |
|--------------|-------------------|-------------------|
| Performance | E2E Query Latency (P95) | < 45 ثانیه روی CPU (هدف Gate 1: ≤ 30 ثانیه) |
| Performance | Ingestion Throughput | > ۱۰ صفحه در دقیقه روی CPU 8-core |
| Reliability | Uptime | ≥ 99% در ساعات کاری |
| Reliability | Failed Task Rate | < 1% در حالت Normal Operation |
| Security | Unauthorized Access Attempts | 100% Rejected — هر Access بدون Token |
| Scalability | Concurrent Users | ≥ ۱۰ کاربر همزمان (فاز ۲)؛ ≥ ۲۰ پس از فاز ۳ بدون Degradation |
| Maintainability | Mean Time to Debug | < 2 ساعت با Logs موجود |
| Data Quality | Recall@5 (Persian) | > 70% حداقل؛ هدف ≥ 75% (Gate 1)؛ ایده‌آل > 85% |
| Offline Compliance | Internet Dependency | صفر — هیچ Request به خارج شبکه |

---

## ۷. مدیریت Bug و Incident

### ۷.۱ طبقه‌بندی Bug

| سطح | تعریف | SLA پاسخ | مثال |
|-----|--------|----------|------|
| P0 — بحرانی | سیستم کاملاً از کار افتاده | فوری — همان روز | Qdrant Down، PostgreSQL Corrupt، LLM Crash |
| P1 — بالا | Feature اصلی کار نمی‌کند | < ۲۴ ساعت | Ingestion متوقف، Query پاسخ نمی‌دهد، Auth شکست |
| P2 — متوسط | Feature جانبی مشکل دارد | < ۱ Sprint | Persian Chunking نادرست، Dashboard نمایش نمی‌دهد |
| P3 — پایین | بهبود یا Cosmetic Issue | Backlog | پیام خطا نامفهوم، Log ناقص، UI بهبود |

### ۷.۲ فرآیند Incident Response در Air-Gapped

1. **تشخیص:** Prometheus Alert یا گزارش کاربر  
2. **ارزیابی:** تعیین سطح (P0–P3) در ۱۵ دقیقه  
3. **Isolation:** جلوگیری از گسترش (P0: Maintenance Mode فعال)  
4. **تحلیل:** بررسی Jaeger Traces + Loki Logs  
5. **رفع:** اعمال Fix یا Rollback  
6. **تأیید:** اجرای Golden Query Set برای تأیید بازیابی  
7. **Post-Mortem:** مستندسازی در ظرف ۴۸ ساعت  

### ۷.۳ Post-Mortem Template

| بخش | محتوا |
|-----|--------|
| تاریخ و مدت | [تاریخ شروع] — [تاریخ پایان] — [مدت تأثیر] |
| خلاصه Incident | [توضیح مختصر: چه اتفاقی افتاد] |
| Timeline رویدادها | [زمان‌بندی دقیق تشخیص، تحلیل، رفع] |
| Root Cause | [علت ریشه‌ای — نه علت سطحی] |
| تأثیر بر کاربران | [چند کاربر، چه مدت، چه داده‌ای] |
| اقدامات انجام‌شده | [fix اعمال شده] |
| Action Itemها | [اقدامات پیشگیرانه با مالک و تاریخ] |
| ثبت در Risk Register | [آیا ریسک جدید شناسایی شد؟] |

---

*مستند: SINA Risk & QA v1.0 — Draft | هم‌راستا با SINA_Roadmap_v1.5 و SINA_SprintPlan | بهمن ۱۴۰۴ / فوریه ۲۰۲۶*
