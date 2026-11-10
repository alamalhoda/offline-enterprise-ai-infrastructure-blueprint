# Version: 1.0
# Updated: ۱۴۰۴/۰۸/۱۹ (2026-11-10)

"""
norm-v1.0 — Persian Normalization Contract (ADR-011)
======================================================
ماژول gemeinsamen نرمال‌سازی فارسی برای بوم‌نقشه زیرساخت هوش مصنوعی سرنـو (SINA).
یک پیاده‌سازی واحد از قرارداد ADR-011 (Persian Normalization Contract,
نسخه norm-v1.0) است و باید هر دو مسیر ingest و query فراخوانی شود.

قوانین اجباری قرارداد norm-v1.0:
  * قالب يونيكد: NFC
  * نگاشت اجباري: U+064A (ي عربى) -> U+06CC (ي فارسى)
  * نگاشت اجباري: U+0643 (ك عربى)  -> U+06A9 (ك فارسى)
  * ZWNJ (U+200C) حفظ شود؛ حذف یا تبدیل به space ممنوع است
  * معکوس کردن متن: کاملاً ممنوع (خروجی هرگز معکوس نمی‌شود)
  * اعداد فارسی (۰-۹) -> اعداد انگلیسی (0-9)
  * واحد Chunk: توکن (پیش‌فرض فعلی 512 / overlap 50 تا تایید نهایی ADR-003)

تنها وابستگی: کتابخانه استاندارد Python (unicodedata). ديترمينستيك و
آسان-اجرایی آفلاین؛ هیچ کتابخانه NLP شخص سوم (مثل hazm) بخشی از قرارداد
نیست — توکین‌سازی جملات و فاصله‌نویسی املایی خارج از منطقى این ماژول هستند.
"""

from __future__ import annotations

import unicodedata

__version__ = "norm-v1.0"
CONTRACT_VERSION = "norm-v1.0"

UNICODE_FORM = "NFC"

# نگاشت‌های اجباري عربى -> فارسى (ADR-011 / norm-v1.0)
_ARABIC_TO_PERSIAN: dict[str, str] = {
    "\u064a": "\u06cc",   # ي (U+064A Arabic yeh)  -> ي (U+06CC Persian yeh)
    "\u0643": "\u06a9",   # ك (U+0643 Arabic kaf)  -> ک (U+06A9 Persian kaf)
}
_ARABIC_TO_PERSIAN_TABLE = str.maketrans(_ARABIC_TO_PERSIAN)

# ZWNJ (U+200C) حفظ شود: هرگز حذف نشود، هرگز به space تبدیل نشود.
ZWNJ = "\u200c"

# اعداد فارسی (۰-۹) -> اعداد انگلیسی (0-9)
_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
_ENGLISH_DIGITS = "0123456789"
_DIGIT_TABLE = str.maketrans(_PERSIAN_DIGITS, _ENGLISH_DIGITS)


def normalize(text: str | None) -> str:
    """قرارداد norm-v1.0 را روی *text* اعمال می‌کند.

    مراحل ديترمينستيك و پایدار:
      1. normalize به فرمت Unicode NFC
      2. نگاشت عربى -> فارسى (U+064A->U+06CC، U+0643->U+06A9)
      3. اعداد فارسی -> اعداد انگلیسی
      4. ZWNJ (U+200C) حفظ می‌گردد (بدون عملیات؛ بقای تضمین‌شده است)

    معکوس کردن متن انجام نمی‌شود؛ هر فراخوانی که خروجی معکوس بسازد،
    نقضِ قرارداد norm-v1.0 است.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError(f"normalize() expects str or None, got {type(text).__name__}")

    # 1. قالب يونيكد: NFC
    normalized = unicodedata.normalize(UNICODE_FORM, text)

    # 2. نگاشت اجباري عربى -> فارسى
    normalized = normalized.translate(_ARABIC_TO_PERSIAN_TABLE)

    # 3. اعداد فارسی -> اعداد انگلیسی
    normalized = normalized.translate(_DIGIT_TABLE)

    # 4. ZWNJ حفظ شده است (هیچ عملیات حذف/تبدیل-به-space انجام نمی‌شود)
    return normalized


def normalize_query(text: str | None) -> str:
    """نرمال‌سازی کوئری. مسیر ingest و query بر اساس ADR-011 ورژن‌بندی‌شده
    و یکسان است؛ بنابراین منطقیاً با normalize یکی است."""
    return normalize(text)


def zwnj_count(text: str) -> int:
    """تعداد کاراکتر ZWNJ (U+200C) در *text* را برمی‌گرداند."""
    return text.count(ZWNJ)


def assert_zwnj_preserved(before: str, after: str) -> None:
    """قاعده حفظ ZWNJ در norm-v1.0 را تأیید می‌کند.

    در صورت حذف یا تبدیل به space، AssertionError می‌دهد.
    """
    before_z = zwnj_count(before)
    after_z = zwnj_count(after)
    assert before_z == after_z, (
        f"حفظ ZWNJ نقض شد: قبل از نرمال‌سازی {before_z} ZWNJ، بعد از آن {after_z} "
        f"(قرارداد norm-v1.0 حذف یا تبدیل به space را ممنوع می‌دارد)"
    )


def is_reversed(text: str, reference: str) -> bool:
    """گارد قرارداد: True برمی‌گرداند اگر *text* معکوس کاراکتر-پذیر *reference* باشد
    (ممنوع در norm-v1.0)."""
    return text == reference[::-1] and text != reference


if __name__ == "__main__":  # pragma: no cover - quick manual smoke check
    smoketests = [
        ("ي كتاب كود 123", "ی کتاب کود 123"),
        (f"مي{ZWNJ}رويم", f"مي{ZWNJ}رويم"),
        ("۱۲۳", "123"),
        ("", ""),
    ]
    for inp, exp in smoketests:
        out = normalize(inp)
        assert out == exp, f"{inp!r} -> {out!r} (expected {exp!r})"
        assert_zwnj_preserved(inp, out)
    print("norm-v1.0 smoke check passed")
