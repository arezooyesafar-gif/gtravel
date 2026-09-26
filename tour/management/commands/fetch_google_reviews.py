# -*- coding: utf-8 -*-
"""دریافت نظرهای گوگل مپ از خط فرمان.

برای زمان‌بندی (Task Scheduler) روی سرور:
    .venv\\Scripts\\python.exe manage.py fetch_google_reviews
"""
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from theme.models import index_page
from tour.google_reviews import GoogleReviewsError, sync_from_google


class Command(BaseCommand):
    help = 'نظرهای گوگل مپ آژانس را می‌خواند و در جدول نظرات ثبت می‌کند.'

    def add_arguments(self, parser):
        parser.add_argument('--language', default='fa',
                            help='زبان درخواستی از گوگل (پیش‌فرض fa)')

    def handle(self, *args, **options):
        setting = index_page.objects.first()
        if setting is None:
            raise CommandError('تنظیمات قالب هنوز ساخته نشده است.')
        try:
            result = sync_from_google(setting, language=options['language'])
        except GoogleReviewsError as exc:
            raise CommandError(exc.message)

        cache.clear()
        self.stdout.write(self.style.SUCCESS(
            'مکان: %s | امتیاز %s از %s نظر' % (
                result['place'], result['rating'], result['total_ratings'])))
        self.stdout.write(
            'دریافت‌شده: %d | جدید: %d | به‌روزرسانی: %d | تکراری: %d' % (
                result['fetched'], result['created'],
                result['updated'], result['skipped']))
