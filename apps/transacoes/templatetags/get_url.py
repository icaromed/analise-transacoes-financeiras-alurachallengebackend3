from django.template.defaulttags import register


@register.filter
def get_url(data):
    format_data = "".join(data.split("/"))
    return format_data

