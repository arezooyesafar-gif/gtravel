from django.apps import apps
from django.db import models

BAD_CHARS = ("Ø", "Ù", "Ú", "Û", "Ð", "Ñ", "Â", "Ã", "â")
SKIP_APPS = {
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "sites",
    "captcha",
    "webp_converter",
}

def looks_bad(value):
    return isinstance(value, str) and any(ch in value for ch in BAD_CHARS)

def fix_text(value):
    if not looks_bad(value):
        return value

    for enc in ("cp1252", "latin1"):
        try:
            fixed = value.encode(enc).decode("utf-8")
            return fixed
        except Exception:
            pass

    return value

total_objects = 0
total_fields = 0

for Model in apps.get_models():
    if Model._meta.app_label in SKIP_APPS:
        continue

    fields = []
    for f in Model._meta.fields:
        if isinstance(f, (models.CharField, models.TextField)) and not isinstance(
            f,
            (
                models.FileField,
                models.ImageField,
                models.URLField,
                models.EmailField,
                models.SlugField,
            ),
        ):
            fields.append(f)

    if not fields:
        continue

    try:
        qs = Model.objects.all()
    except Exception as e:
        print("SKIP MODEL:", Model.__name__, e)
        continue

    for obj in qs.iterator():
        changed_fields = []

        for f in fields:
            old = getattr(obj, f.name, None)
            new = fix_text(old)

            if new != old:
                setattr(obj, f.name, new)
                changed_fields.append(f.name)

        if changed_fields:
            try:
                obj.save(update_fields=changed_fields)
                total_objects += 1
                total_fields += len(changed_fields)
                print("FIXED:", Model.__name__, "id=", obj.pk, changed_fields)
            except Exception as e:
                print("SAVE ERROR:", Model.__name__, "id=", obj.pk, e)

print("DONE")
print("Fixed objects:", total_objects)
print("Fixed fields:", total_fields)