# standard
import json
import hashlib


def cache_key_generator(
    report_name: str, data: dict, dpi: int, output_format: str
) -> str:
    s = report_name + json.dumps(data) + str(dpi) + output_format
    s = s.encode("utf8")
    return hashlib.md5(s).hexdigest()
