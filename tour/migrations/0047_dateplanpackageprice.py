import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0046_package_is_sold_out'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatePlanPackagePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DoubleBedPrice', models.IntegerField(default=0, verbose_name='قیمت اتاق دوتخته')),
                ('SingleBedPrice', models.IntegerField(default=0, verbose_name='قیمت اتاق یک تخته')),
                ('BabyWithBedPrice', models.IntegerField(default=0, verbose_name='قیمت کودک با تخت')),
                ('BabyWithoutBedPrice', models.IntegerField(default=0, verbose_name='قیمت کودک بدون تخت')),
                ('InfontPrice', models.IntegerField(default=0, verbose_name='قیمت نوزاد')),
                ('DoubleBedPrice_doller', models.IntegerField(default=0, verbose_name='قیمت اتاق دوتخته (ارز دوم)')),
                ('SingleBedPrice_doller', models.IntegerField(default=0, verbose_name='قیمت اتاق یک تخته (ارز دوم)')),
                ('BabyWithBedPrice_doller', models.IntegerField(default=0, verbose_name='قیمت کودک با تخت (ارز دوم)')),
                ('BabyWithoutBedPrice_doller', models.IntegerField(default=0, verbose_name='قیمت کودک بدون تخت (ارز دوم)')),
                ('InfontPrice_doller', models.IntegerField(default=0, verbose_name='قیمت نوزاد (ارز دوم)')),
                ('date_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_prices', to='tour.date_plan')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_plan_overrides', to='tour.package')),
            ],
            options={
                'verbose_name': 'قیمت دستی هتل برای تاریخ',
                'verbose_name_plural': 'قیمت های دستی هتل برای تاریخ',
                'unique_together': {('date_plan', 'package')},
            },
        ),
    ]
