Version: 1.5
Updated: ۱۴۰۴/۰۸/۱۶ (2026-11-07)

# SINA — Secure Intelligent Network Assistant

## LLMOps / MLOps Framework

### استقرار، نگهداری و نظارت مدل‌های AI در محیط Air-Gapped

| مورد | مقدار |
|------|--------|
| نسخه | 1.5 — Draft |
| تاریخ | بهمن ۱۴۰۴ / فوریه ۲۰۲۶ |
| محیط | Air-Gapped / CPU-Only / آفلاین کامل |
| مخاطب | Backend Team / ML Engineers / DevOps |
| مرجع | هم‌راستا با **RoadMap_1.md**، **SINA_SprintPlan** و **SINA_RiskQA**؛ مسیر Model Vault، معیارهای کیفیت و Observability با نقشه راه و برنامه Sprint یکسان است. |

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

### ۲.۲ ثبت و مدیریت مدل

- هر مدل با SHA-256، version، metadata و تاریخ ثبت می‌شود.
- فرآیند Manual Transfer از محیط آنلاین به Air-Gapped با تأیید Hash.

---

## ۳. فرآیند استقرار و به‌روزرسانی

- Staging → Production با Zero-downtime و Rollback Plan.
- Alias Switching برای مدل‌های Embedding و LLM.

---

## ۴. Observability و Monitoring

- متریک‌های محلی با Prometheus + Grafana.
- Embedding Drift Detection.
- Quality Metrics از Golden Query Set.

---

## ۵. Backup و Disaster Recovery

| جزء | RPO | RTO | اولویت |
|-----------|--------------------------------|---------------------|--------|
| PostgreSQL (Metadata) | ۱ ساعت | < ۲ ساعت | Critical |
| MinIO (Raw Files) | ۲۴ ساعت | < ۴ ساعت | High |
| Qdrant (Vector Index) | ۴۸ ساعت | < ۲۴ ساعت | Medium |
| Model Vault | N/A (ثابت) | < ۱ ساعت | High |
| Configs & Secrets | Real-time | < ۳۰ دقیقه | Critical |

### Backup Schedule

- روزانه: PostgreSQL + MinIO
- هفتگی: Qdrant + Model Vault
- ماهانه: Full + DR Test

---

## ۸. Continuous Evaluation — ارزیابی مستمر

### ۸.۱ ساختار Golden Query Set

- ۱۰۰ سوال فارسی از دامنه‌های مختلف سازمانی  
- ۳۰ سوال با اصطلاحات تخصصی  
- ۲۰ سوال چندمفهومی  
- ۲۰ سوال با کلمات نرمال‌سازی‌نشده  
- ۱۵ سوال انگلیسی یا ترکیبی  
- ۱۵ سوال edge case  

### ۸.۲ معیارهای ارزیابی و آستانه‌ها

| معیار | آستانه Fail | هدف | توضیح |
|-------|------|-------|-----|--------|
| Recall@5 | < 70% | > 85% | درصد سوالات که پاسخ درست در Top-5 است |
| MRR@10 | < 0.65 | > 0.80 | میانگین رتبه معکوس در Top-10 |
| NDCG@5 | < 0.60 | > 0.75 | کیفیت با وزن‌دهی رتبه |
| Hallucination Rate | > 20% | < 8% | درصد پاسخ‌های غیرواقعی |
| Not-Found Precision | < 80% | > 95% | وقتی پاسخ نیست، درستی تشخیص 'یافت نشد' |
| E2E Latency P95 | > 90s | < 30s | صدک ۹۵ زمان پاسخ کامل |

### ۸.۳ فرآیند Regression Gate

1. اجرای Golden Query Set به صورت خودکار  
2. مقایسه نتایج با Baseline  
3. اگر Metric بیش از ۳% افت کرده باشد → Merge مسدود می‌شود  
4. تحلیل دستی و رفع مشکل  
5. ثبت نتایج در evaluation_history  

---

*مستند: SINA LLMOps v1.0 — Draft | هم‌راستا با RoadMap_1.md، SINA_SprintPlan و SINA_RiskQA | بهمن ۱۴۰۴ / فوریه ۲۰۲۶*
