from tour.models import Footer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.cache import cache


def site_config(request):
    footer = Footer.objects.first()
    return {
        'dollar_rate': footer.dollar_rate if footer else 170000,
        'JAWG_ACCESS_TOKEN': settings.JAWG_ACCESS_TOKEN,
    }

def hotel_menu(request):
    from tour.models import Country
    from hotels.models import Hotel_Data

    cached = cache.get('hotel_menu_countries')
    if cached is None:
        countries = Country.objects.filter(hotel_country__isnull=False).distinct().order_by('menu_order')
        grouped = {'1': [], '2': [], '3': [], '4': []}
        for idx, country in enumerate(countries):
            count = Hotel_Data.objects.filter(Hcountry=country).count()
            column = str((idx % 4) + 1)
            grouped[column].append((country, count))
        cached = {
            'grouped': grouped,
            'all': list(countries),
        }
        cache.set('hotel_menu_countries', cached, timeout=1800)

    grouped = cached['grouped']
    return {
        'hotel_menu_countries_1': grouped.get('1', []),
        'hotel_menu_countries_2': grouped.get('2', []),
        'hotel_menu_countries_3': grouped.get('3', []),
        'hotel_menu_countries_4': grouped.get('4', []),
        'hotel_menu_countries_all': cached['all'],
    }


def tour_menu(request):
    from tour.models import Country, TourMenu

    cached = cache.get('tour_menu_header')
    if cached is None:
        cached = {
            'tour_countries': list(
                Country.objects.filter(tocountry__PubTour=True)
                .order_by('menu_order').distinct()
            ),
            'top_menu': list(TourMenu.objects.filter(show_meu=True)),
        }
        cache.set('tour_menu_header', cached, timeout=1800)
    return cached


def _since(request, key):
    ts = request.session.get(key)
    if ts:
        return timezone.datetime.fromisoformat(ts)
    return timezone.now() - timedelta(days=30)


def admin_notifications(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return {}

    chat_count = 0
    interest_count = 0
    order_count = 0
    contact_count = 0
    hotel_comment_count = 0
    blog_comment_count = 0

    # نوتیف‌های تور/رزرو/تماس - جدا نگه داشته می‌شوند تا خطای احتمالی
    # این بخش، کل نوتیف‌ها را از کار نیندازد
    try:
        from tour.models import TourInterest, ContactUs, TourOrder

        interest_count = TourInterest.objects.filter(
            created_at__gt=_since(request, 'seen_interest')
        ).count()

        order_count = TourOrder.objects.filter(
            OrderTime__gt=_since(request, 'seen_order')
        ).count()

        contact_count = ContactUs.objects.filter(
            CreatedAt__gt=_since(request, 'seen_contact')
        ).count()
    except Exception:
        pass

    # کامنت‌های جدید هتل - بر اساس آخرین کامنت دیده‌شده (با باز کردن لیست پاک می‌شود)
    try:
        from hotels.models import hotel_comments
        seen_id = request.session.get('seen_hotel_comment_id')
        if seen_id is None:
            # اولین بار: از این لحظه به بعد بشمار (backlog قدیمی را نشان نده)
            latest = hotel_comments.objects.order_by('-id').values_list('id', flat=True).first() or 0
            request.session['seen_hotel_comment_id'] = latest
            hotel_comment_count = 0
        else:
            hotel_comment_count = hotel_comments.objects.filter(id__gt=seen_id).count()
    except Exception:
        pass

    # کامنت‌ها و پاسخ‌های جدید مجله گردشگری - بر اساس آخرین مورد دیده‌شده
    try:
        from blog.models import comments as blog_comments, reply_comments
        c_seen = request.session.get('seen_blog_comment_id')
        r_seen = request.session.get('seen_blog_reply_id')
        if c_seen is None or r_seen is None:
            c_latest = blog_comments.objects.order_by('-id').values_list('id', flat=True).first() or 0
            r_latest = reply_comments.objects.order_by('-id').values_list('id', flat=True).first() or 0
            request.session['seen_blog_comment_id'] = c_latest
            request.session['seen_blog_reply_id'] = r_latest
            blog_comment_count = 0
        else:
            blog_comment_count = (
                blog_comments.objects.filter(id__gt=c_seen).count()
                + reply_comments.objects.filter(id__gt=r_seen).count()
            )
    except Exception:
        pass

    total = (
        chat_count + interest_count + order_count + contact_count
        + hotel_comment_count + blog_comment_count
    )

    return {
        'notif_total': total,
        'notif_chat': chat_count,
        'notif_interest': interest_count,
        'notif_order': order_count,
        'notif_contact': contact_count,
        'notif_hotel_comment': hotel_comment_count,
        'notif_blog_comment': blog_comment_count,
    }

