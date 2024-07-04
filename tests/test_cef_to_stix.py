import pytest

from cef_to_stix import build_indicator_stix, convert_cef_to_stix_observation_pattern


def compare_stix_pattern_to_string(stix_pattern, expected_string):
    assert str(stix_pattern) == expected_string


"""
Convert from Splunk SOAR CEF field name to STIX2 pattern
network-traffic spec: https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_rgnc3w40xy

Regarding `network-traffic.dst_ref and .src_ref`:
Specifies the destination of the network traffic, as a reference to a Cyber-observable Object.
The object referenced MUST be of type ipv4-addr, ipv6-addr, mac-addr, or domain-name (for cases where the IP address for a domain name is unknown).
"""


class TestIndividualCEFFieldToSTIXPattern:

    def test_ipv4(self):
        # the ip CEF field is assumed to be an IPv4 address?
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern("ip", "1.2.3.4"), "[ipv4-addr:value = '1.2.3.4']")

    def test_ipv6(self):
        raise NotImplementedError

    @pytest.mark.parametrize("cef_field", ("destinationAddress", "destinationTranslatedAddress"))
    def test_destination_ip_address(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, '203.0.113.33/32'),
            "[network-traffic:dst_ref.type = 'ipv4-addr' AND network-traffic:dst_ref.value = '203.0.113.33/32']")

    @pytest.mark.parametrize("cef_field", ("sourceAddress", "sourceTranslatedAddress"))
    def test_source_ip_address(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, '2.3.4.5'),
            "[network-traffic:src_ref.type = 'ipv4-addr' AND network-traffic:src_ref.value = '2.3.4.5']")

    @pytest.mark.parametrize("cef_field",
                             ["hostname", "host name", "dvchost", "deviceHostname", "domain", "deviceDnsDomain"])
    def test_hostname_with_no_context(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'example.com'),
            "[domain-name:value = 'example.com']")

    @pytest.mark.parametrize("cef_field", ("shost", "sourceHostName", "sourceDnsDomain", "sourceNtDomain", "sntdom"))
    def test_source_hostname(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'example.com'),
            "[network-traffic:src_ref.type = 'domain-name' AND network-traffic:src_ref.value = 'example.com']")

    @pytest.mark.parametrize("cef_field",
                             ("dhost", "destinationHostName", "destinationDnsDomain", "destinationNtDomain", "dntdom"))
    def test_destination_hostname(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'example.com'),
            "[network-traffic:dst_ref.type = 'domain-name' AND network-traffic:dst_ref.value = 'example.com']")

    @pytest.mark.parametrize("cef_field", ["mac address", "deviceMacAddress"])
    def test_mac_address_with_no_context(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'd2:fb:49:24:37:18'),
            "[mac-addr:value = 'd2:fb:49:24:37:18']")

    @pytest.mark.parametrize("cef_field", ["sourceMacAddress", "smac"])
    def test_source_mac_address(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'd2:fb:49:24:37:18'),
            "[network-traffic:src_ref.type = 'mac-addr' AND network-traffic:src_ref.value = 'd2:fb:49:24:37:18']")

    @pytest.mark.parametrize("cef_field", ["destinationMacAddress", "dmac"])
    def test_destination_mac_address(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'd2:fb:49:24:37:18'),
            "[network-traffic:dst_ref.type = 'mac-addr' AND network-traffic:dst_ref.value = 'd2:fb:49:24:37:18']")

    @pytest.mark.parametrize("cef_field", ("url", "requestURL"))
    def test_url(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'https://www.abc.com'),
            "[url:value = 'https://www.abc.com']")

    @pytest.mark.parametrize("cef_field", ("md5", "fileHashMd5"))
    def test_hash_md5(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, 'cead3f77f6cda6ec00f57d76c9a6879f'),
            "[file:hashes.MD5 = 'cead3f77f6cda6ec00f57d76c9a6879f']")

    @pytest.mark.parametrize("cef_field", ("sha1", "fileHashSha1"))
    def test_hash_sha1(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'),
            "[file:hashes.'SHA-1' = '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12']")

    @pytest.mark.parametrize("cef_field", ("sha256", "fileHashSha256"))
    def test_hash_sha256(self, cef_field):
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field,
                                                    'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f'),
            "[file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f']")

    @pytest.mark.parametrize("cef_field", ("sha512", "fileHashSha512"))
    def test_hash_sha512(self, cef_field):
        hash_digest = '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043'
        compare_stix_pattern_to_string(
            convert_cef_to_stix_observation_pattern(cef_field, hash_digest),
            f"[file:hashes.'SHA-512' = '{hash_digest}']")

    @pytest.mark.parametrize("cef_field", ["file name", "fileName"])
    def test_file_name(self, cef_field):
        compare_stix_pattern_to_string(convert_cef_to_stix_observation_pattern(cef_field, "abc.exe"),
                                       "[file:name = 'abc.exe']")

    @pytest.mark.parametrize("cef_field", ["file path", "filePath"])
    def test_file_path(self, cef_field):
        fp = "C:\\Windows\\System32"
        pattern = convert_cef_to_stix_observation_pattern(cef_field, fp)
        pattern_str = str(pattern)
        assert pattern_str == f"[file:parent_directory_ref.path = '{fp}']"


