"""
استخراج قیمت از پاسخ JSON آژانس‌های همکار.
چون هر آژانس ممکنه ساختار متفاوتی داشته باشه، سه سطح تلاش می‌شه:
1) اگه برای منبع، مسیر دستی فیلد قیمت تنظیم شده باشه (مثلاً data.rooms.0.price)، همون استفاده می‌شه.
2) اگه نه، چند ساختار شناخته‌شده (مثل فید خودمون: price.amount) چک می‌شه.
3) اگه هیچ‌کدوم جواب نداد، کل درخت JSON به‌صورت بازگشتی برای فیلدهایی با اسم شبیه قیمت
   (price, amount, قیمت, مبلغ, ...) که مقدارشون عددیه گشته می‌شه و اولین/دومین مورد به‌عنوان
   حدس برگردونده می‌شه.
این یک روش حدسیه، نه تضمینی؛ پاسخ خام همیشه ذخیره می‌شه تا در صورت اشتباه بودن حدس،
بشه دستی مسیر رو تنظیم کرد یا خود پاسخ خام رو خوند.

بخش دوم این فایل (find_price_like_html / extract_price_fields_from_html) برای وقتیه که
آدرس داده‌شده اصلاً API نیست، یه صفحه‌ی وب معمولیه (HTML). چون خیلی از آژانس‌ها API ندارن،
همون لینک صفحه‌ی تور رو می‌گیریم، تگ‌ها رو حذف می‌کنیم، و تو متن باقی‌مونده دنبال یه عدد بزرگ
می‌گردیم که بلافاصله بعدش کلمه‌ی واحد پول (تومان/دلار/...) اومده باشه؛ چند خط بالاترش رو هم
برای کلمات نوع اتاق (دو تخته/یک تخته/...) می‌گردیم تا بفهمیم این قیمت مال کدوم نوع اتاقه.
"""
import re
from html.parser import HTMLParser

_FA_AR_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')

_PRICE_KEY_HINTS = [
    'price', 'amount', 'cost', 'fee', 'rate', 'qeymat', 'gheymat',
    'قیمت', 'مبلغ', 'هزینه', 'نرخ', 'toman', 'تومان', 'dollar', 'دلار',
]
_CURRENCY_KEY_HINTS = ['currency', 'ارز', 'واحد', 'unit', 'symbol']
_EXCLUDE_KEY_HINTS = ['id', 'count', 'index', 'duration', 'year', 'code', 'phone', 'mobile', 'width', 'height']


def resolve_path(data, path):
    """data رو طبق مسیر نقطه‌ای (مثل data.rooms.0.price) می‌خونه؛ اگه پیدا نشه None برمی‌گردونه."""
    if not path:
        return None
    current = data
    for part in path.split('.'):
        part = part.strip()
        if not part:
            continue
        if isinstance(current, dict):
            if part not in current:
                return None
            current = current[part]
        elif isinstance(current, (list, tuple)):
            if not part.lstrip('-').isdigit():
                return None
            idx = int(part)
            if not (-len(current) <= idx < len(current)):
                return None
            current = current[idx]
        else:
            return None
    return current


