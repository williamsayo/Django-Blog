from django import template

register = template.Library()

def class_name(value):
    return value.__class__.__name__

@register.simple_tag(takes_context=True)
def search_parameter(context, **kwargs):
    url = context['request'].GET.copy()

    for page, page_num in kwargs.items():
        
        url[page] = page_num

    for page in [page for page, page_num in url.items() if not page_num]:
        del url[page]

    return url.urlencode()
