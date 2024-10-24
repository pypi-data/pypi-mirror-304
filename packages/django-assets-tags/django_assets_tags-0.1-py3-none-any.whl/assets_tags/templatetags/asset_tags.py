from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def public_assets(path: str = ""):
    base_url = getattr(settings, 'PUBLIC_ASSETS_URL', '')
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

@register.simple_tag
def private_assets(path: str = ""):
    base_url = getattr(settings, 'PRIVATE_ASSETS_URL', '')
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"
