from django.db import migrations

from staff.redirect_rules import clean_path, clean_target


def normalize_paths(apps, schema_editor):
    RedirectRule = apps.get_model('staff', 'RedirectRule')
    for rule in RedirectRule.objects.order_by('id'):
        old_path = clean_path(rule.old_path.lstrip('/')) or '/'
        new_path = '' if rule.status == 410 else clean_target(rule.new_path)
        if old_path == rule.old_path and new_path == rule.new_path:
            continue
        if old_path != rule.old_path and RedirectRule.objects.filter(old_path=old_path).exclude(id=rule.id).exists():
            rule.delete()
            continue
        rule.old_path = old_path
        rule.new_path = new_path
        rule.save(update_fields=['old_path', 'new_path'])


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_redirectrule'),
    ]

    operations = [
        migrations.RunPython(normalize_paths, migrations.RunPython.noop),
    ]
