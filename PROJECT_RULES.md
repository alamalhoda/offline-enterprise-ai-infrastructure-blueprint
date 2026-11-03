# قوانین پروژه (Project Rules)

## Single Source of Truth (SSOT)

**منبع واحد حقیقت:** GitHub Repository — شاخه `main`  
آدرس ریپوزیتوری:  
https://github.com/salimusavi02/offline-enterprise-ai-infrastructure-blueprint

### جریان کار استاندارد (Workflow)

1. **تغییرات ابتدا در فایل‌های پروژه (artifacts)** اعمال می‌شود.  
   مسیر: `/home/workdir/artifacts`

2. **قبل از هر push به GitHub:**
   - وضعیت ریموت بررسی شود.
   - آخرین تغییرات ریموت **pull** شوند تا از conflict جلوگیری شود.
   - در صورت وجود تغییر جدید در ریموت، آن‌ها با تغییرات محلی هماهنگ شوند.

3. پس از بررسی و **تأیید کاربر**، تغییرات به GitHub **commit** و **push** می‌گردند.

### اصول کلیدی

- هیچ تغییری نباید فقط در یکی از دو محل (artifacts یا GitHub) باقی بماند.
- GitHub (`main`) همیشه منبع واحد حقیقت است.
- قبل از push، حتماً pull انجام شود.

---

**تاریخ توافق:** ۱۴۰۴/۰۸/۱۲ (2026-11-03)  
**وضعیت:** تأییدشده توسط کاربر و ثبت در حافظه پروژه
