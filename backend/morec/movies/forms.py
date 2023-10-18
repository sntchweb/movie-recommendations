from io import BytesIO

from defusedxml import ElementTree
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (FileExtensionValidator,
                                    get_available_image_extensions)
from PIL import Image

from movies.models import Genre


def validate_image_and_svg_file_extension(value):
    allowed_extensions = get_available_image_extensions() + ['svg']
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


class SvgImageFormField(forms.ImageField):
    default_validators = [validate_image_and_svg_file_extension]

    def to_python(self, data):
        load_file = super(forms.ImageField, self).to_python(data)
        if load_file is None:
            return None

        if hasattr(data, 'temporary_file_path'):
            ifile = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                ifile = BytesIO(data.read())
            else:
                ifile = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(ifile)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            load_file.image = image
            load_file.content_type = Image.MIME[image.format]
        except Exception as exc:
            # add a workaround to handle svg images
            if not self.is_svg(ifile):
                raise ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                ) from exc
        if hasattr(load_file, 'seek') and callable(load_file.seek):
            load_file.seek(0)
        return load_file

    def is_svg(self, f):
        """
        Check if provided file is svg
        """

        # When is the temporary_file_path
        f_is_path = isinstance(f, str)

        if f_is_path:
            fio = open(f, 'rb')
        else:
            fio = f

        fio.seek(0)

        tag = None
        try:
            for event, el in ElementTree.iterparse(fio, ('start',)):
                tag = el.tag
                break
        except ElementTree.ParseError:
            pass

        if f_is_path:
            fio.close()

        return tag == '{http://www.w3.org/2000/svg}svg'


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        exclude = []
        field_classes = {
            'picture': SvgImageFormField,
        }
