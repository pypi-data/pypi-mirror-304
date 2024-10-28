# Django
from django.db.models import F
from django.dispatch import receiver

# Local application / specific library imports
from .signals import ad_clicked, ad_printed


@receiver(ad_clicked)
def ad_clicked(sender, ad, request, **kwargs):
    ad.clicks_count = F("clicks_count") + 1
    ad.save()


@receiver(ad_printed)
def ad_printed(sender, ad, request, **kwargs):
    ad.prints_count = F("prints_count") + 1
    ad.save()
