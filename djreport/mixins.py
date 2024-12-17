# standard
from typing import Any


class ReportDataSourceMixin(object):
    """Report DataSource Mixin"""

    def get_data(self, **kwargs: Any) -> dict:
        raise NotImplementedError
