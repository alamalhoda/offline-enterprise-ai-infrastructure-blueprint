# Version: 1.0
# Updated: ۱۴۰۴/۰۸/۱۹ (2026-11-10)

"""
test_normalization_vectors.py
Test Vectorهای قطعی برای قرارداد norm-v1.0 (ADR-011: قرارداد نرمال‌سازی فارسی).

هر وکتور شامل (نام، ورودی، خروجی منتظره، مرجع قانون) است و决赛اً
از سه noir invariant هم محافظت می‌کند:
  1. خروجی دقیقاً برابرExpected است.
  2. ZWNJ (U+200C) حفظ شده است (حذف/تبدیل-به-space نشده).
  3. خروجی معکوس ورودی نیست (قانون ممنوعیت معکوس‌سازی).

اجرای pytest:
    pytest test_normalization_vectors.py -v

اجرای self-contained بدون pytest:
    python test_normalization_vectors.py
"""

from __future__ import annotations

import sys

try:
    import pytest  # type: ignore
except Exception:  # pragma: no cover - pytest may be absent in air-gapped env
    pytest = None

from normalization import (  # noqa: E402
    CONTRACT_VERSION,
    ZWNJ,
    assert_zwnj_preserved,
    is_reversed,
    normalize,
    normalize_query,
)

# هر ردیف: (نام وکتور، ورودی، خروجی منتظره، مرجع قانون norm-v1.0)
TEST_VECTORS: list[tuple[str, str, str, str]] = [
    (
        "TV-01",
        "يوجد",
        "یوجد",
        "U+064A (ي عربى) -> U+06CC (ي فارسى) — نگاشت اجباري yeh",
    ),
    (
        "TV-02",
        "كتاب",
        "کتاب",
        "U+0643 (ك عربى) -> U+06A9 (ك فارسى) — نگاشت اجباري kaf",
    ),
    (
        "TV-03",
        "ي كتاب كود",
        "ی کتاب کود",
        "ترکیبی نگاشت yeh +kaf در یک جمله",
    ),
    (
        "TV-04",
        f"می{ZWNJ}رویم",
        f"می{ZWNJ}رویم",
        "ZWNJ (U+200C) حفظ می‌گردد؛ حذف نمی‌شود",
    ),
    (
        "TV-05",
        f"می{ZWNJ}رویم",
        f"می{ZWNJ}رویم",
        "ZWNJ به space تبدیل نمی‌شود (بقای U+200C تضمین‌شده است)",
    ),
    (
        "TV-06",
        "۱۲۳۴۵",
        "12345",
        "اعداد فارسی (۰-۹) -> اعداد انگلیسی (0-9)",
    ),
    (
        "TV-07",
        "e\u0301",
        "é",
        "قالب يونيكد NFC (تکثیر چیدمان Canonical)",
    ),
    (
        "TV-08",
        "این متن معکوس نیست.",
        "این متن معکوس نیست.",
        "ممنوعیت معکوس کردن متن (خروجی = ورودی، ترتیب کاراکترها حفظ‌شده)",
    ),
    (
        "TV-09",
        f"ي كتاب ۱۲۳ می{ZWNJ}رويم كود",
        f"ی کتاب 123 می{ZWNJ}رویم کود",
        "کلیه قوانین در یک ورودی: yeh+kaf+عدد+ZWNJ+ترتیب کاراکترها",
    ),
    (
        "TV-10",
        "",
        "",
        "رشته خالی پایدار است (edge case ورودی خالی)",
    ),
]


def _check_vector(name: str, text: str, expected: str, rule_ref: str) -> None:
    actual = normalize(text)
    assert (
        actual == expected
    ), f"{name} ناکام [{rule_ref}]\n  input:    {text!r}\n  expected: {expected!r}\n  actual:   {actual!r}"
    assert_zwnj_preserved(text, actual)
    assert not is_reversed(actual, text), f"{name}: خروجی با ورودی معکوس است (ممنوع)"
    assert (
        normalize_query(text) == actual
    ), f"{name}: مسیر کوئری با مسیر ingest فرق می‌کند (قرارداد ingest+query یکسان)"
    print(f"PASS {name}: {text!r} -> {actual!r}  ({rule_ref})")


def run_all() -> int:
    print(f"قرارداد: {CONTRACT_VERSION}")
    for name, text, expected, rule_ref in TEST_VECTORS:
        _check_vector(name, text, expected, rule_ref)

    # ورودی None
    assert normalize(None) == ""
    assert normalize_query(None) == ""
    print("PASS None-input -> ''")

    print(f"\nهمه {len(TEST_VECTORS)} Test Vector norm-v1.0 با موفقیت اجرا شدند.")
    return 0


# ───pytest adapters (اگر pytest نصب باشد)───
if pytest is not None:

    @pytest.mark.parametrize(
        "name,text,expected,rule_ref",
        TEST_VECTORS,
        ids=[tv[0] for tv in TEST_VECTORS],
    )
    def test_norm_vector(name: str, text: str, expected: str, rule_ref: str) -> None:
        _check_vector(name, text, expected, rule_ref)

    def test_none_input() -> None:
        assert normalize(None) == ""
        assert normalize_query(None) == ""

    def test_contract_version() -> None:
        assert CONTRACT_VERSION == "norm-v1.0"


if __name__ == "__main__":
    sys.exit(run_all())
