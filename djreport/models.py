# standard
from typing import Any

# dj
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

# internal
from .engine import Engine, ENGINE_CHOICES
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


class Report(models.Model):
    """Report Model"""

    active = models.BooleanField(default=True)
    _engine = models.CharField(
        verbose_name="Engine", max_length=50, choices=ENGINE_CHOICES
    )
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to="reports/")
    data_source = models.ForeignKey(
        "DataSource",
        null=True,
        blank=True,
        related_name="reports",
        on_delete=models.SET_NULL,
    )
    default_data = models.JSONField(default=dict, null=True, blank=True)
    cache_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = "djreport" not in settings.INSTALLED_APPS

    @cached_property
    def engine(self) -> Engine:
        return Engine(self._engine)

    def render(self, dpi: int, output_format: str, **kwargs: Any) -> bytes:
        # default data
        data = self.default_data if self.default_data else {}
        # get data from data source if any
        if self.data_source:
            data.update(self.data_source.get_data(**kwargs))
        # render
        return self.engine.render(self.file.path, data, dpi, output_format)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Report(id={self.id}, name={self.name})"
