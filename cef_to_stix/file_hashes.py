from stix2 import EqualityComparisonExpression, ObjectPath
from stix2.patterns import _PatternExpression
from stix2 import HashConstant

from .abstract_cef_converter import AbstractCEFConverter


class HashMD5Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("file", ["hashes", "MD5"]),
                                            HashConstant(self.cef_field_value, "MD5"))


class HashSHA1Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("file", ["hashes", "SHA-1"]),
                                            HashConstant(self.cef_field_value, "SHA1"))


class HashSHA256Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("file", ["hashes", "SHA-256"]),
                                            HashConstant(self.cef_field_value, "SHA256"))


class HashSHA512Converter(AbstractCEFConverter):
    def convert_to_stix_pattern(self) -> _PatternExpression:
        return EqualityComparisonExpression(ObjectPath("file", ["hashes", "SHA-512"]),
                                            HashConstant(self.cef_field_value, "SHA512"))
