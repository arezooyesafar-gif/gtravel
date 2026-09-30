from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogposts_meta_robots'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposts',
            name='author',
            field=models.CharField(blank=True, default='حدیثه محمدی', max_length=150, verbose_name='نویسنده'),
        ),
    ]
