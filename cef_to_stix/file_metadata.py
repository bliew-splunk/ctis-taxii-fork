from stix2 import EqualityComparisonExpression, ObjectPath, StringConstant
from stix2.patterns import _PatternExpression

from .abstract_cef_converter import AbstractCEFConverter


# Example pattern: [file:name = 'foo.dll' AND file:parent_directory_ref.path = 'C:\\Windows\\System32']
class FileNameConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("file", ["name"]), self.cef_field_value)


class FilePathConverter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        # Setting from_parse_tree=True fixes issue with double escaping backslashes
        rhs = StringConstant(self.cef_field_value, from_parse_tree=True)
        return EqualityComparisonExpression(ObjectPath("file", ["parent_directory_ref", "path"]),
                                            rhs)
