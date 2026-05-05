from math import ceil

from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse
from .models import *
from .forms import *

def mypdf(request, id):
    tour = Tour.objects.get(id=id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    tc = cities.first()
    lc = cities.last()
    packages = Package.objects.filter(TourName=tour.id).order_by('DoubleBedPrice_doller')
    infont = 0
    for i in packages:
        if i.InfontPrice > 0:
            infont = i.InfontPrice
            break
    context = {
        'Tour': tour,
        'packages': packages,
        'tourcity': tc,
        'lc': lc,
        'infont': infont,
    }
    template = get_template('ui/tour-pdf.html')
    html = render_to_string('ui/tour-pdf.html', context)
    html = HTML(string=html, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  '/asset/css/uistyle.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="package.pdf"'
    return response
    # # return render(request, 'ui/tour-pdf.html', context)

def mypdf2(request, id):
    tour = Tour.objects.get(id=id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    tc = cities.first()
    lc = cities.last()
    packages = Package.objects.filter(TourName=tour.id).order_by('DoubleBedPrice_doller')
    pcount = packages.count()
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