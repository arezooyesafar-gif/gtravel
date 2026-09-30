from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0002_objectstamp"),
    ]

    operations = [
        migrations.CreateModel(
            name="RedirectRule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "old_path",
                    models.CharField(db_index=True, max_length=400, unique=True),
                ),
                ("new_path", models.CharField(blank=True, default="", max_length=400)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (301, "301 - انتقال دائمی"),
                            (302, "302 - انتقال موقت"),
                            (410, "410 - حذف شده"),
                        ],
                        default=301,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "ریدایرکت",
                "verbose_name_plural": "ریدایرکت ها",
                "ordering": ["old_path"],
            },
        ),
    ]
