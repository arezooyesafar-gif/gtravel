from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('tour', '0034_footer_dollar_rate')]
    operations = [migrations.CreateModel(name='TourInterest', fields=[
        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.CharField(max_length=100)),
        ('family', models.CharField(max_length=100)),
        ('phone', models.CharField(max_length=20)),
        ('page_type', models.CharField(blank=True, max_length=20)),
        ('page_slug', models.CharField(blank=True, max_length=200)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
    ])]
