# Standard Library
import logging

# Django
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_save

# Local application / specific library imports
from ...models import Ad, Location

logger = logging.getLogger("django")

try:
    # Third party
    from cms.cache import invalidate_cms_page_cache
    from cms.cache.placeholder import clear_placeholder_cache
    from cms.models.pluginmodel import Placeholder

    invalidate_newplugin_cache = True
except ImportError:
    logger.warning(
        "Could not import cache invalidation functions in cmsplugin_ads receivers"
    )
    invalidate_newplugin_cache = False


def invalidate_djangocms_cache(sender, **kwargs):
    if invalidate_newplugin_cache:
        # Get and clear placeholders cache
        placeholders = Placeholder.objects.filter(cmsplugin__plugin_type="AdsPlugin")
        current_site = Site.objects.get_current()
        for placeholder in placeholders:
            for language_code, dummy in settings.LANGUAGES:
                clear_placeholder_cache(placeholder, language_code, current_site.id)

        # Invalidate cms page cache
        invalidate_cms_page_cache()


post_save.connect(
    invalidate_djangocms_cache,
    sender=Location,
    dispatch_uid="invalidate_djangocms_cache_location",
)

post_save.connect(
    invalidate_djangocms_cache,
    sender=Ad,
    dispatch_uid="invalidate_djangocms_cache_ad",
)