class TestMultipleCEFFieldToSTIXPattern:
    def test_destination_and_source_ipv4(self):
        pattern = convert_cef_to_stix_observation_pattern(["sourceAddress", "destinationAddress"],
                                                          "1.2.3.4")
        pattern_str = str(pattern)
        expected = ("[(network-traffic:src_ref.type = 'ipv4-addr' AND network-traffic:src_ref.value = '1.2.3.4')"
                    " OR (network-traffic:dst_ref.type = 'ipv4-addr' AND network-traffic:dst_ref.value = '1.2.3.4')]")
        assert pattern_str == expected

    def test_hostname_aliases(self):
        pattern = convert_cef_to_stix_observation_pattern(
            ["sourceHostName", "destinationHostName", "host name"],
            "example.com")
        pattern_str = str(pattern)
        expected_source_host_name_pattern = "network-traffic:src_ref.type = 'domain-name' AND network-traffic:src_ref.value = 'example.com'"
        expected_destination_host_name_pattern = "network-traffic:dst_ref.type = 'domain-name' AND network-traffic:dst_ref.value = 'example.com'"
        expected_hostname_pattern = "domain-name:value = 'example.com'"
        expected = f"[({expected_source_host_name_pattern}) OR ({expected_destination_host_name_pattern}) OR ({expected_hostname_pattern})]"
        assert pattern_str == expected


class TestBuildIndicatorSTIXJSON:

    def test_url_with_tlp_red(self):
        indicator_json = build_indicator_stix("url", "https://www.example.com", tlp_rating="RED")
        assert indicator_json["id"].startswith("indicator--")
        assert indicator_json["type"] == "indicator"
        assert indicator_json["pattern"] == "[url:value = 'https://www.example.com']"
        assert indicator_json["pattern_type"] == "stix"

        # Static TLP Marking Definition ID expected
        # See: https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_yd3ar14ekwrs
        assert indicator_json["object_marking_refs"] == ["marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed"]

    def test_ipv4(self):
        identity = "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff"
        indicator_json = build_indicator_stix("ip", "1.2.3.4", created_by_ref=identity, description="Malicious IP",
                                              lang="en", confidence=50)
        assert indicator_json["id"].startswith("indicator--")
        assert indicator_json["type"] == "indicator"
        assert indicator_json["pattern"] == "[ipv4-addr:value = '1.2.3.4']"
        assert indicator_json["pattern_type"] == "stix"
        assert indicator_json["created_by_ref"] == identity
        assert indicator_json["description"] == "Malicious IP"
        assert indicator_json["lang"] == "en"
        assert indicator_json["confidence"] == 50
        assert "object_marking_refs" not in indicator_json
