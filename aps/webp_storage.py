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
        if name:
            root, ext = os.path.splitext(name)
            ext = ext.lower()
            if Image is not None and ext in CONVERTIBLE_EXTENSIONS:
                converted = self._to_webp(content)
                if converted is not None:
                    name = root + '.webp'
                    content = converted
            elif ext == '.pdf':
                compressed = self._compress_pdf(content)
                if compressed is not None:
                    content = compressed
        return super().save(name, content, max_length=max_length)

    def _to_webp(self, content):
        quality = getattr(settings, 'WEBP_UPLOAD_QUALITY', 80)
        self._rewind(content)
        try:
            image = Image.open(content)
            if (image.format or '').upper() == 'WEBP':
                self._rewind(content)
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
            self._rewind(content)
            return None

    def _compress_pdf(self, content):
        self._rewind(content)
        try:
            original = content.read()
        except Exception:
            self._rewind(content)
            return None
        if not original:
            self._rewind(content)
            return None
        try:
            import pikepdf
        except Exception:
            self._rewind(content)
            return None
        try:
            buffer = io.BytesIO()
            with pikepdf.open(io.BytesIO(original)) as pdf:
                pdf.save(
                    buffer,
                    compress_streams=True,
                    object_stream_mode=pikepdf.ObjectStreamMode.generate,
                )
            data = buffer.getvalue()
            if data and len(data) < len(original):
                return ContentFile(data)
        except Exception:
            pass
        self._rewind(content)
        return None

    @staticmethod
    def _rewind(content):
        try:
            content.seek(0)
        except Exception:
            pass
