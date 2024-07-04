import json
from typing import List, Union, Type

from stix2 import Indicator, ObservationExpression, \
    OrBooleanExpression, ParentheticalExpression
from stix2.patterns import _PatternExpression
from stix2 import TLP_WHITE, TLP_GREEN, TLP_AMBER, TLP_RED
from cef_to_stix.hostname import SourceHostnameConverter, DestinationHostnameConverter, HostnameConverter
from cef_to_stix.ip_address import DestinationIPv4Converter, SourceIPv4Converter, IPv4Converter
from cef_to_stix.abstract_cef_converter import AbstractCEFConverter
from cef_to_stix.url import URLConverter
from cef_to_stix.hashes import HashMD5Converter, HashSHA1Converter, HashSHA256Converter, HashSHA512Converter
from cef_to_stix.mac_address import MacAddressNoContextConverter, SourceMacAddressConverter, \
    DestinationMacAddressConverter
from cef_to_stix.file_metadata import FileNameConverter, FilePathConverter

# See result from /rest/cef?page_size=1000
#
# For more context on CEF list of fields:
# https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.4/pdfdoc/cef-implementation-standard/cef-implementation-standard.pdf
# This does not cover all fields, but it's a good start. SOAR has slight variations
# Sentinel documentation on CEF field mapping is helpful:
# https://learn.microsoft.com/en-us/azure/sentinel/cef-name-mapping
"""
TODO: Implement most common CEF fields
- base SOAR CEF data types:
    "domain"
    "file name"
    "file path"
    "hash"
    "host name"
    "ip"
    "mac address"
    "md5"
    "port"
    "process name"
    "sha1"
    "sha256"
    "sha512"
    "url"
    "user name"
    "vault id"
"""
TLP_RATING_TO_MARKING_DEFINITION = {
    "WHITE": TLP_WHITE,
    "GREEN": TLP_GREEN,
    "AMBER": TLP_AMBER,
    "RED": TLP_RED
}
TLP_RATINGS = list(TLP_RATING_TO_MARKING_DEFINITION.keys())


def build_indicator_stix(cef_field_name_or_list: Union[str, List], cef_field_value: str,
                         tlp_rating: str = None,
                         **kwargs) -> dict:
    pattern = convert_cef_to_stix_observation_pattern(cef_field_name_or_list, cef_field_value)

    if tlp_rating is not None and tlp_rating not in TLP_RATING_TO_MARKING_DEFINITION:
        raise ValueError(f"Invalid TLP rating: {tlp_rating}. Must be one of {TLP_RATINGS}")

    indicator_kwargs = kwargs
    if tlp_rating is not None:
        indicator_kwargs["object_marking_refs"] = TLP_RATING_TO_MARKING_DEFINITION[tlp_rating]

    indicator = Indicator(pattern=pattern,
                          pattern_type="stix",
                          **indicator_kwargs)
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


MULTIKEY_MAP_OF_CEF_FIELD_TO_STIX_CONVERTER = {
    "ip": IPv4Converter,
    ("destinationAddress", "destinationTranslatedAddress"): DestinationIPv4Converter,
    ("sourceAddress", "sourceTranslatedAddress"): SourceIPv4Converter,
    ("hostname", "host name", "dvchost", "deviceHostname", "deviceDnsDomain", "domain"): HostnameConverter,
    ("shost", "sourceHostName", "sourceDnsDomain", "sourceNtDomain", "sntdom"): SourceHostnameConverter,
    ("dhost", "destinationHostName", "destinationDnsDomain", "destinationNtDomain",
     "dntdom"): DestinationHostnameConverter,
    ("mac address", "deviceMacAddress"): MacAddressNoContextConverter,
    ("smac", "sourceMacAddress"): SourceMacAddressConverter,
    ("dmac", "destinationMacAddress"): DestinationMacAddressConverter,
    ("url", "requestURL"): URLConverter,
    ("md5", "fileHashMd5"): HashMD5Converter,
    ("sha1", "fileHashSha1"): HashSHA1Converter,
    ("sha256", "fileHashSha256"): HashSHA256Converter,
    ("sha512", "fileHashSha512"): HashSHA512Converter,
    ("file name", "fileName"): FileNameConverter,
    ("file path", "filePath"): FilePathConverter,
}
MAP_OF_CEF_FIELD_TO_STIX_CONVERTER = {}
for key, value in MULTIKEY_MAP_OF_CEF_FIELD_TO_STIX_CONVERTER.items():
    if type(key) == str:
        MAP_OF_CEF_FIELD_TO_STIX_CONVERTER[key] = value
    else:
        for k in key:
            MAP_OF_CEF_FIELD_TO_STIX_CONVERTER[k] = value


def get_stix_expression_for_cef_field(cef_field_name: str, cef_field_value: str) -> _PatternExpression:
    conversion_class: Type[AbstractCEFConverter] = MAP_OF_CEF_FIELD_TO_STIX_CONVERTER.get(cef_field_name)
    if conversion_class is None:
        raise NotImplementedError(f"CEF field {cef_field_name} conversion not implemented yet.")
    else:
        return conversion_class(cef_field_value=cef_field_value).convert_to_stix_pattern()
