# Django
from django.db import models
from django.db.models import F, Q
from django.utils.timezone import now

DEFAULT_ORDER_BY = "?"


class AdQuerySet(models.QuerySet):
    def with_status(self, status):
        # Local application / specific library imports
        from .models import Ad

        match status:
            case Ad.PublicationStatus.PENDING:
                return self.pending()
            case Ad.PublicationStatus.ACTIVE:
                return self.active()
            case Ad.PublicationStatus.PAUSED:
                return self.paused()
            case Ad.PublicationStatus.COMPLETED:
                return self.completed()
        return self.none()

    def pending(self):
        today = now().date()
        return self.filter(
            # Not paused
            Q(is_paused=False)
            # Publication date start is not defined but not reached
            & Q(publication_date_start__isnull=False)
            & Q(publication_date_start__gt=today)
        )

    def active(self):
        today = now().date()
        return self.filter(
            # Not paused
            Q(is_paused=False)
            # Publication date start is reached or not defined
            & (
                Q(publication_date_start__isnull=False)
                & Q(publication_date_start__lte=today)
                | Q(publication_date_start__isnull=True)
            )
            # Publication date end is not reached or not defined
            & (
                Q(publication_date_end__isnull=False)
                & Q(publication_date_end__gte=today)
                | Q(publication_date_end__isnull=True)
            )
            # Prints limit is not reached or not defined
            & (
                Q(prints_limit__isnull=False) & Q(prints_count__lt=F("prints_limit"))
                | Q(prints_limit__isnull=True)
            )
            # Clicks limit is not reached or not defined
            & (
                Q(clicks_limit__isnull=False) & Q(clicks_count__lt=F("clicks_limit"))
                | Q(clicks_limit__isnull=True)
            )
        )

    def paused(self):
        return self.filter(is_paused=True)

    def completed(self):
        today = now().date()
        return self.filter(
            # Not paused
            Q(is_paused=False)
            # Publication date end is defined and reached
            & (
                (
                    Q(publication_date_end__isnull=False)
                    & Q(publication_date_end__lt=today)
                )
                # Prints limit is defined and reached
                | (
                    Q(prints_limit__isnull=False)
                    & Q(prints_count__gte=F("prints_limit"))
                )
                # Clicks limit is defined and reached
                | (
                    Q(clicks_limit__isnull=False)
                    & Q(clicks_count__gte=F("clicks_limit"))
                )
            )
        )

    def for_location(self, location_identifier, order_by=DEFAULT_ORDER_BY):
        return self.filter(location__identifier=location_identifier).order_by(order_by)


class AdManager(models.Manager):
    def get_queryset(self):
        return AdQuerySet(self.model, using=self._db)

    def with_status(self, status):
        return self.get_queryset().with_status(status)

    def for_location(self, location_identifier, order_by=DEFAULT_ORDER_BY):
        return self.get_queryset().for_location(location_identifier, order_by)
