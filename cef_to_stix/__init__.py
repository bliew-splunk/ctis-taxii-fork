import json
from typing import List, Union, Type

from stix2 import Indicator, ObservationExpression, \
    OrBooleanExpression, ParentheticalExpression
from stix2.patterns import _PatternExpression

from cef_to_stix.hostname import SourceHostnameConverter, DestinationHostnameConverter, HostnameConverter
from cef_to_stix.ip_address import DestinationIPv4Converter, SourceIPv4Converter, IPv4Converter
from cef_to_stix.abstract_cef_converter import AbstractCEFConverter
from cef_to_stix.url import URLConverter

# See result from /rest/cef?page_size=1000
#
# For more context on CEF list of fields:
# https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.4/pdfdoc/cef-implementation-standard/cef-implementation-standard.pdf
# This does not cover all fields, but it's a good start. SOAR has slight variations
# Sentinel documentation on CEF field mapping is helpful:
# https://learn.microsoft.com/en-us/azure/sentinel/cef-name-mapping
"""
TODO: Implement most common CEF fields
- base data types:
    ip, port, mac address, url, domain, hash, sha1, sha256, sha512, md5, file name, file path, host name, user name
    process name
- SRC & DEST for IPv4:
    - IP
    - Hostname
    - Domain
- filename
- file hashes (MD5, SHA1, SHA256)
- URL
- Email

"""


def build_indicator_stix(cef_field_name_or_list: Union[str, List], cef_field_value: str) -> dict:
    pattern = convert_cef_to_stix_observation_pattern(cef_field_name_or_list, cef_field_value)

    # TODO: add more fields to the indicator
    # https://stix2.readthedocs.io/en/latest/api/stix2.v21.html#stix2.v21.Indicator
    indicator = Indicator(pattern=pattern,
                          pattern_type="stix")
    indicator_json = str(indicator)
    return json.loads(indicator_json)


def convert_multiple_cef_fields_to_stix_observation_pattern(cef_field_names: List[str],
                                                            cef_field_value: str) -> ObservationExpression:
    # each CEF field in cef_field_names share the same value given by cef_field_value.
    # For example (["sourceAddress", "destinationAddress"], "1.2.3.4")
    patterns = []
    for field_name in cef_field_names:
        pattern = get_stix_expression_for_cef_field(field_name, cef_field_value)
        pattern = ParentheticalExpression(pattern)
        patterns.append(pattern)
    expr = OrBooleanExpression(patterns)
    return ObservationExpression(expr)


def convert_cef_to_stix_observation_pattern(cef_field_name_or_list: Union[str, List],
                                            cef_field_value: str) -> ObservationExpression:
    if isinstance(cef_field_name_or_list, str):
        pattern = get_stix_expression_for_cef_field(cef_field_name_or_list, cef_field_value)
        return ObservationExpression(pattern)
    else:
        return convert_multiple_cef_fields_to_stix_observation_pattern(cef_field_name_or_list, cef_field_value)


MAP_OF_CEF_FIELD_TO_STIX_CONVERTER = {
    "ip": IPv4Converter,
    "destinationAddress": DestinationIPv4Converter,
    "destinationTranslatedAddress": DestinationIPv4Converter,
    "sourceAddress": SourceIPv4Converter,
    "sourceTranslatedAddress": SourceIPv4Converter,
    "hostname": HostnameConverter,
    "host name": HostnameConverter,
    "dvchost": HostnameConverter,
    "deviceHostname": HostnameConverter,
    "shost": SourceHostnameConverter,
    "sourceHostName": SourceHostnameConverter,
    "dhost": DestinationHostnameConverter,
    "destinationHostName": DestinationHostnameConverter,
    "url": URLConverter,
    "requestURL": URLConverter
}


def get_stix_expression_for_cef_field(cef_field_name: str, cef_field_value: str) -> _PatternExpression:
    conversion_class: Type[AbstractCEFConverter] = MAP_OF_CEF_FIELD_TO_STIX_CONVERTER.get(cef_field_name)
    if conversion_class is None:
        raise NotImplementedError(f"CEF field {cef_field_name} conversion not implemented yet.")
    else:
        return conversion_class(cef_field_value=cef_field_value).convert_to_stix_pattern()
