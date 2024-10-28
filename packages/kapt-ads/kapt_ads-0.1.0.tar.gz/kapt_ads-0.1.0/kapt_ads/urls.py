# Django
from django.urls import path

# Local application / specific library imports
from .views import TargetRedirectView

urlpatterns = [
    path("r/<int:pk>/", TargetRedirectView.as_view(), name="target-redirect"),
]
