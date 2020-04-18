from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from bs4 import BeautifulSoup


register = template.Library()


@register.simple_tag
def extract_elements(source, element_type, src_prefix="", *args, **kwargs):
    print(['extract_elements', element_type])

    absolute_path = finders.find(source)

    with open(absolute_path) as fp:
        soup = BeautifulSoup(fp, "html5lib")

    if element_type == 'stylesheet':
        tags = soup.find_all(rel='stylesheet')
    if element_type == 'script':
        tags = soup.find_all('script')

    for tag in tags:
        source_attribute_name = None

        if tag.name == 'script':
            source_attribute_name = 'src'
        if tag.name == 'link':
            source_attribute_name = 'href'

        if source_attribute_name not in tag.attrs:
            continue

        src = tag.attrs[source_attribute_name]
        src = "{}{}".format(src_prefix, src)
        src = static(src)
        tag.attrs[source_attribute_name] = src

    str_tags = [str(x) for x in tags]
    html = "".join(str_tags)

    return mark_safe(html)
