from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0040_date_plan_price_dollar_infant_dollar'),
    ]

    operations = [
        migrations.AddField(
            model_name='date_plan',
            name='price_dollar_type',
            field=models.CharField(blank=True, choices=[('', 'انتخاب نوع اختلاف قیمت'), ('طبق پکیج اصلی', 'طبق پکیج اصلی'), ('افزایش', 'افزایش'), ('کاهش', 'کاهش')], default='طبق پکیج اصلی', max_length=300, null=True, verbose_name='نوع اختلاف ارز دوم'),
        ),
    ]
