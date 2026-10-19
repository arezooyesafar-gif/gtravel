import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0055_alter_country_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='Description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000000, null=True),
        ),
    ]
