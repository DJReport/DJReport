# dj
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

# internal
from .mixins import ReportDataSourceMixin


class DataSource(models.Model):
    """Date Source"""

    name = models.CharField(max_length=150, unique=True)
    dotted_path = models.CharField(
        max_length=255, help_text="E.g. apps.accounting.data_sources.Invoice"
    )

    class Meta:
        abstract = "djreport" not in settings.INSTALLED_APPS

    @cached_property
    def instance(self) -> ReportDataSourceMixin:
        data_source_class = import_string(self.dotted_path)
        return data_source_class()

    def get_data(self, **kwargs) -> dict:
        return self.instance.get_data(**kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"DataSource(id={self.id}, name={self.name})"
