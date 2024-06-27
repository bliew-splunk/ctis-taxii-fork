from stix2 import AndBooleanExpression, EqualityComparisonExpression, ObjectPath
from stix2.patterns import _PatternExpression

from cef_to_stix.abstract_cef_converter import AbstractCEFConverter
from .constants import DESTINATION_REF, DOMAIN_NAME, NETWORK_TRAFFIC, SOURCE_REF


class HostnameConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath(DOMAIN_NAME, ["value"]), self.cef_field_value)


class SourceHostnameConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        type_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "type"]), DOMAIN_NAME)
        value_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "value"]),
                                                  self.cef_field_value)
        return AndBooleanExpression([type_expr, value_expr])


class DestinationHostnameConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        type_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "type"]), DOMAIN_NAME)
        value_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "value"]),
                                                  self.cef_field_value)
        return AndBooleanExpression([type_expr, value_expr])
