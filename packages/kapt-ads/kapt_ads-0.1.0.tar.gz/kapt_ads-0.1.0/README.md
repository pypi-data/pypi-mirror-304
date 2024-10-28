# Kapt ads

A minimal application for advertising management with Django.

![preview kapt_ads](https://gitlab.com/kapt/open-source/kapt-ads/-/raw/main/preview.png)

# Requirements

- Python 3.10+
- Django 4.2+

# Installation

- run `pip install kapt_ads`
- add the following apps to your `INSTALLED_APPS` (in the same order):
  ```py
  "kapt_ads",  # kapt-ads must appear before django_quill
  "django_quill"
  ```
- run `python manage.py migrate kapt_ads`
- include kapt-ads urls in your root url conf (avoid using "ads" in your path)
  ```py
  path("kaptiver/", include("kapt_ads.urls")),
  ```
## Settings

`KAPT_ADS_LOCATION_FORMAT_CHOICES`: choices of ads formats. Defaults to:
```
(
    ("square", _("Square")),
    ("horizontal_banner", _("Horizontal banner")),
    ("vertical_banner", _("Vertical banner")),
)
```

`KAPT_ADS_QUILL_CONFIGS`: a dictionary describing the config for the Quill text editor. See [documentation of django-quill](https://django-quill-editor.readthedocs.io/en/latest/).

`KAPT_ADS_MEDIA_DIRECTORY`: name of the directory in which images will be stored (default: `"kaptiver"`)

# Django CMSPlugin Ads

A plugin for Django CMS is provided in this package. To use it:
- add `kapt_ads.contrib.cmsplugin_ads` to your `INSTALLED_APPS`
- run `python manage.py migrate cmsplugin_ads`

## Settings

`KAPT_CMSPLUGIN_ADS_CACHE_DURATION`: number of seconds the ads should be cached (default: `3600`)

`KAPT_CMSPLUGIN_ADS_TEMPLATES`: choices of templates to display the ads (default: `(("ads.html", _("Default")),)`)
