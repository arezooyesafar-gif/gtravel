from django.db import migrations, models


def move_dollar_adjustments(apps, schema_editor):
    date_plan = apps.get_model('tour', 'date_plan')
    for row in date_plan.objects.filter(price_currency='دلار'):
        row.price_dollar = row.price or 0
        row.price = 0
        row.infant_price_dollar = row.infant_price or 0
        row.infant_price = 0
        row.save(update_fields=['price', 'price_dollar', 'infant_price', 'infant_price_dollar'])


def reverse_move_dollar_adjustments(apps, schema_editor):
    date_plan = apps.get_model('tour', 'date_plan')
    for row in date_plan.objects.filter(price_currency='دلار'):
        row.price = row.price_dollar or 0
        row.infant_price = row.infant_price_dollar or 0
        row.save(update_fields=['price', 'infant_price'])


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0039_tour_force_pub'),
    ]

    operations = [
        migrations.AddField(
            model_name='date_plan',
            name='price_dollar',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='اختلاف قیمت ارز دوم'),
        ),
        migrations.AddField(
            model_name='date_plan',
            name='infant_price_dollar',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='افزایش قیمت نوزاد ارز دوم'),
        ),
        migrations.AlterField(
            model_name='date_plan',
            name='price',
            field=models.IntegerField(default=0, verbose_name='اختلاف قیمت ارز اول'),
        ),
        migrations.AlterField(
            model_name='date_plan',
            name='infant_price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='افزایش قیمت نوزاد ارز اول'),
        ),
        migrations.RunPython(move_dollar_adjustments, reverse_move_dollar_adjustments),
    ]
