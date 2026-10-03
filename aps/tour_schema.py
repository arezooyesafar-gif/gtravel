import json
from datetime import date

from django.urls import reverse
from django.utils.safestring import mark_safe

SITE = 'https://arezoosafar.com'
CURRENCIES = (
    ('تومان', 'IRR', 10),
    ('ریال', 'IRR', 1),
    ('دلار', 'USD', 1),
    ('یورو', 'EUR', 1),
    ('درهم', 'AED', 1),
    ('لیر', 'TRY', 1),
    ('یوان', 'CNY', 1),
    ('روبل', 'RUB', 1),
)


def currency_code(name):
    name = str(name or '')
    for label, code, factor in CURRENCIES:
        if label in name:
            return code, factor
    return None, None


def number(value):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def tour_offer(tour, url, price, price_foreign, currency, currency_foreign, packages, departures, dollar_rate):
    price, price_foreign = number(price), number(price_foreign)
    main_code, main_factor = currency_code(currency)
    foreign_code, foreign_factor = currency_code(currency_foreign)
    offer = {'@type': 'Offer', 'url': url}
    if price and main_code and price_foreign:
        if not foreign_code:
            return None
        components = [
            {'@type': 'UnitPriceSpecification', 'price': price * main_factor, 'priceCurrency': main_code},
            {'@type': 'UnitPriceSpecification', 'price': price_foreign * foreign_factor, 'priceCurrency': foreign_code},
        ]
        offer['priceSpecification'] = {'@type': 'CompoundPriceSpecification', 'priceComponent': components}
        if main_code == 'IRR' and foreign_code == 'USD' and number(dollar_rate):
            offer['price'] = price * main_factor + price_foreign * number(dollar_rate) * 10
            offer['priceCurrency'] = 'IRR'
    elif price and main_code:
        offer['price'] = price * main_factor
        offer['priceCurrency'] = main_code
    elif price_foreign and foreign_code:
        offer['price'] = price_foreign * foreign_factor
        offer['priceCurrency'] = foreign_code
    else:
        return None
    today = date.today()
    upcoming = sorted(day for day in departures if day and day >= today)
    if not upcoming:
        offer['availability'] = 'https://schema.org/Discontinued'
    elif packages and all(getattr(package, 'fully_sold_out', False) for package in packages):
        offer['availability'] = 'https://schema.org/SoldOut'
    else:
        offer['availability'] = 'https://schema.org/InStock'
        offer['priceValidUntil'] = upcoming[-1].isoformat()
    offer['seller'] = {'@type': 'TravelAgency', 'name': 'آرزوی سفر پارسیان', 'url': SITE + '/'}
    return offer


def tour_schema(tour, price, price_foreign, currency, currency_foreign, packages, date_plans, dollar_rate):
    url = SITE + reverse('tour-detail', args=[tour.id, tour.Slug])
    data = {
        '@context': 'https://schema.org',
        '@type': ['TouristTrip', 'Product'],
        'name': tour.Title,
        'url': url,
    }
    if tour.TourImage:
        data['image'] = [SITE + tour.TourImage.url]
    data['description'] = tour.MetaDescription or tour.Title
    data['sku'] = str(tour.id)
    data['provider'] = {'@type': 'TravelAgency', 'name': 'آرزوی سفر پارسیان', 'url': SITE + '/'}
    departures = [tour.StartDate] + [plan.start_date for plan in date_plans]
    offer = tour_offer(tour, url, price, price_foreign, currency, currency_foreign, packages, departures, dollar_rate)
    if offer:
        data['offers'] = offer
    else:
        data['@type'] = 'TouristTrip'
        data.pop('sku')
    text = json.dumps(data, ensure_ascii=False, indent=4)
    return mark_safe(text.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))
