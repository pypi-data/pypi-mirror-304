from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def plausible(site_domains=None, script_url=None, async_tag=None):
    if site_domains is None:
        site_domains = getattr(settings, "PLAUSIBLE_SITES", None)
    if script_url is None:
        script_url = getattr(settings, "PLAUSIBLE_SCRIPT_URL", None)

    if not site_domains or not script_url:
        return ""

    if getattr(settings, "PLAUSIBLE_SCRIPT_ASYNC_TAG", False):
        defer_or_async = "async" if async_tag is not False else "defer"
    else:
        defer_or_async = "defer" if not async_tag else "async"

    attrs = {
        "data-domain": site_domains,
        "src": script_url,
    }

    return mark_safe("<script {}{}></script>".format(defer_or_async, flatatt(attrs)))
