from stix2 import EqualityComparisonExpression, ObjectPath
from stix2.patterns import _PatternExpression

from .abstract_cef_converter import AbstractCEFConverter


class URLConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("url", ["value"]), self.cef_field_value)
