# -*- coding: utf-8 -*-
"""خواندن نظرهای گوگل مپ و ثبتشان در جدول TourReview.

از Places API (New) استفاده می‌شود چون تنها نسخه‌ای است که هم از سرور و هم
از مرورگر (CORS) قابل صدا زدن است. گوگل حداکثر ۵ نظرِ منتخب هر مکان را
برمی‌گرداند و اجازهٔ فیلتر کردنشان را نمی‌دهد؛ برای همین کشورِ هر نظر از
روی متنش حدس زده می‌شود و اگر پیدا نشد، مدیر در پنل انتخابش می‌کند.
"""
import json
import re
from datetime import datetime

from django.utils import timezone

PLACES_ENDPOINT = 'https://places.googleapis.com/v1/places/%s'
FIELD_MASK = 'id,displayName,rating,userRatingCount,reviews'
DEFAULT_TIMEOUT = 15


class GoogleReviewsError(Exception):
    """خطای قابل نمایش به مدیر.

    network=True یعنی خود درخواست به گوگل نرسید (فیلترینگ، DNS، تایم‌اوت).
    در این حالت پنل می‌تواند همان درخواست را از مرورگرِ مدیر بفرستد.
    """

    def __init__(self, message, network=False):
        super().__init__(message)
        self.message = message
        self.network = network


def _config(setting):
    """(place_id, api_key, proxy) را از تنظیمات قالب می‌خواند."""
    place_id = (getattr(setting, 'google_place_id', '') or '').strip()
    api_key = (getattr(setting, 'google_places_key', '') or '').strip()
    proxy = (getattr(setting, 'google_api_proxy', '') or '').strip()
    if not place_id:
        raise GoogleReviewsError(
            'شناسهٔ مکان (Place ID) در تنظیمات ثبت نشده است.')
    if not api_key:
        raise GoogleReviewsError(
            'کلید Places API در تنظیمات ثبت نشده است.')
    m = re.search(r'placeid=([^&\s]+)', place_id) or re.search(r'place_id[:=]([^&\s]+)', place_id)
    if m:
        place_id = m.group(1)
    return place_id, api_key, proxy


def fetch_place(place_id, api_key, language='fa', proxy=None,
                timeout=DEFAULT_TIMEOUT):
    """پاسخ خام Places API را برمی‌گرداند."""
    import requests

    url = PLACES_ENDPOINT % place_id
    headers = {
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': FIELD_MASK,
    }
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    try:
        resp = requests.get(url, headers=headers,
                            params={'languageCode': language},
                            proxies=proxies, timeout=timeout)
    except Exception as exc:
        raise GoogleReviewsError(
            'سرور نتوانست به گوگل وصل شود — %s: %s'
            % (type(exc).__name__, str(exc)[:160]),
            network=True)

    if resp.status_code == 403:
        raise GoogleReviewsError(
            'گوگل کلید را نپذیرفت (۴۰۳). مطمئن شو Places API (New) روی '
            'پروژه فعال است و کلید محدودیت IP اشتباه ندارد.')
    if resp.status_code == 404:
        raise GoogleReviewsError('این Place ID در گوگل پیدا نشد (۴۰۴).')
    if resp.status_code != 200:
        detail = ''
        try:
            detail = resp.json().get('error', {}).get('message', '')
        except Exception:
            detail = resp.text[:200]
        raise GoogleReviewsError('گوگل خطا داد (%s): %s'
                                 % (resp.status_code, detail))
    try:
        return resp.json()
    except ValueError:
        raise GoogleReviewsError('پاسخ گوگل قابل خواندن نبود.')


def _parse_date(value):
    """publishTime گوگل (ISO 8601) را به date تبدیل می‌کند."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
    except Exception:
        return None


def normalize(payload):
    """پاسخ گوگل را به لیستی از دیکشنری‌های ساده تبدیل می‌کند."""
    rows = []
    for r in (payload or {}).get('reviews', []) or []:
        text = ((r.get('originalText') or {}).get('text')
                or (r.get('text') or {}).get('text') or '').strip()
        author = ((r.get('authorAttribution') or {}).get('displayName')
                  or '').strip()
        if not text or not author:
            continue
        rows.append({
            'external_id': (r.get('name') or '').strip()[:190],
            'author': author[:150],
            'rating': int(r.get('rating') or 5),
            'text': text[:1500],
            'review_date': _parse_date(r.get('publishTime')),
            'source_url': (r.get('googleMapsUri') or '').strip()[:500] or None,
        })
    return rows


def guess_country(text):
    """کشور نظر را از روی نام کشورها در متن حدس می‌زند."""
    from tour.models import Country

    if not text:
        return None
    best = None
    for country in Country.objects.all().only('id', 'TitleC', 'slug'):
        title = (country.TitleC or '').strip()
        if title and title in text:
            if best is None or len(title) > len(best[1]):
                best = (country, title)
    return best[0] if best else None


def import_reviews(rows, publish=True, assign_country=True):
    """نظرها را ثبت یا به‌روزرسانی می‌کند و شمارش را برمی‌گرداند."""
    from tour.models import TourReview

    created = updated = skipped = 0
    for row in rows:
        existing = None
        if row.get('external_id'):
            existing = TourReview.objects.filter(
                external_id=row['external_id']).first()
        if existing is None:
            existing = TourReview.objects.filter(
                author=row['author'], text=row['text']).first()

        if existing is not None:
            changed = False
            if not existing.external_id and row.get('external_id'):
                existing.external_id = row['external_id']
                changed = True
            if existing.text != row['text']:
                existing.text = row['text']
                changed = True
            if existing.rating != row['rating']:
                existing.rating = row['rating']
                changed = True
            if row.get('review_date') and existing.review_date != row['review_date']:
                existing.review_date = row['review_date']
                changed = True
            if changed:
                existing.save()
                updated += 1
            else:
                skipped += 1
            continue

        country = guess_country(row['text']) if assign_country else None
        TourReview.objects.create(
            external_id=row.get('external_id') or None,
            author=row['author'],
            rating=row['rating'],
            text=row['text'],
            review_date=row.get('review_date'),
            country=country,
            source='google',
            source_url=row.get('source_url'),
            publish=publish,
            sort_order=0,
        )
        created += 1
    return {'created': created, 'updated': updated, 'skipped': skipped}


def sync_from_google(setting, language='fa'):
    """کل مسیر: خواندن از گوگل + ثبت در دیتابیس."""
    place_id, api_key, proxy = _config(setting)
    payload = fetch_place(place_id, api_key, language=language, proxy=proxy)
    rows = normalize(payload)
    result = import_reviews(rows)
    result['fetched'] = len(rows)
    result['place'] = (payload.get('displayName') or {}).get('text', '')
    result['rating'] = payload.get('rating')
    result['total_ratings'] = payload.get('userRatingCount')
    result['at'] = timezone.now()
    return result
