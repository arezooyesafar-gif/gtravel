from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0044_apipartner'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourorder',
            name='api_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='tour.apipartner', verbose_name='ثبت\u200cشده از طریق آژانس (API)'),
        ),
    ]