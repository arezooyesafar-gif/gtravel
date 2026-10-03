import re

from django import template

register = template.Library()

@register.filter
def is_toman(pcry):
    if pcry is None:
        return False
    title = getattr(pcry, 'Title', '') or ''
    return 'تومان' in title


_ONES = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه']
_TEENS = ['ده', 'یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هجده', 'نوزده']
_TENS = ['', '', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود']


def _cardinal_word(number):
    """عدد ۱ تا ۹۹ را به حروف فارسی برمی‌گرداند."""
    if number < 10:
        return _ONES[number]
    if number < 20:
        return _TEENS[number - 10]
    tens, ones = divmod(number, 10)
    if ones == 0:
        return _TENS[tens]
    return '%s و %s' % (_TENS[tens], _ONES[ones])


def _make_ordinal(word, standalone):
    if word == 'یک':
        return 'اول' if standalone else 'یکم'
    if word == 'سه':
        return 'سوم'
    if word == 'سی':
        return 'سی‌ام'
    return word + 'م'


@register.filter
def persian_ordinal(number):
    """۱ -> اول ، ۲ -> دوم ، ۲۳ -> بیست و سوم"""
    try:
        number = int(number)
    except (TypeError, ValueError):
        return ''
    if number < 1 or number > 99:
        return str(number)
    word = _cardinal_word(number)
    if ' و ' in word:
        head, tail = word.rsplit(' و ', 1)
        return '%s و %s' % (head, _make_ordinal(tail, standalone=False))
    return _make_ordinal(word, standalone=True)


@register.filter
def persian_digits(value):
    """ارقام لاتین را به ارقام فارسی تبدیل می‌کند."""
    if value is None:
        return ''
    return str(value).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


def _mojibake(text):
    """شکل خراب‌شده‌ی متن فارسی (وقتی UTF-8 به اشتباه cp1252 خوانده شده)."""
    try:
        return text.encode('utf-8').decode('cp1252')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return ''


def _build_day_prefix_re():
    words = set()
    for n in range(1, 100):
        words.add(persian_ordinal(n))
        words.add(_cardinal_word(n))
    words.discard('')
    words |= {m for m in (_mojibake(w) for w in words) if m}
    # عبارت‌های طولانی‌تر اول بیایند تا «بیست و یکم» قبل از «یک» تطبیق بخورد
    alternatives = sorted(words, key=len, reverse=True)
    day_words = [w for w in ('روز', _mojibake('روز')) if w]
    pattern = r'^\s*(?:%s)\s*(?:%s|[0-9۰-۹٠-٩]+)\s*(?:[:：\-–—،]\s*)?' % (
        '|'.join(re.escape(d) for d in day_words),
        '|'.join(re.escape(w) for w in alternatives),
    )
    return re.compile(pattern)


_DAY_PREFIX_RE = _build_day_prefix_re()


@register.filter
def strip_day_prefix(title):
    """
    شماره روز به صورت خودکار نمایش داده می‌شود، پس اگر ادمین در عنوان
    «روز اول:» یا «روز ۲ -» نوشته باشد، از ابتدای عنوان حذف می‌شود.
    """
    if not title:
        return ''
    text = str(title).strip()
    cleaned = _DAY_PREFIX_RE.sub('', text, count=1).strip(' :-–—،')
    return cleaned or ''


_EMPTY_MARKERS = {'', '-', '--', '_', '—', '–', '.', '،'}


@register.filter
def clean_value(value):
    """اگر مقدار خالی یا خط تیره باشد، رشته خالی برمی‌گرداند تا در قالب نمایش داده نشود."""
    if value is None:
        return ''
    text = str(value).strip()
    return '' if text in _EMPTY_MARKERS else text


@register.filter
def nights_in_city(cities, city):
    """
    تعداد شب اقامت در شهرِ یک هتل را از برنامه پروازی تور (TourCity) پیدا می‌کند.
    اگر شهر در برنامه نباشد یا شب اقامتی ثبت نشده باشد، رشته خالی برمی‌گرداند
    تا در قالب چیزی نمایش داده نشود.
    """
    if not cities or city is None:
        return ''
    city_id = getattr(city, 'id', None)
    if city_id is None:
        return ''
    total = 0
    for tour_city in cities:
        target = getattr(tour_city, 'CtName', None)
        if getattr(target, 'id', None) != city_id:
            continue
        try:
            nights = int(str(getattr(tour_city, 'NightCount', '') or '').strip())
        except (TypeError, ValueError):
            continue
        if nights > 0:
            total += nights
    return total or ''


def _first_number(value):
    match = re.search(r'\d[\d,]*', str(value or ''))
    return int(match.group().replace(',', '')) if match else 0


@register.filter
def price_slider_max(rows, rate):
    rate = _first_number(rate) or 170000
    highest = 0
    for row in rows or []:
        packages = row[1] if len(row) > 1 else None
        if not packages:
            continue
        package = packages[0]
        foreign = package.DoubleBedPrice_doller or (_first_number(package.DollerPrice) if package.DollerPrice else 0)
        numbers = [n for n in (_first_number(package.DoubleBedPrice), _first_number(foreign)) if n > 0]
        if not numbers:
            continue
        value = numbers[0] + (numbers[1] if len(numbers) > 1 else 0) * rate if numbers[0] >= 1000000 else numbers[0] * rate
        highest = max(highest, value)
    if highest <= 0:
        return 0
    return -(-highest // 5000000) * 5000000
