# dj
from django.core.cache import cache
from django.http import HttpResponse

# drf
from rest_framework import status
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# internal
from .models import Report
from .conf import djreport_conf
from .engine import get_extension
from .serializers import RenderSerializer


class RenderView(GenericAPIView):
    """Render View"""

    serializer_class = RenderSerializer
    queryset = Report.objects.filter(active=True)
    renderer_classes = [renderers.JSONRenderer]

    @staticmethod
    def render_report(
        report: Report, data: dict, dpi: int, output_format: str
    ) -> bytes:
        # check for report.cache_required
        if not report.cache_required:
            return report.render(dpi, output_format, data)
        # generate cache-key base on report.name, data, dpi and output_format
        key = djreport_conf.cache_key_generator(report.name, data, dpi, output_format)
        # get value by generated-key from cache registry
        value = cache.get(key)
        # if value does not exist:
        # 1) generate value by rendering report
        # 2) set value into cache registry for next time uses
        # 3) return value as result
        if not value:
            value = report.render(dpi, output_format, data)
            cache.set(key, value, djreport_conf.cache_timeout)

        return value

    @staticmethod
    def download_response(
        report_name: str, rendered_bytes: bytes, output_format: str
    ) -> HttpResponse:
        # create generic mime type file-response
        response = HttpResponse(rendered_bytes, content_type="application/octet-stream")
        # create file name base on given report_name and output_format
        filename = report_name + get_extension(output_format)
        # add filename to response headers as [filename_header_key] for local uses
        response[djreport_conf.filename_header_key] = filename
        # set Content-Disposition as attachment
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def get(self, request, pk):  # noqa
        # get report
        report = self.get_object()
        # serialize and validate render parameters
        serializer = self.get_serializer(
            data=request.query_params, context={"report": report}
        )
        if serializer.is_valid():
            # extract dpi and output_format
            dpi = serializer.validated_data["dpi"]
            output_format = serializer.validated_data["output_format"]
            # get data from report.data_source
            data = report.data_source.get_data(**request.query_params)
            rendered_report = self.render_report(report, data, dpi, output_format)
            return self.download_response(report.name, rendered_report, output_format)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
