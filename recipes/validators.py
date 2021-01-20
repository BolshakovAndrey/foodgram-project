from django.core.exceptions import ValidationError


def image_size_validator(image):
    """
    Validate the maximum size for the image uploaded to the site.
    :param image:
    :return:
    """
    file_size = image.file.size
    limit_mb = 4
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)
