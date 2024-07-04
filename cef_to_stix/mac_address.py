from stix2 import EqualityComparisonExpression, ObjectPath
from stix2.patterns import _PatternExpression, AndBooleanExpression
from .constants import NETWORK_TRAFFIC, SOURCE_REF, DESTINATION_REF, MAC_ADDR
from .abstract_cef_converter import AbstractCEFConverter


class MacAddressNoContextConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        # "[mac-addr:value = '00:0a:95:9d:68:16']"
        return EqualityComparisonExpression(ObjectPath(MAC_ADDR, ["value"]), self.cef_field_value)


class DestinationMacAddressConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        # [network-traffic:dst_ref.type = 'mac-addr' AND network-traffic:dst_ref.value = 'd2:fb:49:24:37:18']
        type_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "type"]), MAC_ADDR)
        value_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [DESTINATION_REF, "value"]),
                                                  self.cef_field_value)
        return AndBooleanExpression([type_expr, value_expr])


class SourceMacAddressConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        # [network-traffic:src_ref.type = 'mac-addr' AND network-traffic:src_ref.value = 'd2:fb:49:24:37:18']
        type_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "type"]), MAC_ADDR)
        value_expr = EqualityComparisonExpression(ObjectPath(NETWORK_TRAFFIC, [SOURCE_REF, "value"]),
                                                  self.cef_field_value)
        return AndBooleanExpression([type_expr, value_expr])
