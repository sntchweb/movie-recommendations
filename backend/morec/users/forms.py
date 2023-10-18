from django import forms

from users.models import Avatar
from movies.forms import SvgImageFormField


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = []
        field_classes = {
            'avatar': SvgImageFormField,
        }
