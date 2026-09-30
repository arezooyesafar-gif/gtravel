import re

import django.db.models.deletion
from django.db import migrations, models


def normalize(text):
    text = (text or '').replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ')
    return re.sub(r'\s+', ' ', text).strip().lower()


def fill_country(apps, schema_editor):
    Country = apps.get_model('tour', 'Country')
    PostCategory = apps.get_model('blog', 'PostCategory')
    countries = [(normalize(c.TitleC), (c.slug or '').lower(), c.id) for c in Country.objects.all()]
    for category in PostCategory.objects.filter(country__isnull=True):
        name = ' %s ' % ' '.join(re.split(r'[\s\-_،,:|()]+', normalize(category.CatName)))
        slug_parts = set(re.split(r'[-_]', (category.slug or '').lower()))
        matches = {}
        for title, slug, country_id in countries:
            if title and len(title) >= 2 and (' %s ' % title) in name:
                matches[country_id] = True
            if slug and slug in slug_parts:
                matches[country_id] = True
        if len(matches) == 1:
            category.country_id = next(iter(matches))
            category.save(update_fields=['country'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogposts_author'),
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategory',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_categories', to='tour.country', verbose_name='کشور'),
        ),
        migrations.RunPython(fill_country, migrations.RunPython.noop),
    ]
