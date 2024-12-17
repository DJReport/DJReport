# dj
from django.contrib import admin

# internal
from .models import DataSource, Report


class DataSourceListFilter(admin.SimpleListFilter):
    """DataSource List Filter"""

    title = "data source"

    parameter_name = "data_source"

    def lookups(self, request, model_admin):
        return [(ds.id, ds.name) for ds in DataSource.objects.all()]

    def queryset(self, request, queryset):
        if value := self.value():
            queryset = queryset.filter(id=value)
        return queryset


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """DataSource Admin"""

    list_display = ["id", "name", "dotted_path"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report Admin"""

    list_display = ["id", "name", "data_source", "active"]
    list_filter = ["active", DataSourceListFilter]
