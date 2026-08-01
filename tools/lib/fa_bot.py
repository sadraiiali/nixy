"""Persian orthography helpers ported from fa.wikipedia fa_bot.js (persianTools).

Upstream:
  https://fa.wikipedia.org/wiki/ویکی‌پدیا:ویرایشگر_خودکار/ابرابزار/fa_bot.js

Local reference dump: tools/lib/_fa_bot_upstream.js

Adapted for this repo:
- Python API (no MediaWiki / browser globals)
- Markdown protection is applied by tools.lib.fa_orthography
- Western digits are left alone by default (technical documentation)
"""

from __future__ import annotations

import re
from typing import Callable

ARABIC_DIGITS = "0123456789"
ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
HAMZA = "\u0654"
SIMILAR_PERSIAN = (
    "\u0643\uFB91\uFB90\uFB8F\uFB8E\uFEDC\uFEDB\uFEDA\uFED9"
    "\u0649\uFEEF\u064A\u06C1\u06D5\u06BE"
)
# Note: original had \uFEF0-\uFEF4 as a range; expand for character class safety
SIMILAR_PERSIAN_RANGE = "\uFEF0-\uFEF4"
VOWELS = "\u064B-\u0650\u0652\u0670"
PERSIAN_CHARACTERS = (
    "\u0621-\u0655\u067E\u0686\u0698\u06AF\u06A9\u0643\u06AA"
    "\uFED9\uFEDA\u06CC\uFEF1\uFEF2"
    + SIMILAR_PERSIAN
    + SIMILAR_PERSIAN_RANGE
)
PERSIAN_CHARACTERS_NO_VOWELS = (
    "\u0621-\u064A\u0653-\u0655\u067E\u0686\u0698\u06AF\u06A9\u0643\u06AA"
    "\uFED9\uFEDA\u06CC\uFEF1\uFEF2"
    + SIMILAR_PERSIAN
    + SIMILAR_PERSIAN_RANGE
)

PERSIAN_GLYPHS: dict[str, str] = {
    "\u200cه": "ﻫ",
    "ی\u200c": "ﻰﻲ",
    "أ": "ﺄﺃﺃ",
    "آ": "ﺁﺁﺂ",
    "إ": "ﺇﺈﺇ",
    "ا": "ﺍﺎ",
    "ب": "ﺏﺐﺑﺒ",
    "پ": "ﭖﭗﭘﭙ",
    "ت": "ﺕﺖﺗﺘ",
    "ث": "ﺙﺚﺛﺜ",
    "ج": "ﺝﺞﺟﺠ",
    "چ": "ﭺﭻﭼﭽ",
    "ح": "ﺡﺢﺣﺤ",
    "خ": "ﺥﺦﺧﺨ",
    "د": "ﺩﺪ",
    "ذ": "ﺫﺬ",
    "ر": "ﺭﺮ",
    "ز": "ﺯﺰ",
    "ژ": "ﮊﮋ",
    "س": "ﺱﺲﺳﺴ",
    "ش": "ﺵﺶﺷﺸ",
    "ص": "ﺹﺺﺻﺼ",
    "ض": "ﺽﺾﺿﻀ",
    "ط": "ﻁﻂﻃﻄ",
    "ظ": "ﻅﻆﻇﻈ",
    "ع": "ﻉﻊﻋﻌ",
    "غ": "ﻍﻎﻏﻐ",
    "ف": "ﻑﻒﻓﻔ",
    "ق": "ﻕﻖﻗﻘ",
    "ک": "ﮎﮏﮐﮑﻙﻚﻛﻜ",
    "گ": "ﮒﮓﮔﮕ",
    "ل": "ﻝﻞﻟﻠ",
    "م": "ﻡﻢﻣﻤ",
    "ن": "ﻥﻦﻧﻨ",
    "ه": "ﻩﻪﻫﻬ",
    "هٔ": "ﮤﮥ",
    "و": "ﻭﻮ",
    "ؤ": "ﺅﺅﺆ",
    "ی": "ﯼﯽﯾﯿﻯﻰﻱﻲﻳﻴ",
    "ئ": "ﺉﺊﺋﺌ",
    "لا": "ﻻﻼ",
    "لإ": "ﻹﻺ",
    "لأ": "ﻸﻷ",
    "لآ": "ﻵﻶ",
}

