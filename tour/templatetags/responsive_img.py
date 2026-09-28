
import logging
import os

import html as html_lib
import re
from urllib.parse import unquote

from django import template
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

register = template.Library()
logger = logging.getLogger(__name__)

DEFAULT_WIDTHS = (480, 768, 1200, 1600)
CACHE_PREFIX = "resized_cache/"
QUALITY = 78

_known_bad = set()


def _field_file(value):
    if not value:
        return None
    name = getattr(value, "name", None)
    if not name:
        return None
    return value


def _variant_path(name, width):
    root, _ext = os.path.splitext(name)
    return "%s%s_%dw.webp" % (CACHE_PREFIX, root, width)


def _open_image(field_file):
    from PIL import Image

    field_file.open("rb")
    try:
        im = Image.open(field_file)
        im.load()
        return im
    finally:
        field_file.close()


def _natural_size(field_file):
    name = field_file.name
    if name in _known_bad:
        return None

    ck = "respimg:size:%s" % name
    hit = cache.get(ck)
    if hit is not None:
        return tuple(hit) if hit else None

    from PIL import Image

    try:
        field_file.open("rb")
        try:
            im = Image.open(field_file)
            size = im.size
        finally:
            field_file.close()
        cache.set(ck, list(size), 60 * 60 * 24 * 30)
        return size
    except Exception as exc:
        _known_bad.add(name)
        cache.set(ck, [], 60 * 60 * 6)
        logger.warning("responsive_img: could not read size of %s (%s)", name, exc)
        return None


def _ensure_variant(field_file, name, width, natural_size):
    variant_name = _variant_path(name, width)
    ck = "respimg:var:%s" % variant_name
    hit = cache.get(ck)
    if hit is not None:
        return hit or None
    if default_storage.exists(variant_name):
        url = default_storage.url(variant_name)
        cache.set(ck, url, 60 * 60 * 24 * 30)
        return url

    try:
        from PIL import Image, ImageOps

        orig_w, orig_h = natural_size
        if width >= orig_w:
            cache.set(ck, "", 60 * 60 * 24 * 30)
            return None

        im = _open_image(field_file)
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.mode else "RGB")

        target_h = round(orig_h * (width / float(orig_w)))
        resized = im.resize((width, target_h), Image.LANCZOS)

        from io import BytesIO
        buf = BytesIO()
        resized.save(buf, format="WEBP", quality=QUALITY, method=6)
        buf.seek(0)
        default_storage.save(variant_name, ContentFile(buf.read()))
        url = default_storage.url(variant_name)
        cache.set(ck, url, 60 * 60 * 24 * 30)
        return url
    except Exception as exc:
        _known_bad.add(name)
        logger.warning("responsive_img: could not build %s @%dw (%s)", name, width, exc)
        return None


def build_srcset(field_file, widths=DEFAULT_WIDTHS):
    field_file = _field_file(field_file)
    if field_file is None:
        return []

    natural_size = _natural_size(field_file)
    if not natural_size:
        return []

    name = field_file.name
    entries = []
    for width in sorted(set(widths)):
        url = _ensure_variant(field_file, name, width, natural_size)
        if url:
            entries.append((url, width))
    return entries


@register.simple_tag
def srcset_for(field_file, widths=DEFAULT_WIDTHS):
    if isinstance(widths, str):
        widths = [int(w) for w in widths.split(",") if w.strip()]
    entries = build_srcset(field_file, widths)
    if not entries:
        return ""
    return mark_safe(", ".join("%s %dw" % (url, w) for url, w in entries))


@register.simple_tag
def img_url_at(field_file, width):
    field_file = _field_file(field_file)
    if field_file is None:
        return ""
    width = int(width)
    natural_size = _natural_size(field_file)
    if not natural_size:
        return field_file.url
    url = _ensure_variant(field_file, field_file.name, width, natural_size)
    return url or field_file.url


@register.simple_tag
def img_dimensions(field_file):
    field_file = _field_file(field_file)
    if field_file is None:
        return ""
    natural_size = _natural_size(field_file)
    if not natural_size:
        return ""
    w, h = natural_size
    return mark_safe('width="%d" height="%d"' % (w, h))


@register.simple_tag
def srcset_with_original(field_file, widths=DEFAULT_WIDTHS):
    if isinstance(widths, str):
        widths = [int(w) for w in widths.split(",") if w.strip()]
    field_file = _field_file(field_file)
    if field_file is None:
        return ""
    natural_size = _natural_size(field_file)
    if not natural_size:
        return ""
    entries = ["%s %dw" % (url, w) for url, w in build_srcset(field_file, widths)]
    entries.append("%s %dw" % (field_file.url, natural_size[0]))
    return mark_safe(", ".join(entries))


class _StoredImage:
    def __init__(self, name):
        self.name = name
        self._fh = None

    def open(self, mode="rb"):
        self._fh = default_storage.open(self.name, mode)
        return self

    def __getattr__(self, attr):
        fh = self.__dict__.get("_fh")
        if fh is None:
            raise AttributeError(attr)
        return getattr(fh, attr)

    def close(self):
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    @property
    def url(self):
        return default_storage.url(self.name)


