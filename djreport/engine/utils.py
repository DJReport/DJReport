# internal
from .consts import EXTENSIONS

# dj
from django.core.exceptions import ImproperlyConfigured


def get_extension(output_format: str) -> str:
    try:
        return f".{EXTENSIONS[output_format]}"
    except KeyError:
        raise ImproperlyConfigured(f"Invalid format: {output_format}")
