# Django
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

# Local application / specific library imports
from .models import Ad
from .signals import ad_clicked


class TargetRedirectView(RedirectView):
    view_signal = ad_clicked

    def get_redirect_url(self, **kwargs):
        ad = get_object_or_404(Ad, pk=self.kwargs["pk"])

        if ad.target_url is None:
            raise Http404

        # Send a signal indicating that the ad has been clicked
        self.view_signal.send(sender=self, ad=ad, request=self.request)

        return ad.target_url
