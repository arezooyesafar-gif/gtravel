from django.shortcuts import render
from visa.forms import visa_request_form
from visa.models import visa_request_item
from weasyprint import HTML, CSS
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.conf import settings

def visa_pdf(request, id):
    item = visa_request_item.objects.get(id=id)
    forms = visa_request_form(instance=item)
    context = {
        'item': item,
        'forms': forms
    }
    return render(request, 'layout/pdf.html', context)
