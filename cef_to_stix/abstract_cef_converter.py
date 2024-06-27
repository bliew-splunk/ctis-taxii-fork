import abc

from stix2.patterns import _PatternExpression


class AbstractCEFConverter(abc.ABC):
    def __init__(self, cef_field_value):
        self.cef_field_value = cef_field_value

    @abc.abstractmethod
    def convert_to_stix_pattern(self) -> _PatternExpression:
        pass
