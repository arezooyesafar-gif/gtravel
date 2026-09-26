from math import ceil
import os
import re
import io
import base64
import html as html_module

from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from tour.date_pricing import packages_for_date

def _image_to_b64(image_field):
    try:
        from PIL import Image as PILImage
        with PILImage.open(image_field.path) as img:
            buf = io.BytesIO()
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
                bg = PILImage.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                bg.save(buf, format='JPEG', quality=85)
            else:
                img.convert('RGB').save(buf, format='JPEG', quality=85)
            return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def _strip_html(html_text, max_chars=400):
    """Strip HTML tags and truncate to max_chars for PDF card rendering."""
    if not html_text:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html_text)
    text = html_module.unescape(text)
    # Fix mojibake: UTF-8 bytes stored as Latin-1
    try:
        text = text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
        pass
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + '…'
    return text

def mypdf(request, id):
    tour = Tour.objects.get(id=id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    tc = cities.first()
    lc = cities.last()
    selected_dp = None
    dp_id = request.GET.get('dp')
    if dp_id:
        try:
            selected_dp = date_plan.objects.get(id=dp_id, tour=tour)
        except date_plan.DoesNotExist:
            pass
    # قیمت/هتل/ویو/سرویسِ مؤثرِ همون تاریخ از قبل روی پکیج‌ها اعمال می‌شه، پس
    # قالب دیگه نباید اختلاف قیمت رو دوباره اضافه کنه
    packages = packages_for_date(tour, selected_dp)
    price_adjustment = 0
    infont = 0
    infont_dollar = 0
    for i in packages:
        if (i.InfontPrice or 0) > 0 or (i.InfontPrice_doller and i.InfontPrice_doller > 0):
            infont = i.InfontPrice
            infont_dollar = int(i.InfontPrice_doller or 0)
            break

    total = len(packages)
    MAX_PER_PAGE = 8

    if total == 0:
        page_packages = [[]]
    else:
        pages_needed = max(1, ceil(total / MAX_PER_PAGE))
        per_page = ceil(total / pages_needed)
        page_packages = [packages[i:i + per_page] for i in range(0, total, per_page)]

    tour_image_b64 = _image_to_b64(tour.TourImage) if tour.TourImage else None

    tour_main_b64 = None
    if not tour_image_b64 and tour.tour_main:
        tour_main_b64 = _image_to_b64(tour.tour_main)

    airline_logo_b64 = None
    if tc and tc.Airline and tc.Airline.AirlineLogo:
        airline_logo_b64 = _image_to_b64(tc.Airline.AirlineLogo)

    context = {
        'Tour': tour,
        'svc_desc': _strip_html(tour.ShortDsc, max_chars=400),
        'doc_desc': _strip_html(tour.documents, max_chars=400),
        'note_desc': _strip_html(tour.pdfdesc, max_chars=400),
        'tour_image_b64': tour_image_b64 or tour_main_b64,
        'airline_logo_b64': airline_logo_b64,
        'packages': packages,
        'page_packages': page_packages,
        'tourcity': tc,
        'lc': lc,
        'infont': infont,
        'infont_dollar': infont_dollar,
        'selected_dp': selected_dp,
        'price_adjustment': price_adjustment,
    }
    html = render_to_string('pdf/package_pdf.html', context)
    html = HTML(string=html, base_url=request.build_absolute_uri())
    font_file = os.path.join(settings.STATIC_ROOT, 'asset', 'css', 'fonts', 'arezoosafar.ttf')
    font_url = 'file:///' + font_file.replace('\\', '/')
    font_css = CSS(string=f"@font-face{{font-family:'ArezooPDF';src:url('{font_url}')format('truetype');}}")
    pdf = html.write_pdf(presentational_hints=True, stylesheets=[font_css])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="package.pdf"'
    return response

def mypdf2(request, id):
    tour = Tour.objects.get(id=id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    tc = cities.first()
    lc = cities.last()
    packages = packages_for_date(tour)
    pcount = len(packages)
    if not packages:
        raise Http404('برای این تور پکیجی برای نمایش وجود ندارد')
    infont = next((i.InfontPrice for i in packages if i.InfontPrice > 0), 0)
    if packages[0].Mhotel and not packages[0].M1hotel:
        per_page = 10  # Define how many packages per page
        num_pages = ceil(pcount / per_page)  # Calculate total number of pages
        pdf_document = None
        for page_num in range(num_pages):
            start_idx = page_num * per_page
            end_idx = (page_num + 1) * per_page
            current_packages = packages[start_idx:end_idx]

            html = render_to_string('ui/tour-pdf.html', {
                'Tour': tour,
                'packages': current_packages,
                'tourcity': tc,
                'lc': lc,
                'infont': infont
            })

            if pdf_document is None:
                pdf_document = HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                        presentational_hints=True)
            else:
                pdf_document.pages.append(HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                                    presentational_hints=True).pages[0])

        pdf = pdf_document.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                    presentational_hints=True)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="package.pdf"'
        return response
    if packages[0].M1hotel and not packages[0].M2hotel:
        per_page = 8
        num_pages = ceil(pcount / per_page)
        pdf_document = None
        for page_num in range(num_pages):
            start_idx = page_num * per_page
            end_idx = (page_num + 1) * per_page
            current_packages = packages[start_idx:end_idx]

            html = render_to_string('ui/tour-pdf.html', {
                'Tour': tour,
                'packages': current_packages,
                'tourcity': tc,
                'lc': lc,
                'infont': infont
            })

            if pdf_document is None:
                pdf_document = HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                        presentational_hints=True)
            else:
                pdf_document.pages.append(HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                                    presentational_hints=True).pages[0])

        pdf = pdf_document.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                    presentational_hints=True)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="package.pdf"'
        return response
    if packages[0].M2hotel and not packages[0].M3hotel:
        per_page = 6  # Define how many packages per page
        num_pages = ceil(pcount / per_page)  # Calculate total number of pages
        pdf_document = None
        for page_num in range(num_pages):
            start_idx = page_num * per_page
            end_idx = (page_num + 1) * per_page
            current_packages = packages[start_idx:end_idx]

            html = render_to_string('ui/tour-pdf.html', {
                'Tour': tour,
                'packages': current_packages,
                'tourcity': tc,
                'lc': lc,
                'infont': infont
            })

            if pdf_document is None:
                pdf_document = HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                        presentational_hints=True)
            else:
                pdf_document.pages.append(HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                                    presentational_hints=True).pages[0])

        pdf = pdf_document.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                    presentational_hints=True)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="package.pdf"'
        return response
    if packages[0].M3hotel and not packages[0].M4hotel:
        per_page = 5  # Define how many packages per page
        num_pages = ceil(pcount / per_page)  # Calculate total number of pages
        pdf_document = None
        for page_num in range(num_pages):
            start_idx = page_num * per_page
            end_idx = (page_num + 1) * per_page
            current_packages = packages[start_idx:end_idx]

            html = render_to_string('ui/tour-pdf.html', {
                'Tour': tour,
                'packages': current_packages,
                'tourcity': tc,
                'lc': lc,
                'infont': infont
            })

            if pdf_document is None:
                pdf_document = HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                        presentational_hints=True)
            else:
                pdf_document.pages.append(HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                                    presentational_hints=True).pages[0])

        pdf = pdf_document.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                    presentational_hints=True)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="package.pdf"'
        return response
    per_page = 20  # Define how many packages per page
    num_pages = ceil(pcount / per_page)  # Calculate total number of pages
    pdf_document = None
    for page_num in range(num_pages):
        start_idx = page_num * per_page
        end_idx = (page_num + 1) * per_page
        current_packages = packages[start_idx:end_idx]

        html = render_to_string('ui/tour-pdf.html', {
            'Tour': tour,
            'packages': current_packages,
            'tourcity': tc,
            'lc': lc,
            'infont': infont
        })

        if pdf_document is None:
            pdf_document = HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                     presentational_hints=True)
        else:
            pdf_document.pages.append(HTML(string=html).render(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                                                presentational_hints=True).pages[0])

    pdf = pdf_document.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '/asset/css/uistyle.css')],
                                 presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="package.pdf"'
    return response