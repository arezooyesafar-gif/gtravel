import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0054_package_transfer_m1hotel_package_transfer_m2hotel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='Description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000000, null=True),
        ),
    ]
