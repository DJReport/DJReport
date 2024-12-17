# standard
import os
import json
import tempfile
import subprocess

# dj
from django.utils.functional import cached_property
from django.core.exceptions import ImproperlyConfigured

# internal
from .consts import BINS
from .utils import get_extension


class Engine(object):
    """Report Engine"""

    def __init__(self, engine: str) -> None:
        self._engine = engine

    @cached_property
    def bin(self) -> str:
        # get key
        try:
            key = BINS[self._engine]
        except KeyError:
            raise ImproperlyConfigured(f"Invalid engine: '{self._engine}'.")
        # get path
        path = os.getenv(key)
        if path is None:
            raise ImproperlyConfigured(f"'{key}' is not set.")
        # check for path
        if not os.path.exists(path):
            raise ImproperlyConfigured(f"'{path}' does not exist.")
        return path

    def render(
        self, report_path: str, data: dict, dpi: int, output_format: str
    ) -> bytes:
        # prepare data
        data = json.dumps(data, ensure_ascii=False)
        # get extension from given output_format
        extension = get_extension(output_format)
        # render
        with tempfile.NamedTemporaryFile(suffix=extension, delete=True) as f:
            subprocess.run(
                [self.bin, report_path, data, str(dpi), output_format, f.name],
                capture_output=True,
                text=True,
            )
            # rewind file
            f.seek(0)
            # read temp file content before delete
            content = f.read()
        # return content as result
        return content
