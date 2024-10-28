# Standard Library
from collections.abc import Mapping

# Django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Third party
from django_quill.widgets import QuillWidget as BaseQuillWidget

# Local application / specific library imports
from .conf import settings as local_settings


class QuillWidget(BaseQuillWidget):
    class Media:
        extend = False
        js = local_settings.QUILL_MEDIA_JS
        css = {"all": local_settings.QUILL_MEDIA_CSS}

    def __init__(self, config_name="default", *args, **kwargs):
        super(BaseQuillWidget, self).__init__(
            *args, **kwargs
        )  # Bypass BaseQuillWidget.__init__
        self.config = local_settings.DEFAULT_QUILL_CONFIG.copy()
        configs = getattr(settings, "KAPT_ADS_QUILL_CONFIGS", None)
        if configs:
            if isinstance(configs, Mapping):
                if config_name in configs:
                    config = configs[config_name]
                    if not isinstance(config, Mapping):
                        raise ImproperlyConfigured(
                            'QUILL_CONFIGS["%s"] setting must be a Mapping object'
                            % config_name
                        )
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured(
                        'No configuration named "%s" found in your QUILL_CONFIGS'
                        % config_name
                    )
            else:
                raise ImproperlyConfigured(
                    "QUILL_CONFIGS settings must be a Mapping object"
                )