def _existing_variant(name, width):
    variant_name = _variant_path(name, width)
    ck = "respimg:var:%s" % variant_name
    hit = cache.get(ck)
    if hit is not None:
        return hit or None, True
    if default_storage.exists(variant_name):
        url = default_storage.url(variant_name)
        cache.set(ck, url, 60 * 60 * 24 * 30)
        return url, True
    return None, False


_IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
_SRC_ATTR = re.compile(r"""\ssrc\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
BODY_WIDTHS = (480, 768, 1200)
BODY_SIZES = "(max-width: 991px) calc(100vw - 84px), 862px"
BODY_BUILD_BUDGET = 2


def _has_attr(tag_lower, attr):
    return re.search(r"\s%s\s*=" % attr, tag_lower) is not None


def _body_image_name(src, media_url):
    path = html_lib.unescape(src).split("?", 1)[0].split("#", 1)[0]
    if not path.startswith(media_url):
        return None
    return unquote(path[len(media_url):])


def responsive_body_images(value, sizes=BODY_SIZES, widths=BODY_WIDTHS, budget=BODY_BUILD_BUDGET):
    if not value or "<img" not in str(value).lower():
        return value
    text = str(value)
    media_url = settings.MEDIA_URL or "/media/"
    if not media_url.startswith("/"):
        media_url = "/" + media_url
    widths = sorted(set(widths))

    found = {}
    for tag in _IMG_TAG.findall(text):
        src_match = _SRC_ATTR.search(tag)
        if not src_match:
            continue
        src = src_match.group(1) if src_match.group(1) is not None else src_match.group(2)
        name = _body_image_name(src, media_url)
        if name and name not in found:
            stored = _StoredImage(name)
            natural_size = _natural_size(stored)
            if natural_size:
                found[name] = (stored, natural_size)

    ready = {}
    missing = []
    for name, (stored, natural_size) in found.items():
        for width in widths:
            if width >= natural_size[0]:
                break
            url, known = _existing_variant(name, width)
            if url:
                ready[(name, width)] = url
            elif not known:
                missing.append((name, width))
    priority = {w: i for i, w in enumerate(sorted(widths, key=lambda w: (w != 768, w)))}
    missing.sort(key=lambda item: priority[item[1]])
    for name, width in missing[:max(budget, 0)]:
        stored, natural_size = found[name]
        url = _ensure_variant(stored, name, width, natural_size)
        if url:
            ready[(name, width)] = url

    def rewrite(match):
        tag = match.group(0)
        low = tag.lower()
        extra = []
        if not _has_attr(low, "loading"):
            extra.append('loading="lazy"')
        if not _has_attr(low, "decoding"):
            extra.append('decoding="async"')
        src_match = _SRC_ATTR.search(tag)
        if src_match and not _has_attr(low, "srcset"):
            src = src_match.group(1) if src_match.group(1) is not None else src_match.group(2)
            name = _body_image_name(src, media_url)
            if name in found:
                natural_size = found[name][1]
                if not _has_attr(low, "width") and not _has_attr(low, "height"):
                    extra.append('width="%d" height="%d"' % natural_size)
                entries = ["%s %dw" % (ready[(name, w)], w) for w in widths if (name, w) in ready]
                if entries:
                    entries.append("%s %dw" % (src, natural_size[0]))
                    extra.append('srcset="%s" sizes="%s"' % (", ".join(entries), sizes))
        if not extra:
            return tag
        body = tag[:-1].rstrip()
        closing = ">"
        if body.endswith("/"):
            body = body[:-1].rstrip()
            closing = " />"
        return "%s %s%s" % (body, " ".join(extra), closing)

    return mark_safe(_IMG_TAG.sub(rewrite, text))


@register.filter(name="responsive_html", is_safe=True)
def responsive_html(value):
    return responsive_body_images(value)


@register.simple_tag
def srcset_existing(field_file, widths="480,768"):
    if isinstance(widths, str):
        widths = [int(w) for w in widths.split(",") if w.strip()]
    field_file = _field_file(field_file)
    if field_file is None:
        return ""
    natural_size = _natural_size(field_file)
    if not natural_size:
        return ""
    entries = []
    for width in sorted(set(widths)):
        if width >= natural_size[0]:
            break
        url, _known = _existing_variant(field_file.name, width)
        if url:
            entries.append("%s %dw" % (url, width))
    entries.append("%s %dw" % (field_file.url, natural_size[0]))
    return mark_safe(", ".join(entries))


@register.simple_tag(takes_context=True)
def srcset_budget(context, field_file, widths="480,768", budget=3):
    if isinstance(widths, str):
        widths = [int(w) for w in widths.split(",") if w.strip()]
    field_file = _field_file(field_file)
    if field_file is None:
        return ""
    natural_size = _natural_size(field_file)
    if not natural_size:
        return ""
    state = context.render_context.setdefault("respimg_budget", {"left": int(budget)})
    entries = []
    for width in sorted(set(widths)):
        if width >= natural_size[0]:
            break
        url, known = _existing_variant(field_file.name, width)
        if not known and state["left"] > 0:
            state["left"] -= 1
            url = _ensure_variant(field_file, field_file.name, width, natural_size)
        if url:
            entries.append("%s %dw" % (url, width))
    entries.append("%s %dw" % (field_file.url, natural_size[0]))
    return mark_safe(", ".join(entries))
