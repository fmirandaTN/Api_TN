from django.db.models.query import QuerySet
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import ISO_8601
from rest_framework.settings import api_settings
from rest_framework.fields import DateTimeField


class FlexFieldsModelSerializer(FlexFieldsModelSerializer):
    deleted = 'False'

    def __init__(self, *args, **kwargs):
        foreign_fields = kwargs.pop('include', [])
        foreign_fields_include_writable_fields = kwargs.pop(
            'include_writable_fields', False)

        super_return = super().__init__(*args, **kwargs)

        foreign_fields += self._parse_request_list_value(
            'include')

        # Drop any fields that are not specified in the `include`, `expand` argument or required for POST/PATCH.
        show_fields = set(foreign_fields)
        show_fields = show_fields | set(self.expanded_fields)
        if ("request" in self.context and self.context["request"].method in ["POST", "PATCH", "PUT"]) or foreign_fields_include_writable_fields:
            show_fields = show_fields | set(
                [field.field_name for field in self._writable_fields])
        hide_fields = set(
            self.Meta.hidden_fields if hasattr(self.Meta, 'hidden_fields') else [])
        for field_name in hide_fields - show_fields:
            self.fields.pop(field_name)

        return super_return

    def to_representation(self, instance):
        """ We use this method to display datetimes without milliseconds. """
        request = self.context.get("request")
        if request:
            deleted = request.query_params.get('deleted', None)
            if deleted == 'True' or deleted == '*' or deleted == '~all':
                self.deleted = deleted

        if self.deleted == 'False' and instance.deleted:
            return None

        ret = super().to_representation(instance)
        fields = self._readable_fields

        for field in fields:
            attribute = field.get_attribute(instance)
            if isinstance(field, DateTimeField):
                """
                This is how DRF handles the representation:
                https://github.com/encode/django-rest-framework/blob/master/rest_framework/fields.py#L1195
                """
                attribute = field.enforce_timezone(attribute)
                output_format = getattr(
                    self, 'format', api_settings.DATETIME_FORMAT)
                if output_format.lower() == ISO_8601:
                    attribute = attribute.isoformat(timespec='milliseconds')
                    if attribute.endswith('+00:00'):
                        attribute = attribute[:-6] + 'Z'
                    ret[field.field_name] = attribute

            if isinstance(ret[field.field_name], list):
                ret[field.field_name] = [
                    x for x in ret[field.field_name] if x is not None]

        return ret

    def _get_expand_input(self, passed_settings, *args, **kwargs):
        """
            This method has been expanded so it now allows to use
            'expand' without limits in list endpoints.
        """

        super_return = super()._get_expand_input(
            passed_settings=passed_settings, *args, **kwargs)

        value = passed_settings.get("expand")

        if len(value) > 0:
            return value

        if not self._can_access_request:
            return []

        expand = self._parse_request_list_value("expand")

        if "permitted_expands" in self.context:
            permitted_expands = self.context["permitted_expands"]

            if "~all" in permitted_expands or "*" in permitted_expands:
                return expand

        return super_return
