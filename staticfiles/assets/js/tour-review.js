/* ===========================================================================
   دکمهٔ «دریافت نظرها از گوگل» در صفحهٔ لیست نظرات داشبورد.

   اول از سرور درخواست می‌دهد. اگر سرور به گوگل نرسید (فیلترینگ)، همان
   درخواست را از مرورگرِ خودِ مدیر می‌فرستد - Places API (New) تنها نسخه‌ای
   است که CORS دارد - و نتیجه را برای ثبت به سرور پس می‌دهد.
   =========================================================================== */
(function () {
    'use strict';

    var btn = document.getElementById('review-google-btn');
    if (!btn) { return; }

    var box = document.getElementById('review-google-status');
    var FIELD_MASK = 'id,displayName,rating,userRatingCount,reviews';

    function say(kind, html) {
        if (!box) { return; }
        box.className = 'review-google-status is-visible is-' + kind;
        box.innerHTML = html;
    }

    function busy(on) {
        btn.disabled = on;
        btn.textContent = on ? 'در حال دریافت…' : btn.dataset.label;
    }

    function csrf() {
        var el = document.querySelector('input[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }

    function report(data) {
        var parts = [];
        if (data.place) { parts.push('مکان: <b>' + data.place + '</b>'); }
        if (data.rating) {
            parts.push('امتیاز گوگل: <b>' + data.rating + '</b>'
                + (data.total_ratings ? ' از ' + data.total_ratings + ' نظر' : ''));
        }
        parts.push('دریافت‌شده: <b>' + (data.fetched || 0) + '</b>');
        parts.push('نظر جدید: <b>' + (data.created || 0) + '</b>');
        parts.push('به‌روزرسانی: <b>' + (data.updated || 0) + '</b>');
        parts.push('تکراری: <b>' + (data.skipped || 0) + '</b>');
        say('ok', parts.join(' &nbsp;•&nbsp; ')
            + '<br>صفحه تازه‌سازی می‌شود؛ برای نظرهایی که کشورشان «انتخاب نشده» است'
            + ' با «ویرایش» کشور را مشخص کن.');
        setTimeout(function () { window.location.reload(); }, 2200);
    }

    /* مسیر جایگزین: خواندن مستقیم از گوگل با مرورگر مدیر */
    function fromBrowser(placeId, apiKey) {
        say('busy', 'سرور به گوگل نرسید؛ دارم از همین مرورگر امتحان می‌کنم…');
        var url = 'https://places.googleapis.com/v1/places/'
            + encodeURIComponent(placeId) + '?languageCode=fa';
        return fetch(url, {
            headers: {
                'X-Goog-Api-Key': apiKey,
                'X-Goog-FieldMask': FIELD_MASK
            }
        }).then(function (r) {
            return r.json().then(function (payload) {
                if (!r.ok) {
                    var msg = (payload.error && payload.error.message) || r.status;
                    throw new Error('گوگل جواب نداد: ' + msg);
                }
                return payload;
            });
        }).then(function (payload) {
            return fetch(btn.dataset.importUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf()
                },
                body: JSON.stringify(payload)
            }).then(function (r) { return r.json(); });
        });
    }

    btn.dataset.label = btn.textContent.trim();

    btn.addEventListener('click', function () {
        busy(true);
        say('busy', 'در حال گرفتن نظرها از گوگل…');

        fetch(btn.dataset.fetchUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrf() }
        }).then(function (r) {
            return r.json();
        }).then(function (data) {
            if (data.ok) { report(data); return null; }
            if (data.network && data.place_id && data.api_key) {
                return fromBrowser(data.place_id, data.api_key)
                    .then(function (res) {
                        if (res && res.ok) { report(res); }
                        else {
                            say('error', (res && res.error)
                                || 'از مرورگر هم نشد. اگر فیلترشکن روشن است دوباره امتحان کن.');
                            busy(false);
                        }
                    });
            }
            say('error', data.error || 'دریافت نشد.');
            busy(false);
            return null;
        }).catch(function (err) {
            var offline = /Failed to fetch|NetworkError|Load failed/i.test(err.message);
            say('error', offline
                ? 'مرورگر هم به گوگل نرسید. فیلترشکن را روشن کن و دوباره بزن،'
                    + ' یا در تنظیمات یک پراکسی برای سرور بگذار.'
                : 'خطا: ' + err.message);
            busy(false);
        });
    });
}());
