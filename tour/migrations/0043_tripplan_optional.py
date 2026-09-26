import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0042_tour_cancel_policy_about_tour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripplan',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='tripplan',
            name='plan_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=75, scale=None, size=[1920, 1080], upload_to='media/trip-plan/main-images'),
        ),
    ]