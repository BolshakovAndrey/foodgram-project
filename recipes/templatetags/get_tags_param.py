from django import template

register = template.Library()

@register.filter
def get_tags_param(request, tag):
    """
    Takes `request` object and add `tag` to the GET request query params
    """
    tags = request.GET.get("tag", "")
    tags = tags.split(',') if tags else []
    if tag not in tags:
        tags.append(tag)
    else:
        tags.remove(tag)
    return ','.join(tags)
