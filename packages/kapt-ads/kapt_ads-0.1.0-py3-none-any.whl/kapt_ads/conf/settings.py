# Django
from django.conf import settings
from django.utils.translation import gettext_lazy as _

DEFAULT_LOCATION_CHOICES = (
    ("square", _("Square")),
    ("horizontal_banner", _("Horizontal banner")),
    ("vertical_banner", _("Vertical banner")),
)

LOCATION_FORMAT_CHOICES = getattr(
    settings, "KAPT_ADS_LOCATION_FORMAT_CHOICES", DEFAULT_LOCATION_CHOICES
)

DEFAULT_QUILL_CONFIG = {
    "theme": "snow",
    "modules": {
        "syntax": False,
        "toolbar": [
            [
                {"header": [2, 3, False]},
                {"align": []},
                {"color": []},
                "bold",
                "italic",
                "underline",
                "strike",
            ],
            [{"list": "ordered"}, {"list": "bullet"}, {"list": "check"}],
            [{"script": "sub"}, {"script": "super"}],  # superscript/subscript
            ["clean"],
        ],
        # quill-resize
        "resize": {
            "showSize": True,
            "locale": {},
        },
    },
}

QUILL_MEDIA_JS = [
    # quill
    "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js",
    # quill-resize
    "https://cdn.jsdelivr.net/npm/@botom/quill-resize-module@2.0.0/dist/quill-resize-module.min.js",
    # custom
    "django_quill/django_quill.js",
]

QUILL_MEDIA_CSS = [
    "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css",
    # quill-resize
    "https://cdn.jsdelivr.net/npm/quill-resize-module@1.2.4/dist/resize.min.css",
    # custom
    "django_quill/django_quill.css",
]

ADS_MEDIA_DIRECTORY = getattr(settings, "KAPT_ADS_MEDIA_DIRECTORY", "kaptiver")
