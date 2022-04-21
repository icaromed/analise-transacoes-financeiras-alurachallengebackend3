from django.template.defaulttags import register


@register.filter
def get_url(data):
    format_data = "".join(data.split("/"))
    return f"{format_data}/detalhar"

