from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0012_alter_hotel_data_hoteldesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel_data',
            name='short_url',
            field=models.BooleanField(default=False),
        ),
    ]
