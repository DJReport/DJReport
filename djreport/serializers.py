# drf
from rest_framework import serializers

# internal
from .engine import FORMATS, MIN_DPI, MAX_DPI


class RenderSerializer(serializers.Serializer):  # noqa
    """Render Serializer"""

    dpi = serializers.IntegerField(
        min_value=MIN_DPI, max_value=MAX_DPI, default=MIN_DPI
    )
    output_format = serializers.ChoiceField(choices=FORMATS)

    def validate_output_format(self, value):
        # get report instance from context
        report = self.context.get("report")
        # check that given report instance.engine support given output format
        if report:
            # validate given output format
            pass
        return value
