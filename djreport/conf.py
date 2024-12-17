# typing
from typing import Any

# dj
from django.conf import settings
from django.utils.module_loading import import_string


class DJReportConf(object):
    """DJReport Conf"""

    @staticmethod
    def _get_settings(key: str, default: Any = None) -> Any:
        return getattr(settings, key, default)

    @property
    def installed(self) -> bool:
        return "djreport" in settings.INSTALLED_APPS

    @property
    def cache_key_generator(self) -> callable:
        dotted_path = self._get_settings(
            "DJREPORT_CACHE_KEY_GENERATOR", "djreport.utils.cache_key_generator"
        )
        return import_string(dotted_path)

    @property
    def filename_header_key(self) -> str:
        return self._get_settings("DJREPORT_FILENAME_HEADER_KEY", "X-FileName")

    @property
    def cache_timeout(self):
        return self._get_settings("DJREPORT_CACHE_TIMEOUT", 60 * 5)


djreport_conf = DJReportConf()
