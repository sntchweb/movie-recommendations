class ImageDeleteMixin:
    image_fields = None

    def get_image_field(self):
        assert self.image_fields is not None, (
            'Error, need include "image_field" attribute'
        )
        assert isinstance(self.image_fields, (tuple, list)), (
            'Error, "image_field" must be list or tuple type'
        )
        for image_field in self.image_fields:
            exist = hasattr(self.__class__, image_field)
            if not exist:
                raise AttributeError(
                    f'"{self.__class__.__name__}" no has "{image_field}" field'
                )
        return self.image_fields

    def remove_image_on_update(self):
        try:
            obj = self.__class__.objects.get(id=self.id)
        except self.__class__.DoesNotExist:
            return

        for image_field in self.get_image_field():
            cur_image = getattr(obj, image_field)
            new_image = getattr(self, image_field)
            if cur_image and cur_image != new_image:
                cur_image.delete(save=False)