PERSIAN_PAST_VERBS = '(ارزید|افتاد|افراشت|افروخت|افزود|افسرد|افشاند|افکند|انباشت|انجامید|انداخت|اندوخت|اندود|اندیشید|انگاشت|انگیخت|انگیزاند|اوباشت|ایستاد|آراست|آراماند|آرامید|آرمید|آزرد|آزمود|آسود|آشامید|آشفت|آشوبید|آغازید|آغشت|آفرید|آکند|آگند|آلود|آمد|آمرزید|آموخت|آموزاند|آمیخت|آهیخت|آورد|آویخت|باخت|باراند|بارید|بافت|بالید|باوراند|بایست|بخشود|بخشید|برازید|برد|برید|بست|بسود|بسیجید|بلعید|بود|بوسید|بویید|بیخت|پاشاند|پاشید|پالود|پایید|پخت|پذیراند|پذیرفت|پراکند|پراند|پرداخت|پرستید|پرسید|پرهیزید|پروراند|پرورد|پرید|پژمرد|پژوهید|پسندید|پلاسید|پلکید|پناهید|پنداشت|پوسید|پوشاند|پوشید|پویید|پیچاند|پیچانید|پیچید|پیراست|پیمود|پیوست|تاباند|تابید|تاخت|تاراند|تازاند|تازید|تافت|تپاند|تپید|تراشاند|تراشید|تراوید|ترساند|ترسید|ترشید|ترکاند|ترکید|تکاند|تکانید|تنید|توانست|جَست|جُست|جست|جنباند|جنبید|جنگید|جهاند|جهید|جوشاند|جوشید|جوید|چاپید|چایید|چپاند|چپید|چراند|چربید|چرخاند|چرخید|چرید|چسباند|چسبید|چشاند|چشید|چکاند|چکید|چلاند|چلانید|چمید|چید|خاراند|خارید|خاست|خایید|خراشاند|خراشید|خرامید|خروشید|خرید|خزید|خشکاند|خشکید|خفت|خلید|خمید|خنداند|خندانید|خندید|خواباند|خوابانید|خوابید|خواست|خواند|خوراند|خورد|خوفید|خیساند|خیسید|داد|داشت|دانست|درخشانید|درخشید|دروید|درید|دزدید|دمید|دواند|دوخت|دوشید|دوید|دید|دیدم|راند|ربود|رخشید|رساند|رسانید|رست|رَست|رُست|رسید|رشت|رفت|رُفت|رقصاند|رقصید|رمید|رنجاند|رنجید|رندید|رهاند|رهانید|رهید|روبید|روفت|رویاند|رویید|ریخت|رید|ریسید|زاد|زارید|زایید|زد|زدود|زیست|سابید|ساخت|سپارد|سپرد|سپوخت|ستاند|ستد|سترد|ستود|ستیزید|سرایید|سرشت|سرود|سرید|سزید|سفت|سگالید|سنجید|سوخت|سود|سوزاند|شاشید|شایست|شتافت|شد|شست|شکافت|شکست|شکفت|شکیفت|شگفت|شمارد|شمرد|شناخت|شناساند|شنید|شوراند|شورید|طپید|طلبید|طوفید|غارتید|غرید|غلتاند|غلتانید|غلتید|غلطاند|غلطانید|غلطید|غنود|فرستاد|فرسود|فرمود|فروخت|فریفت|فشاند|فشرد|فهماند|فهمید|قاپید|قبولاند|کاست|کاشت|کاوید|کرد|کشاند|کشانید|کشت|کشید|کفت|کفید|کند|کوبید|کوچید|کوشید|کوفت|گَزید|گُزید|گایید|گداخت|گذارد|گذاشت|گذراند|گذشت|گرازید|گرایید|گرداند|گردانید|گردید|گرفت|گروید|گریاند|گریخت|گریست|گزارد|گزید|گسارد|گستراند|گسترد|گسست|گسیخت|گشت|گشود|گفت|گمارد|گماشت|گنجاند|گنجانید|گنجید|گندید|گوارید|گوزید|لرزاند|لرزید|لغزاند|لغزید|لمباند|لمدنی|لمید|لندید|لنگید|لهید|لولید|لیسید|ماسید|مالاند|مالید|ماند|مانست|مرد|مکشید|مکید|مولید|مویید|نازید|نالید|نامید|نشاند|نشست|نکوهید|نگاشت|نگریست|نمایاند|نمود|نهاد|نهفت|نواخت|نوردید|نوشاند|نوشت|نوشید|نیوشید|هراسید|هشت|ورزید|وزاند|وزید|یارست|یازید|یافت)'
PERSIAN_PRESENT_VERBS = '(ارز|افت|افراز|افروز|افزا|افزای|افسر|افشان|افکن|انبار|انباز|انجام|انداز|اندای|اندوز|اندیش|انگار|انگیز|انگیزان|اوبار|ایست|آرا|آرام|آرامان|آرای|آزار|آزما|آزمای|آسا|آسای|آشام|آشوب|آغار|آغاز|آفرین|آکن|آگن|آلا|آلای|آمرز|آموز|آموزان|آمیز|آهنج|آور|آویز|آی|بار|باران|باز|باش|باف|بال|باوران|بای|باید|بخش|بخشا|بخشای|بر|بَر|بُر|براز|بساو|بسیج|بلع|بند|بو|بوس|بوی|بیز|بین|پا|پاش|پاشان|پالا|پالای|پذیر|پذیران|پر|پراکن|پران|پرداز|پرس|پرست|پرهیز|پرور|پروران|پز|پژمر|پژوه|پسند|پلاس|پلک|پناه|پندار|پوس|پوش|پوشان|پوی|پیچ|پیچان|پیرا|پیرای|پیما|پیمای|پیوند|تاب|تابان|تاران|تاز|تازان|تپ|تپان|تراش|تراشان|تراو|ترس|ترسان|ترش|ترک|ترکان|تکان|تن|توان|توپ|جنب|جنبان|جنگ|جه|جهان|جو|جوش|جوشان|جوی|چاپ|چای|چپ|چپان|چر|چران|چرب|چرخ|چرخان|چسب|چسبان|چش|چشان|چک|چکان|چل|چلان|چم|چین|خار|خاران|خای|خر|خراش|خراشان|خرام|خروش|خز|خشک|خشکان|خل|خم|خند|خندان|خواب|خوابان|خوان|خواه|خور|خوران|خوف|خیز|خیس|خیسان|دار|درخش|درخشان|درو|دزد|دم|ده|دو|دوان|دوز|دوش|ران|ربا|ربای|رخش|رس|رسان|رشت|رقص|رقصان|رم|رنج|رنجان|رند|ره|رهان|رو|روب|روی|رویان|ریز|ریس|رین|زا|زار|زای|زدا|زدای|زن|زی|ساب|ساز|سای|سپار|سپر|سپوز|ستا|ستان|ستر|ستیز|سر|سرا|سرای|سرشت|سز|سگال|سنب|سنج|سوز|سوزان|شاش|شای|شتاب|شکاف|شکف|شکن|شکوف|شکیب|شمار|شمر|شناس|شناسان|شنو|شو|شور|شوران|شوی|طپ|طلب|طوف|غارت|غر|غلت|غلتان|غلط|غلطان|غنو|فرسا|فرسای|فرست|فرما|فرمای|فروش|فریب|فشار|فشان|فشر|فهم|فهمان|قاپ|قبولان|کار|کاه|کاو|کش|کَش|کُش|کِش|کشان|کف|کن|کوب|کوچ|کوش|گا|گای|گداز|گذار|گذر|گذران|گرا|گراز|گرای|گرد|گردان|گرو|گری|گریان|گریز|گز|گزار|گزین|گسار|گستر|گستران|گسل|گشا|گشای|گمار|گنج|گنجان|گند|گو|گوار|گوز|گوی|گیر|لرز|لرزان|لغز|لغزان|لم|لمبان|لند|لنگ|له|لول|لیس|ماس|مال|مان|مک|مول|موی|میر|ناز|نال|نام|نشان|نشین|نکوه|نگار|نگر|نما|نمای|نمایان|نه|نهنب|نواز|نورد|نوش|نوشان|نویس|نیوش|هراس|هست|هل|ورز|وز|وزان|یاب|یار|یاز)'
PERSIAN_COMPLEX_PAST = {'باز': 'آفرید|آمد|آموخت|آورد|ایستاد|تابید|جست|خواند|داشت|رساند|ستاند|شمرد|ماند|نمایاند|نهاد|نگریست|پرسید|گذارد|گرداند|گردید|گرفت|گشت|گشود|گفت|یافت', 'در': 'بر ?داشت|بر ?گرفت|آمد|آمیخت|آورد|آویخت|افتاد|افکند|انداخت|رفت|ماند|نوردید|کشید|گرفت', 'بر': 'آشفت|آمد|آورد|افتاد|افراشت|افروخت|افشاند|افکند|انداخت|انگیخت|تاباند|تابید|تافت|تنید|جهید|خاست|خواست|خورد|داشت|دمید|شمرد|نهاد|چید|کرد|کشید|گرداند|گردانید|گردید|گزید|گشت|گشود|گمارد|گماشت', 'فرو': 'آمد|خورد|داد|رفت|نشاند|کرد|گذارد|گذاشت', 'وا': 'داشت|رهاند|ماند|نهاد|کرد', 'ور': 'آمد|افتاد|رفت', 'یاد': 'گرفت', 'پدید': 'آورد', 'پراکنده': 'ساخت', 'زمین': 'خورد', 'گول': 'زد', 'لخت': 'کرد'}
PERSIAN_COMPLEX_PRESENT = {'باز': 'آفرین|آموز|آور|ایست|تاب|جو|خوان|دار|رس|ستان|شمار|مان|نمایان|نه|نگر|پرس|گذار|گردان|گرد|گشا|گو|گیر|یاب', 'در': 'بر ?دار|بر ?گیر|آمیز|آور|آویز|افت|افکن|انداز|مان|نورد|کش|گذر|گیر', 'بر': 'آشوب|آور|افت|افراز|افروز|افشان|افکن|انداز|انگیز|تابان|تاب|تن|جه|خواه|خور|خیز|دار|دم|شمار|نه|چین|کش|کن|گردان|گزین|گشا|گمار', 'فرو': 'خور|ده|رو|نشین|کن|گذار', 'وا': 'دار|رهان|مان|نه|کن', 'ور': 'افت|رو', 'یاد': 'گیر', 'پدید': 'آور', 'پراکنده': 'ساز', 'زمین': 'خور', 'گول': 'زن', 'لخت': 'کن'}


