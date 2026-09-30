from tour.models import Tour

from .seo_sitemaps import good_slug


def related_tours_for_post(post, limit=3):
    category = post.Category
    country_id = None
    while category is not None and country_id is None:
        country_id = category.country_id
        category = category.parentCat
    if country_id is None:
        return []
    tours = Tour.objects.filter(PubTour=True, Tcountry_id=country_id).order_by('-updateDate')
    return [tour for tour in tours[:limit * 5] if good_slug(tour.Slug)][:limit]