def _looks_numeric(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        s = value.strip().translate(_FA_AR_DIGITS).replace(',', '').replace('،', '')
        return bool(re.fullmatch(r'-?\d+(\.\d+)?', s))
    return False


def to_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().translate(_FA_AR_DIGITS).replace(',', '').replace('،', '')
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def _key_matches(key, hints):
    lk = str(key).lower()
    return any(h in lk for h in hints)


def find_price_like(data):
    """به‌صورت بازگشتی دنبال فیلدهایی با اسم شبیه قیمت و مقدار عددی می‌گرده.
    برای هر مورد، اگه تو همون سطح یه فیلد شبیه واحد ارز پیدا بشه، همراهش برمی‌گردونده می‌شه.
    خروجی: لیستی از (key_path_list, amount, currency_or_None) به ترتیب پیمایش."""
    matches = []

    def _sibling_currency(container):
        if not isinstance(container, dict):
            return None
        for k, v in container.items():
            if _key_matches(k, _CURRENCY_KEY_HINTS) and isinstance(v, str) and v.strip():
                return v.strip()
        return None

    def _walk(node, key_path):
        if isinstance(node, dict):
            for k, v in node.items():
                lk = str(k).lower()
                is_excluded = any(h in lk for h in _EXCLUDE_KEY_HINTS)
                if not is_excluded and _key_matches(k, _PRICE_KEY_HINTS) and _looks_numeric(v):
                    matches.append((key_path + [str(k)], to_number(v), _sibling_currency(node)))
                _walk(v, key_path + [str(k)])
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                _walk(v, key_path + [str(i)])

    _walk(data, [])
    return matches


def extract_price_fields(data, source=None):
    """نقطه ورود اصلی: بر اساس اولویت‌های بالا سعی می‌کنه amount/currency (ارز اول و دوم) رو پیدا کنه."""
    result = _extract_price_fields_raw(data, source)
    # واحد ارز تو دیتابیس محدود به ۵۰ کاراکتره؛ اگه آژانس یه چیز عجیب/طولانی برگردوند خطا نگیریم
    for key in ('price_currency', 'price_currency_foreign'):
        if isinstance(result.get(key), str):
            result[key] = result[key].strip()[:50] or None
    return result


def _extract_price_fields_raw(data, source=None):
    result = {
        'price_amount': None, 'price_currency': None,
        'price_amount_foreign': None, 'price_currency_foreign': None,
    }

    # 1) مسیر دستی تنظیم‌شده روی منبع
    if source is not None and getattr(source, 'price_amount_path', None):
        raw = resolve_path(data, source.price_amount_path)
        if raw is not None and _looks_numeric(raw):
            result['price_amount'] = to_number(raw)
        if source.price_currency_path:
            cur = resolve_path(data, source.price_currency_path)
            if isinstance(cur, str):
                result['price_currency'] = cur
        if source.price_amount_foreign_path:
            raw_f = resolve_path(data, source.price_amount_foreign_path)
            if raw_f is not None and _looks_numeric(raw_f):
                result['price_amount_foreign'] = to_number(raw_f)
        if source.price_currency_foreign_path:
            cur_f = resolve_path(data, source.price_currency_foreign_path)
            if isinstance(cur_f, str):
                result['price_currency_foreign'] = cur_f
        if result['price_amount'] is not None:
            return result

    # 2) ساختارهای شناخته‌شده‌ی رایج
    if isinstance(data, dict):
        price = data.get('price')
        if isinstance(price, dict) and _looks_numeric(price.get('amount')):
            result['price_amount'] = to_number(price.get('amount'))
            result['price_currency'] = price.get('currency')
            if _looks_numeric(price.get('amount_foreign')):
                result['price_amount_foreign'] = to_number(price.get('amount_foreign'))
            result['price_currency_foreign'] = price.get('currency_foreign')
            return result
        for key in ('DoubleBedPrice', 'double_bed_price', 'price'):
            if key in data and _looks_numeric(data.get(key)):
                result['price_amount'] = to_number(data.get(key))
                result['price_currency'] = data.get('currency')
                foreign = data.get('DoubleBedPrice_doller') or data.get('price_foreign')
                if _looks_numeric(foreign):
                    result['price_amount_foreign'] = to_number(foreign)
                result['price_currency_foreign'] = data.get('currency_foreign')
                return result

    # 3) جستجوی بازگشتی حدسی در کل درخت
    guesses = find_price_like(data)
    if guesses:
        result['price_amount'] = guesses[0][1]
        result['price_currency'] = guesses[0][2]
        if len(guesses) > 1:
            result['price_amount_foreign'] = guesses[1][1]
            result['price_currency_foreign'] = guesses[1][2]

    return result


_BLOCK_TAGS = {'div', 'p', 'li', 'tr', 'td', 'br', 'section', 'article', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'}


_SKIP_CONTENT_TAGS = {'script', 'style', 'noscript'}


class _HtmlTextExtractor(HTMLParser):
    """یه صفحه HTML رو به یه سری خط متن ساده تبدیل می‌کنه (هر تگ بلوکی = یه خط جدا) تا بشه راحت‌تر دنبال قیمت گشت.
    محتوای تگ‌های script/style/noscript (که متن واقعی صفحه نیستن، کد یا استایلن) نادیده گرفته می‌شه."""
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_CONTENT_TAGS:
            self._skip_depth += 1
        if tag in _BLOCK_TAGS:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in _SKIP_CONTENT_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag in _BLOCK_TAGS:
            self.parts.append('\n')

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.parts.append(data)


def html_to_lines(html_text):
    parser = _HtmlTextExtractor()
    try:
        parser.feed(html_text)
    except Exception:
        pass
    text = ''.join(parser.parts)
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    return [line for line in lines if line]


_ROOM_LABEL_HINTS = [
    ('double_bed', ['دو تخته', 'دبل', 'double']),
    ('single_bed', ['یک تخته', 'سینگل', 'single']),
    ('child_with_bed', ['کودک با تخت']),
    ('child_without_bed', ['کودک بدون تخت']),
    ('infant', ['نوزاد', 'infant']),
]
_CURRENCY_WORDS = ['تومان', 'ریال', 'دلار', 'یورو', 'toman', 'rial', 'dollar', 'euro']
_FOREIGN_CURRENCY_WORDS = {'دلار', 'یورو', 'dollar', 'euro'}
_HTML_PRICE_LINE_RE = re.compile(r'^([\d۰-۹][\d۰-۹,،]{2,})$')


def find_price_like_html(html_text):
    """تو متن ساده‌شده‌ی صفحه (بعد از حذف تگ‌ها) دنبال خط‌هایی می‌گرده که فقط یه عدد بزرگ هستن
    و تا ۲ خط بعدشون کلمه‌ی واحد پول اومده باشه؛ برای فهمیدن نوع اتاق هم چند خط قبلش رو برای
    کلمات آشنا (دو تخته/یک تخته/...) می‌گرده. خروجی: لیستی از (label_or_None, amount, currency)."""
    lines = html_to_lines(html_text)
    matches = []
    for i, line in enumerate(lines):
        if not _HTML_PRICE_LINE_RE.match(line):
            continue
        amount = to_number(line)
        if amount is None or amount < 1000:
            continue
        currency = None
        for j in range(i + 1, min(i + 3, len(lines))):
            if lines[j] in _CURRENCY_WORDS:
                currency = lines[j]
                break
        if not currency:
            continue
        label = None
        for k in range(max(0, i - 6), i):
            for key, hints in _ROOM_LABEL_HINTS:
                if any(h in lines[k] for h in hints):
                    label = key
                    break
            if label:
                break
        matches.append((label, amount, currency))
    return matches


def extract_price_fields_from_html(html_text):
    """مشابه extract_price_fields ولی برای یه صفحه‌ی HTML معمولی (نه JSON API). چون صفحه‌ی
    وب مسیر فیلد مشخصی نداره، همیشه حدسیه: اول دنبال قیمت «دو تخته» می‌گرده (چون قیمت پایه‌ی
    سایت ما هم همینه)، اگه نبود اولین قیمتی که پیدا کرده رو برمی‌گردونه."""
    result = {
        'price_amount': None, 'price_currency': None,
        'price_amount_foreign': None, 'price_currency_foreign': None,
    }
    matches = find_price_like_html(html_text)
    if not matches:
        return result

    double_bed_matches = [m for m in matches if m[0] == 'double_bed']
    primary = double_bed_matches[0] if double_bed_matches else matches[0]
    result['price_amount'] = primary[1]
    result['price_currency'] = primary[2][:50]

    for label, amount, currency in matches:
        if currency in _FOREIGN_CURRENCY_WORDS:
            result['price_amount_foreign'] = amount
            result['price_currency_foreign'] = currency[:50]
            break

    return result


def _normalize_hotel_name(name):
    """اسم هتل رو برای مقایسه ساده می‌کنه: نیم‌فاصله/فاصله‌های تکراری حذف، حروف کوچک،
    و کلمه‌ی عمومی «هتل»/«hotel» از ابتدا یا انتها برداشته می‌شه (چون سایت‌های مختلف
    ممکنه این کلمه رو جای متفاوتی بذارن یا اصلاً نذارن)."""
    if not name:
        return ''
    s = str(name).replace('‌', ' ')
    s = re.sub(r'\s+', ' ', s).strip().lower()
    for prefix in ('هتل ', 'hotel '):
        if s.startswith(prefix):
            s = s[len(prefix):]
    for suffix in (' هتل', ' hotel'):
        if s.endswith(suffix):
            s = s[:-len(suffix)]
    return s.strip()


def _hotel_name_matches(page_line, candidate_name):
    """فقط این جهت رو چک می‌کنیم: اسم هتل ما (candidate) کاملاً تو خط صفحه اومده باشه، نه برعکس؛
    وگرنه یه اسم عمومی/کوتاه تو دیتابیس (که مثلاً اسم شهر رو هم توش داره) می‌تونه با هر خطی که
    فقط اسم شهر توشه false-match بده."""
    a = _normalize_hotel_name(page_line)
    b = _normalize_hotel_name(candidate_name)
    if len(a) < 4 or len(b) < 6:
        return False
    return a == b or b in a


def _extract_room_prices_from_segment(lines):
    """تو یه تیکه از متن (مال یه هتل خاص)، برای هر نوع اتاق قیمت ارز اول و دوم رو پیدا می‌کنه.
    خروجی: dict مثل {'double_bed': {'amount':..,'currency':..,'amount_foreign':..,'currency_foreign':..}, ...}"""
    label_positions = []
    for i, line in enumerate(lines):
        for key, hints in _ROOM_LABEL_HINTS:
            if any(h in line for h in hints):
                label_positions.append((i, key))
                break

    prices = {}
    for idx, (pos, key) in enumerate(label_positions):
        end = label_positions[idx + 1][0] if idx + 1 < len(label_positions) else len(lines)
        segment = lines[pos + 1:end]
        pairs = []
        j = 0
        while j < len(segment) - 1:
            if _HTML_PRICE_LINE_RE.match(segment[j]) and segment[j + 1] in _CURRENCY_WORDS:
                pairs.append((to_number(segment[j]), segment[j + 1]))
                j += 2
            else:
                j += 1
        if not pairs:
            continue
        main = next((p for p in pairs if p[1] not in _FOREIGN_CURRENCY_WORDS), None)
        foreign = next((p for p in pairs if p[1] in _FOREIGN_CURRENCY_WORDS), None)
        entry = prices.setdefault(key, {})
        if main:
            entry['amount'] = main[0]
            entry['currency'] = main[1][:50]
        if foreign:
            entry['amount_foreign'] = foreign[0]
            entry['currency_foreign'] = foreign[1][:50]
    return prices


def find_hotel_price_blocks_html(html_text, hotel_candidates):
    """hotel_candidates: لیستی از (package_id, [نام‌های ممکن هتل]) که از پکیج‌های خود تور می‌گیریم.
    تو صفحه دنبال این اسم‌ها می‌گرده و برای هر کدوم که پیدا کرد، قیمت اتاق‌های مختلف که تا قبل از
    اسم هتل بعدی (که تو صفحه پیدا شده) اومدن رو استخراج می‌کنه.
    خروجی: لیستی از dict با کلیدهای package_id, matched_name, prices."""
    lines = html_to_lines(html_text)
    found = []
    for i, line in enumerate(lines):
        if len(line) < 4:
            continue
        matched_here = None
        for package_id, names in hotel_candidates:
            for name in names:
                if name and _hotel_name_matches(line, name):
                    matched_here = (package_id, name)
                    break
            if matched_here:
                break
        if matched_here:
            found.append((i, matched_here[0], matched_here[1]))

    results = []
    for idx, (pos, package_id, matched_name) in enumerate(found):
        end = found[idx + 1][0] if idx + 1 < len(found) else min(pos + 40, len(lines))
        segment = lines[pos + 1:end]
        prices = _extract_room_prices_from_segment(segment)
        if prices:
            results.append({
                'package_id': package_id,
                'matched_name': matched_name,
                'prices': prices,
            })
    return results