def normalize_zwnj(text: str) -> str:
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}] *)[\u200F\u200E]+( *[{PERSIAN_CHARACTERS}])",
        "\\1\u200c\\2",
        text,
    )
    text = re.sub(r"\u200c{2,}", "\u200c", text)
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}])¬(?=[{PERSIAN_CHARACTERS}])",
        "\\1\u200c",
        text,
    )
    text = re.sub(
        r"([۰-۹0-9إأةؤورزژاآدذ،؛,:«»\\/@#$٪×\*()ـ\-=|ء])\u200c",
        r"\1",
        text,
    )
    text = re.sub(r"\u200c([A-Za-z0-9_])", r"\1", text)
    text = re.sub(r"([A-Za-z0-9_])\u200c", r"\1", text)
    text = re.sub(
        rf"\u200c([{VOWELS}{ARABIC_INDIC_DIGITS}{PERSIAN_DIGITS}{HAMZA}])",
        r"\1",
        text,
    )
    text = re.sub(rf"([{ARABIC_INDIC_DIGITS}])\u200c", r"\1", text)
    text = re.sub(r"([A-Za-z0-9_])\u200c", r"\1", text)
    text = re.sub(
        r"\u200c([ء\n\s\[\]\.،«»:\(\)\؛\؟\?\;\$\!\@\-\=\+\\|])",
        r"\1",
        text,
    )
    text = re.sub(
        r"([\n\s\[\.،«»:\(\)\؛\؟\?\;\$\!\@\-\=\+\\|])\u200c",
        r"\1",
        text,
    )
    text = re.sub(r"\u200c(\]\][\s\n])", r"\1", text)
    text = re.sub(r"([\n\s]\[\[)\u200c", r"\1", text)
    return text


