from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_hotel_services_paid_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel_data',
            name='Slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
