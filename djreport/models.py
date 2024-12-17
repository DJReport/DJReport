# standard
from typing import Any

# dj
from django.db import models
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

# internal
from .conf import djreport_conf
from .mixins import ReportDataSourceMixin
from .engine import Engine, ENGINE_CHOICES


class DataSource(models.Model):
    """Date Source"""

    name = models.CharField(max_length=150, unique=True)
    dotted_path = models.CharField(
        max_length=255, help_text="E.g. apps.accounting.data_sources.Invoice"
    )

    class Meta:
        abstract = not djreport_conf.installed

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
        related_name="reports",
        on_delete=models.CASCADE,
    )
    cache_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = not djreport_conf.installed

    @cached_property
    def engine(self) -> Engine:
        return Engine(self._engine)

    def render(
        self, dpi: int, output_format: str, data: dict = None, **kwargs: Any
    ) -> bytes:
        # get data
        if data is None:
            data = self.data_source.get_data(**kwargs)
        # render
        return self.engine.render(self.file.path, data, dpi, output_format)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Report(id={self.id}, name={self.name})"