def to_standard_persian_characters(text: str) -> str:
    for standard, glyphs in PERSIAN_GLYPHS.items():
        text = re.sub(f"[{re.escape(glyphs)}]", standard, text)
    text = normalize_zwnj(text)
    for a, b in (
        ("ك", "ک"),
        ("ڪ", "ک"),
        ("ﻙ", "ک"),
        ("ﻚ", "ک"),
        ("ي", "ی"),
        ("ى", "ی"),
        ("ے", "ی"),
        ("ۍ", "ی"),
        ("ې", "ی"),
        ("ہ", "ه"),
        ("ە", "ه\u200c"),
        ("ھ", "ه"),
    ):
        text = text.replace(a, b)
    return text


def to_persian_digits(text: str) -> str:
    for i in range(10):
        text = text.replace(ARABIC_INDIC_DIGITS[i], PERSIAN_DIGITS[i])
        text = text.replace(ARABIC_DIGITS[i], PERSIAN_DIGITS[i])
    text = re.sub(rf"([{PERSIAN_DIGITS}]) ?%", r"\1٪", text)
    text = re.sub(
        rf"٪([{PERSIAN_DIGITS}]+(?:[.٬٫][{PERSIAN_DIGITS}]*)*)",
        r"\1٪",
        text,
    )
    text = re.sub(rf"([{PERSIAN_DIGITS}])\.(?=[{PERSIAN_DIGITS}])", r"\1٫", text)
    text = re.sub(rf"([{PERSIAN_DIGITS}])،(?=[{PERSIAN_DIGITS}])", r"\1٬", text)
    return text


