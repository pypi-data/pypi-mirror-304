# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KaptAdsAppConfig(AppConfig):
    name = "kapt_ads"
    verbose_name = _("Ads")

    def ready(self):
        # Local application / specific library imports
        from . import receivers  # noqa
