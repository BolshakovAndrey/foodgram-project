from django.core.exceptions import ValidationError


def image_size_validator(image):
    """
    Validate the maximum size for the image uploaded to the site.
    :param image:
    :return:
    """
    file_size = image.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError('Максимальный размер изображения не должен превышать  %s MB' % limit_mb)