def apply_orthography(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\uFEFF\u00AD]+", "", text)
    text = re.sub(
        r"[ \xA0\xAD\u1680\u180E\u2000-\u200D\u2028\u2029\u202F\u205F\u2060\u3000]+\n",
        "\n",
        text,
    )
    text = re.sub(r"\n[\t\u00A0]+", "\n", text)
    text = re.sub(
        r"[\u0020\u0085\u00A0\u180E\u2000-\u200A\u202F\u205F\u3000]",
        " ",
        text,
    )
    text = text.replace("\u0085", "")
    text = re.sub(r"[\u01C3\uFE15]", "!", text)
    text = re.sub(r"[\u02D0\u0589\u05C3\uA789]", ":", text)
    text = re.sub(r"[\u0338\u2044\u2215\u2571\u29F8\u3033\uFF0F]", "/", text)
    text = text.replace("\u05F4", '"')
    text = re.sub(r"[\u06D4\u0701\uFF0E\uFF61]", ".", text)
    text = text.replace("\u3014", "(").replace("\u3015", ")")
    # Project style (nix notes): ezafe after heh is ه + ZWNJ + ی, not hamza (هٔ).
    # Upstream fa_bot prefers هٔ; we invert that for this repo.
    text = re.sub(r"[ۂۀ](?![\s\n])", "ه\u200cی ", text)
    text = re.sub(r"ه[\u200c\u200e\s]*[ءٔ]([\s\n]|$)", "ه\u200cی\\1", text)
    text = re.sub(r"(ۀ|هٓ)", "ه\u200cی", text)
    # Normalize bare heh+hamza ezafe (هٔ) → ه‌ی
    text = text.replace("ه\u0654", "ه\u200cی")
    text = re.sub(r"ه\u200c[ئی]ی", "ه\u200cای", text)
    text = re.sub(r"([\u200c\u200e])([\s\n])", r"\2", text)
    text = re.sub(r"([\s\n])([\u200c\u200e])", r"\1", text)
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}{VOWELS}{HAMZA}])(\s)([{VOWELS}{HAMZA}])",
        r"\1\3\2",
        text,
    )
    text = re.sub(rf"([{VOWELS}{HAMZA}]){{2,}}", r"\1", text)
    text = text.replace("ئء", "یء").replace("أء", "اء").replace("ؤء", "ؤ")
    text = re.sub(r"سؤ ?استفاده", "سوءاستفاده", text)
    text = re.sub(
        r"درباره (ام|ات|اش|مان|تان|شان|ای)(\s|$)",
        "درباره\u200c\\1\\2",
        text,
    )
    text = text.replace("درباره ", "درباره\u200cی ")
    text = re.sub(
        rf"صفحه(\s|)([{PERSIAN_DIGITS}]+)(\n|\.|\,|\||\<)",
        "صفحه\u200cی \\2\\3",
        text,
    )
    return text


