from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0043_tripplan_optional'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام آژانس / همکار')),
                ('api_key', models.CharField(editable=False, max_length=64, unique=True, verbose_name='کلید API')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('note', models.CharField(blank=True, max_length=300, null=True, verbose_name='توضیحات')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('last_used_at', models.DateTimeField(blank=True, null=True, verbose_name='آخرین استفاده')),
            ],
            options={
                'verbose_name': 'کلید دسترسی API تور',
                'verbose_name_plural': 'کلیدهای دسترسی API تور',
            },
        ),
    ]
