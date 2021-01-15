from django import template
# All template tags and filters are registered in template.Library
# add our filter to them as well
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