def _complex_verbs_apply_zwnj(text: str) -> str:
    for x, y in PERSIAN_COMPLEX_PAST.items():
        text = re.sub(
            rf"(^|[^{PERSIAN_CHARACTERS}])({re.escape(x)}) ?(می|نمی|)( |\u200c|)(ن|)({y})(م|ی|یم|ید|ند|ه|ن|)($|[^{PERSIAN_CHARACTERS}])",
            "\\1\\2\u200c\\3\u200c\\5\\6\\7\\8",
            text,
        )
    for x, y in PERSIAN_COMPLEX_PRESENT.items():
        text = re.sub(
            rf"(^|[^{PERSIAN_CHARACTERS}])({re.escape(x)}) ?(می|نمی|)( |\u200c|)(ن|)({y})(م|ی|د|یم|ید|ند|ن)($|[^{PERSIAN_CHARACTERS}])",
            "\\1\\2\u200c\\3\u200c\\5\\6\\7\\8",
            text,
        )
    return text


def apply_zwnj(text: str) -> str:
    text = _complex_verbs_apply_zwnj(text)
    text = normalize_zwnj(text)
    text = re.sub(
        rf"(^|[^{PERSIAN_CHARACTERS}])(می|نمی) ?{PERSIAN_PAST_VERBS}"
        rf"(م|ی|یم|ید|ند|ه|)($|[^{PERSIAN_CHARACTERS}])",
        "\\1\\2\u200c\\3\\4\\5",
        text,
    )
    text = re.sub(
        rf"(^|[^{PERSIAN_CHARACTERS}])(می|نمی) ?{PERSIAN_PRESENT_VERBS}"
        rf"(م|ی|د|یم|ید|ند)($|[^{PERSIAN_CHARACTERS}])",
        "\\1\\2\u200c\\3\\4\\5",
        text,
    )
    text = re.sub(
        rf"(^|[^{PERSIAN_CHARACTERS}])(ن|){PERSIAN_PAST_VERBS}"
        rf"ه (ام|ای|ایم|اید|اند|است)($|[^{PERSIAN_CHARACTERS}])",
        "\\1\\2\\3ه\u200c\\4\\5",
        text,
    )
    text = re.sub(
        rf"(^|[^{PERSIAN_CHARACTERS}])(می|نمی) ?(دان)(م|د|یم|ید|ند)($|[^{PERSIAN_CHARACTERS}])",
        "\\1\\2\u200c\\3\\4\\5",
        text,
    )
    text = re.sub(r"(\s)(می|نمی) ?توان", "\\1\\2\u200cتوان", text)
    text = re.sub(r" ها([\]\.،:»\)\s]|'{2,3}|={2,})", "\u200cها\\1", text)
    text = re.sub(
        r" ها(ی|یی|یم|یت|یش|ی?مان|ی?تان|ی?شان)([\]\.،:»\)\s])",
        "\u200cها\\1\\2",
        text,
    )
    text = text.replace("هها", "ه\u200cها")
    text = re.sub(r" ترین([\]\.،:»\)\s]|'{2,3}|={2,})", "\u200cترین\\1", text)
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]ی) تبار([^{PERSIAN_CHARACTERS}])",
        "\\1\u200cتبار\\2",
        text,
    )
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]ی) شناس([^{PERSIAN_CHARACTERS}])",
        "\\1\u200cشناس\\2",
        text,
    )
    text = re.sub(r"(^\u200c|\u200c$)", "", text, flags=re.M)
    text = re.sub(r"ا\sً", "اً", text)
    text = text.replace(" که\u200cای ", " که ای ")
    text = text.replace("می\u200cستری", "میستری")
    text = re.sub(
        rf"می\u200cگوی($|[^{PERSIAN_CHARACTERS}\u200c])",
        r"میگوی\1",
        text,
    )
    text = re.sub(
        rf"می\u200cدوی($|[^{PERSIAN_CHARACTERS}\u200c])",
        r"میدوی\1",
        text,
    )
    return text


