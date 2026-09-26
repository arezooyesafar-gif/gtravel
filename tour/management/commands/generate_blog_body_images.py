from django.core.management.base import BaseCommand

from blog.models import blogPosts
from tour.templatetags.responsive_img import build_srcset, responsive_body_images


class Command(BaseCommand):
    help = "Pre-generate WEBP variants for images inside blog post bodies"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--post", type=int, default=None)

    def handle(self, *args, **options):
        qs = blogPosts.objects.only("id", "Image", "ShortDesc", "Description").order_by("-id")
        if options.get("post"):
            qs = qs.filter(id=options["post"])
        if options.get("limit"):
            qs = qs[:options["limit"]]
        done = 0
        for post in qs:
            try:
                build_srcset(post.Image, (480, 768))
                responsive_body_images(post.ShortDesc, budget=10 ** 6)
                responsive_body_images(post.Description, budget=10 ** 6)
                done += 1
                self.stdout.write("post %s ok" % post.id)
            except Exception as exc:
                self.stderr.write("post %s failed: %s" % (post.id, exc))
        self.stdout.write(self.style.SUCCESS("Done. %d post(s) processed." % done))
