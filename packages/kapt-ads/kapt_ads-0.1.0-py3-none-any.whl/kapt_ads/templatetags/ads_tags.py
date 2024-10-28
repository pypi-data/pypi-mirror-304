# Django
from django import template
from django.template import loader

# Local application / specific library imports
from .. import signals
from ..models import Ad

register = template.Library()


def retrieve_ads(location_identifier, number):
    # Fetch the active ads for the given location
    ads = Ad.objects.with_status(Ad.PublicationStatus.ACTIVE).for_location(
        location_identifier
    )
    if number is not None:
        ads = ads[:number]
    return ads


@register.simple_tag(takes_context=True)
def display_ads(context, location, template_name="kapt_ads/ads.html", number=None):
    """
    This will display an ad for the given location.

    Usage:
    ```
    {% display_ad location='location-slug' %}
    ```

    A specific template can be used:
    ```
    {% display_ad location='location-slug' template_name='kapt_ads/ad2.html' %}
    ```

    The number of ads to print can also be specified:
    ```
    {% display_ad location='location-slug' number=2 %}
    ```
    """
    ads = retrieve_ads(location, number)

    # Send an 'ad_printed' signal for each ad that will be printed
    for ad in ads:
        signals.ad_printed.send(
            sender="display_ads-templatetag", ad=ad, request=context["request"]
        )

    # Render the ads
    t = loader.get_template(template_name)
    return t.render(
        {
            "ads": ads,
            "number": number,
        }
    )
