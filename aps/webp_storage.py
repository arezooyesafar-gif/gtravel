import io
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

try:
    from PIL import Image
except Exception:
    Image = None

CONVERTIBLE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}


class WebPStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if Image is not None and name:
            root, ext = os.path.splitext(name)
            if ext.lower() in CONVERTIBLE_EXTENSIONS:
                converted = self._to_webp(content)
                if converted is not None:
                    name = root + '.webp'
                    content = converted
        return super().save(name, content, max_length=max_length)

    def _to_webp(self, content):
        quality = getattr(settings, 'WEBP_UPLOAD_QUALITY', 80)
        try:
            content.seek(0)
        except Exception:
            pass
        try:
            image = Image.open(content)
            if (image.format or '').upper() == 'WEBP':
                return None
            image.load()
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                image = image.convert('RGBA')
            else:
                image = image.convert('RGB')
            buffer = io.BytesIO()
            image.save(buffer, format='WEBP', quality=quality, method=4)
            return ContentFile(buffer.getvalue())
        except Exception:
            try:
                content.seek(0)
            except Exception:
                pass
            return None
