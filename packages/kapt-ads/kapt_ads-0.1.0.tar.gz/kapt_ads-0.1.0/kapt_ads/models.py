# Standard Library
import math
import os
import uuid

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Local application / specific library imports
from .conf import settings as local_settings
from .fields import QuillField
from .managers import AdManager


def get_ad_filename(instance, filename):
    extension = os.path.splitext(filename)[1]

    filename = "/".join(
        [
            local_settings.ADS_MEDIA_DIRECTORY,
            "{uuid}{ext}".format(uuid=str(uuid.uuid4()), ext=extension),
        ]
    )
    return filename


class Advertiser(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)

    class Meta:
        verbose_name = _("Advertiser")
        verbose_name_plural = _("Advertisers")

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    identifier = models.SlugField(
        max_length=150, verbose_name=_("Identifier"), db_index=True, null=True
    )
    format = models.CharField(
        max_length=150,
        verbose_name=_("Format"),
        choices=local_settings.LOCATION_FORMAT_CHOICES,
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        constraints = [models.UniqueConstraint("identifier", name="unique_identifier")]

    def __str__(self):
        return _("{name} (format: {format})").format(
            name=self.name, format=self.get_format_display()
        )


class Ad(models.Model):
    advertiser = models.ForeignKey(
        Advertiser,
        related_name="ads",
        verbose_name=_("Advertiser"),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=150,
        verbose_name=_("Name"),
        help_text=_("For admin use only. Will not appear on the ad."),
    )
    location = models.ForeignKey(
        Location, verbose_name=_("Location"), on_delete=models.SET_NULL, null=True
    )
    image = models.ImageField(verbose_name=_("Image"), upload_to=get_ad_filename)
    text = QuillField(verbose_name=_("Text"), null=True, blank=True)

    target_url = models.URLField(
        verbose_name=_("Target URL"),
        help_text=_("The URL that opens when the ad is clicked."),
        blank=True,
        null=True,
    )

    publication_date_start = models.DateField(
        verbose_name=_("Publication start date"), blank=True, null=True
    )
    publication_date_end = models.DateField(
        verbose_name=_("Publication end date"), blank=True, null=True
    )
    is_paused = models.BooleanField(verbose_name=_("Is paused"), default=False)

    clicks_limit = models.PositiveIntegerField(
        verbose_name=_("Clicks limit"), blank=True, null=True
    )
    clicks_count = models.PositiveIntegerField(
        verbose_name=_("Clicks count"), editable=False, blank=True, default=0
    )

    prints_limit = models.PositiveIntegerField(
        verbose_name=_("Prints limit"), blank=True, null=True
    )
    prints_count = models.PositiveIntegerField(
        verbose_name=_("Prints count"), editable=False, blank=True, default=0
    )

    objects = AdManager()

    class PublicationStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACTIVE = "active", _("Active")
        PAUSED = "paused", _("Paused")
        COMPLETED = "completed", _("Completed")

        @classmethod
        def explain(cls, status):
            if status == cls.PENDING:
                return _("The publication start date has not been reached yet")
            elif status == cls.ACTIVE:
                return _("This ad is online")
            elif status == cls.PAUSED:
                return _("This ad has been manually paused")
            elif status == cls.COMPLETED:
                return _(
                    "The publication end date, prints limit or clicks limit has been reached"
                )

    class Meta:
        verbose_name = _("Ad")
        verbose_name_plural = _("Ads")

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        # Validates dates: the start date must be lesser or equal than the end date.
        if (
            self.publication_date_start is not None
            and self.publication_date_end is not None
            and self.publication_date_start > self.publication_date_end
        ):
            raise ValidationError(
                {
                    "publication_date_start": _(
                        "The start date must be lesser or equal than the end date"
                    )
                }
            )

        if self.clicks_limit and self.prints_limit:
            raise ValidationError(
                {
                    "clicks_limit": _(
                        "Either a limit on the number of clicks or a limit on the number of prints should be specified, but not both."
                    ),
                    "prints_limit": _(
                        "Either a limit on the number of clicks or a limit on the number of prints should be specified, but not both."
                    ),
                }
            )

    @property
    def publication_status(self):
        prints_count = self.prints_count or 0
        prints_limit = self.prints_limit or math.inf
        clicks_count = self.clicks_count or 0
        clicks_limit = self.clicks_limit or math.inf
        today = now().date()

        if self.is_paused:
            return self.PublicationStatus.PAUSED
        elif self.publication_date_start and self.publication_date_start > today:
            return self.PublicationStatus.PENDING
        elif (
            self.publication_date_end
            and self.publication_date_end < today
            or prints_count >= prints_limit
            or clicks_count >= clicks_limit
        ):
            return self.PublicationStatus.COMPLETED
        return self.PublicationStatus.ACTIVE

    def get_publication_status_badge(self):
        match self.publication_status:
            case self.PublicationStatus.PENDING:
                return "🕙"
            case self.PublicationStatus.ACTIVE:
                return "🟢"
            case self.PublicationStatus.PAUSED:
                return "⏸️"
            case self.PublicationStatus.COMPLETED:
                return "⏹️"

    def get_publication_status_explanation(self):
        return self.PublicationStatus.explain(self.publication_status)
