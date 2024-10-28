# Third party
from django_quill.fields import QuillField as BaseQuillField

# Local application / specific library imports
from .forms import QuillFormField


class QuillField(BaseQuillField):
    def formfield(self, **kwargs):
        kwargs.update({"form_class": self._get_form_class()})
        return super(BaseQuillField, self).formfield(
            **kwargs
        )  # Bypass BaseQuillField formfield method

    @staticmethod
    def _get_form_class():
        return QuillFormField
