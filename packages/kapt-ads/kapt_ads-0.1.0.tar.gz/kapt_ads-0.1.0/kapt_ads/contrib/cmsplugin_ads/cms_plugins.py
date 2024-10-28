# Django
from django.utils.translation import gettext_lazy as _

# Third party
from cms.constants import EXPIRE_NOW
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

# Local application / specific library imports
from .conf import settings
from .models import AdsPluginConf

# Project
from kapt_ads import signals


class AdsPlugin(CMSPluginBase):
    model = AdsPluginConf
    name = _("Ads")
    render_template = True
    cache = False

    def render(self, context, instance, placeholder):
        context["conf"] = instance

        self.render_template = "cmsplugin_ads/{}".format(instance.template)

        # Send an 'ad_printed' signal for each ad that will be printed
        for ad in instance.ads:
            signals.ad_printed.send(
                sender="display_ads-templatetag",
                ad=ad,
                request=context["request"],
            )

        context["ads"] = instance.ads
        return context

    def get_cache_expiration(self, request, instance, placeholder):
        if len(instance.ads) > 0:
            return EXPIRE_NOW
        return settings.CACHE_DURATION


plugin_pool.register_plugin(AdsPlugin)
