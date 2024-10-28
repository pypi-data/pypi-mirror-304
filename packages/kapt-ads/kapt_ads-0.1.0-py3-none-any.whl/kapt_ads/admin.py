# Django
from django.contrib import admin
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext as _

# Local application / specific library imports
from .models import Ad, Advertiser, Location


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ("name", "get_ads_count")

    @admin.display(description=_("Ads count"))
    def get_ads_count(self, obj):
        return obj.ads.count()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "get_format_display")
    list_filter = ("format",)
    search_fields = ("name",)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "advertiser",
        "name",
        "publication_date_start",
        "publication_date_end",
        "get_prints_count",
        "get_clicks_count",
        "get_publication_status",
    )
    list_display_links = ("name",)
    list_filter = ("advertiser", "is_paused")
    search_fields = ("name", "advertiser")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "advertiser",
                    "name",
                    "location",
                    "image",
                    "text",
                    "target_url",
                ],
            },
        ),
        (
            _("Scheduling"),
            {
                "fields": [
                    "is_paused",
                    ("publication_date_start", "publication_date_end"),
                ]
            },
        ),
        (
            _("Limits"),
            {
                "fields": [
                    ("prints_limit", "clicks_limit"),
                ]
            },
        ),
    ]

    @admin.display(description=_("Prints count"))
    def get_prints_count(self, obj):
        if obj.prints_limit:
            return f"{obj.prints_count} / {obj.prints_limit}"
        return obj.prints_count

    @admin.display(description=_("Clicks count"))
    def get_clicks_count(self, obj):
        if not obj.target_url:
            title = _("This ad is not clickable because it does not have a target URL.")
            return mark_safe('<span title="{}">-</span>'.format(title))
        elif obj.clicks_limit:
            return f"{obj.clicks_count} / {obj.clicks_limit}"
        return obj.clicks_count

    @admin.display(description=_("Is active"))
    def get_publication_status(self, obj):
        badge = obj.get_publication_status_badge()
        title = obj.get_publication_status_explanation()
        if (
            obj.publication_date_start
            and obj.publication_status == obj.PublicationStatus.ACTIVE
        ):
            since = defaultfilters.timesince(obj.publication_date_start, now().date())
            title += _(" (for {})").format(since)
        return mark_safe(f'<span title="{title}">{badge}</span>')
