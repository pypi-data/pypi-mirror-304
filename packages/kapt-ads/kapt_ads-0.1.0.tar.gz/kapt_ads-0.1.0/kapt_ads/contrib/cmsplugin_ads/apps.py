# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CMSPluginAdsConfig(AppConfig):
    label = "cmsplugin_ads"
    name = "kapt_ads.contrib.cmsplugin_ads"
    verbose_name = _("CMSPlugin Ads")

    def ready(self):
        # Local application / specific library imports
        from . import receivers  # noqa
