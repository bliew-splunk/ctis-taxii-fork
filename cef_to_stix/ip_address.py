from stix2 import AndBooleanExpression, EqualityComparisonExpression, ObjectPath
from stix2.patterns import _PatternExpression

from .abstract_cef_converter import AbstractCEFConverter
from .constants import DESTINATION_REF, NETWORK_TRAFFIC, SOURCE_REF, STIX_TYPE_IPV4


class IPv4Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath(STIX_TYPE_IPV4, ["value"]), self.cef_field_value)


class SourceIPv4Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        src_ref_type = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "type"]), STIX_TYPE_IPV4)
        src_ref_value = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "value"]),
                                                     self.cef_field_value)
        return AndBooleanExpression([src_ref_type, src_ref_value])


class DestinationIPv4Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        dst_ref_type = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "type"]),
                                                    STIX_TYPE_IPV4)
        dst_ref_value = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "value"]),
                                                     self.cef_field_value)
        return AndBooleanExpression([dst_ref_type, dst_ref_value])
