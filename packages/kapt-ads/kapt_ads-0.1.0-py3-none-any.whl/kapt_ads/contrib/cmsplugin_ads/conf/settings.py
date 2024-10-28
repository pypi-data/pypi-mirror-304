# Django
from django.conf import settings
from django.utils.translation import gettext as _

# Cache the results for 1h by default.
# CAUTION: Don't set a value too high as it can prevent planned ads from being displayed
CACHE_DURATION = getattr(settings, "KAPT_CMSPLUGIN_ADS_CACHE_DURATION", 3600)

DEFAULT_TEMPLATES = (("ads.html", _("Default")),)
TEMPLATES = getattr(settings, "KAPT_CMSPLUGIN_ADS_TEMPLATES", DEFAULT_TEMPLATES)
