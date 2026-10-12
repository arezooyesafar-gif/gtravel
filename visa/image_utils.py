import io
import os
import re

from django import forms
from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def _safe_base(name):
    base = os.path.splitext(os.path.basename(name or ''))[0]
    base = re.sub(r'[^A-Za-z0-9_-]+', '_', base).strip('_')
    return base or 'img'


def _open_image(data):
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
        return image
    except Exception:
        return None


def _open_pdf(data):
    try:
        import pymupdf as fitz
    except Exception:
        try:
            import fitz
        except Exception:
            return None
    try:
        document = fitz.open(stream=data, filetype='pdf')
        page = document.load_page(0)
        pixmap = page.get_pixmap(dpi=200)
        image = Image.open(io.BytesIO(pixmap.tobytes('png')))
        image.load()
        return image
    except Exception:
        return None


def to_jpeg(uploaded):
    data = uploaded.read()
    try:
        uploaded.seek(0)
    except Exception:
        pass
    image = _open_image(data)
    if image is None:
        image = _open_pdf(data)
    if image is None:
        raise forms.ValidationError('فرمت فایل پشتیبانی نمی‌شود؛ یک تصویر یا فایل PDF ارسال کنید.')
    image = ImageOps.exif_transpose(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=85, optimize=True)
    return ContentFile(output.getvalue(), name=_safe_base(uploaded.name) + '.jpg')
