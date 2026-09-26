import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0041_date_plan_price_dollar_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='cancel_policy',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=6000, null=True, verbose_name='قوانین کنسلی'),
        ),
        migrations.AddField(
            model_name='tour',
            name='about_tour',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=15000, null=True, verbose_name='درباره تور'),
        ),
    ]
