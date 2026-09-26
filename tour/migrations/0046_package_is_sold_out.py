from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0045_tourorder_api_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='is_sold_out',
            field=models.BooleanField(default=False, verbose_name='پر شده / موجود نیست'),
        ),
    ]
