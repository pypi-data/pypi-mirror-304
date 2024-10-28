# Django
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

# Third party
from cms.models import CMSPlugin

# Local application / specific library imports
from ...models import Location
from ...templatetags.ads_tags import retrieve_ads
from .conf import settings as local_settings


class AdsPluginConf(CMSPlugin):
    number_of_ads = models.IntegerField(
        verbose_name=_("Number of ads to print"), null=True, blank=True
    )

    template = models.CharField(
        verbose_name=_("Template"),
        choices=local_settings.TEMPLATES,
        default=local_settings.TEMPLATES[0][0],
        max_length=150,
    )

    location = models.ForeignKey(
        Location, verbose_name=_("Location"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Ads configuration")
        verbose_name_plural = _("Ads configurations")

    def __str__(self):
        return _("Ads location {}").format(self.location)

    @cached_property
    def ads(self):
        return retrieve_ads(self.location.identifier, self.number_of_ads)
