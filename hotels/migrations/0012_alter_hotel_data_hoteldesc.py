import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_alter_hotel_data_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel_data',
            name='HotelDesc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000000, null=True),
        ),
    ]
