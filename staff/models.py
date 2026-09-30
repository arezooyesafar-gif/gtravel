from django.contrib.auth.models import User
from django.db import models

ACTIONS = [
    ('view', 'مشاهده'),
    ('add', 'ایجاد'),
    ('edit', 'ویرایش'),
    ('delete', 'حذف'),
]

AREAS = [
    ('tours', 'تورها'),
    ('packages', 'پکیج ها'),
    ('hotels', 'هتل ها'),
    ('destinations', 'مقاصد (کشور و شهر)'),
    ('flights', 'پروازها (ایرلاین و فرودگاه)'),
    ('blog', 'مجله گردشگری'),
    ('memories', 'سفرنامه'),
    ('pages', 'صفحات و فایل ها'),
    ('orders', 'رزرو و سفارشات'),
    ('reviews', 'نظرات مشتریان'),
    ('messages', 'پیام ها و مخاطبین'),
    ('visas', 'درخواست های ویزا'),
    ('users', 'کاربران'),
    ('settings', 'تنظیمات سایت'),
]

AREA_LABELS = dict(AREAS)
ACTION_LABELS = dict(ACTIONS)


class StaffAccess(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_access')
    permissions = models.TextField(blank=True, default='')
    note = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دسترسی پشتیبان'
        verbose_name_plural = 'دسترسی پشتیبان ها'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def codes(self):
        return {code for code in self.permissions.split(',') if code}

    def set_codes(self, codes):
        allowed = {'%s:%s' % (area, action) for area, _ in AREAS for action, _ in ACTIONS}
        self.permissions = ','.join(sorted(code for code in codes if code in allowed))

    def has(self, area, action):
        return '%s:%s' % (area, action) in self.codes

    def area_actions(self, area):
        return [action for action, _ in ACTIONS if self.has(area, action)]

    def allowed_areas(self):
        return [area for area, _ in AREAS if self.area_actions(area)]

    def summary(self):
        parts = []
        for area, area_label in AREAS:
            actions = self.area_actions(area)
            if actions:
                parts.append('%s: %s' % (area_label, '، '.join(ACTION_LABELS[a] for a in actions)))
        return ' | '.join(parts)


class ObjectStamp(models.Model):
    model_label = models.CharField(max_length=100)
    object_id = models.CharField(max_length=40)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    updated_name = models.CharField(max_length=150, blank=True, default='')
    updated_at = models.DateTimeField()

    class Meta:
        unique_together = [('model_label', 'object_id')]
        verbose_name = 'آخرین تغییر'
        verbose_name_plural = 'آخرین تغییرات'

    def __str__(self):
        return '%s #%s %s' % (self.model_label, self.object_id, self.updated_name)


class ChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='change_logs')
    username = models.CharField(max_length=150, blank=True, default='')
    action = models.CharField(max_length=10, choices=ACTIONS)
    area = models.CharField(max_length=30, blank=True, default='')
    model_label = models.CharField(max_length=100, blank=True, default='')
    model_title = models.CharField(max_length=150, blank=True, default='')
    object_id = models.CharField(max_length=40, blank=True, default='')
    title = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'تغییر کاربر'
        verbose_name_plural = 'تاریخچه تغییرات'

    def __str__(self):
        return '%s %s %s' % (self.username, self.action, self.title)

    @property
    def action_label(self):
        return ACTION_LABELS.get(self.action, self.action)

    @property
    def area_label(self):
        return AREA_LABELS.get(self.area, self.area)


REDIRECT_STATUSES = [
    (301, '301 - انتقال دائمی'),
    (302, '302 - انتقال موقت'),
    (410, '410 - حذف شده'),
]


class RedirectRule(models.Model):
    old_path = models.CharField(max_length=400, unique=True, db_index=True)
    new_path = models.CharField(max_length=400, blank=True, default='')
    status = models.IntegerField(choices=REDIRECT_STATUSES, default=301)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['old_path']
        verbose_name = 'ریدایرکت'
        verbose_name_plural = 'ریدایرکت ها'

    def __str__(self):
        return '%s -> %s' % (self.old_path, self.new_path or str(self.status))
