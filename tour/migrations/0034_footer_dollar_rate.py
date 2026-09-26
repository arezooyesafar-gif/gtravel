from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('tour', '0033_contactus_createdat'),
    ]
    operations = [
        migrations.AddField(
            model_name='footer',
            name='dollar_rate',
            field=models.IntegerField(default=90000, verbose_name='نرخ دلار به تومان'),
        ),
    ]