def punctuation(text: str) -> str:
    """Markdown-safer subset of upstream persianTools.punctuation.

    Intentionally does **not**:
    - insert spaces into relative paths (``./``, ``../``)
    - convert bare ``...`` in ASCII/code contexts to ellipsis
    - strip spaces before ``.`` when it starts a path component
    """
    text = text.replace("ː", ":")
    text = re.sub(rf"([{PERSIAN_CHARACTERS}])[ ]*[?]", r"\1؟", text)
    text = re.sub(rf"([{PERSIAN_CHARACTERS}])[ ]*[;]", r"\1؛ ", text)
    text = re.sub(rf"([{PERSIAN_CHARACTERS}])(]]|»|)[ ]*[,]", r"\1\2، ", text)
    text = re.sub(r"(،|؛|؟)  ", r"\1 ", text)
    text = text.replace("\r", "")
    # Collapse repeated spaces between non-space chars (preserve list indent style lightly)
    text = re.sub(r"(?<=\S) {2,}(?=\S)", " ", text)
    # Space after Persian punctuation marks (not ASCII ".")
    text = re.sub(
        r"([،\؛\؟»])([^\s\.\(\)«»\"\[\]<>\dA-Za-z_/\{\}\|۰۱۲۳۴۵۶۷۸۹'])",
        r"\1 \2",
        text,
    )
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]+|\]|\)|»)([؟،؛!])([{PERSIAN_CHARACTERS}{PERSIAN_DIGITS}]+|\[|\(|«)",
        r"\1\2 \3",
        text,
    )
    # Space after full stop only when both sides are Persian
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}])\.([{PERSIAN_CHARACTERS}])",
        r"\1. \2",
        text,
    )
    text = re.sub(r"([\(\«]) ", r"\1", text)
    text = re.sub(r" ([\)\»])", r"\1", text)
    text = re.sub(r"([^ \(\[\|\r\n>'])(«)", r"\1 \2", text)
    text = re.sub(r" +\( +", " (", text)
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]|\]|») *\( *(?=[{PERSIAN_CHARACTERS}])(?!ها\)|ان\))",
        r"\1 (",
        text,
    )
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]) *\) *(?=[{PERSIAN_CHARACTERS}]|\[|«)",
        r"\1) ",
        text,
    )
    text = re.sub(r"\n\s{1,}\n", "\n\n", text)
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]), ?(?=[{PERSIAN_CHARACTERS}])",
        r"\1، ",
        text,
    )
    text = re.sub(r"(؛)(([\s]+)?[\.،؛:!؟\-…])", r"\1", text)
    text = re.sub(r"(؛)(\s|)\n\n", ".\n\n", text)
    text = re.sub(r"([\(\«])[\s]([؛\.،])", r"\1", text)
    text = re.sub(r"(،)([\s]+)?([،؛!؟\-][\.،؛!؟\-]*|\.(?!\.))", r"\1", text)
    # Ellipsis only after Persian letters
    text = re.sub(rf"([{PERSIAN_CHARACTERS}])( *)(\.{{3,}})", r"\1\2…", text)
    text = re.sub(rf"([{PERSIAN_CHARACTERS}])\.( *[،؛:!؟\?]+)", r"\1.", text)
    text = re.sub(
        rf"(\(|«)[\.،؛](\s|)([{PERSIAN_CHARACTERS}])",
        r"\1\3",
        text,
    )
    text = re.sub(r"(؟(\s|)){2,}", "؟", text)
    text = text.replace("؟ !", "؟!").replace("! ؟", "!؟")
    text = re.sub(
        rf"([{PERSIAN_CHARACTERS}]) +([؟،:؛!])(\s|$)",
        r"\1\2\3",
        text,
    )
    text = text.replace(" (ها)", "(ها)")
    return text



def apply_fa_bot(
    text: str,
    *,
    digits: bool = False,
    do_punctuation: bool = True,
) -> str:
    """Full persianTools pipeline."""
    if not text:
        return text
    text = to_standard_persian_characters(text)
    text = apply_orthography(text)
    text = apply_zwnj(text)
    if do_punctuation:
        text = punctuation(text)
    if digits:
        text = to_persian_digits(text)
    return text


def replace_except(
    text: str,
    callback: Callable[[str], str],
    excepts: list[re.Pattern[str]],
) -> str:
    """Apply *callback* outside regions matched by *excepts* (upstream replaceExcept)."""
    result: list[str] = []
    while text:
        ranges: list[tuple[int, int]] = []
        for pat in excepts:
            m = pat.search(text)
            if m is not None:
                ranges.append((m.start(), m.end()))
        if not ranges:
            result.append(callback(text))
            break
        ranges.sort(key=lambda r: r[0])
        min_from, min_to = ranges[0]
        max_to = min_to
        for fr, to in ranges:
            if fr <= max_to:
                max_to = max(max_to, to)
        result.append(callback(text[:min_from]))
        result.append(text[min_from:max_to])
        text = text[max_to:]
    return "".join(result)
