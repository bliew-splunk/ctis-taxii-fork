from taxii_client import TAXIIClient


def test_create_bundle_envelope_without_bundle_id_arg():
    obj1 = {
        "type": "indicator",
        "spec_version": "2.1",
        "id": "indicator--994479a7-e19b-4962-b66b-e1ff29f2442b",
        "created": "2024-06-24T12:34:56.000Z",
        "modified": "2024-06-24T12:34:56.000Z",
        "name": "Malicious IP Indicator",
        "pattern": "[ipv4-addr:value = '198.51.100.1']",
        "pattern_type": "stix",
        "valid_from": "2024-06-24T12:34:56.000Z",
    }
    objects = [obj1]
    bundle = TAXIIClient.create_bundle_envelope(objects)
    assert "id" in bundle
    assert bundle["id"].startswith("bundle--")


def test_create_bundle_envelope_with_given_bundle_id():
    obj1 = {
        "type": "indicator",
        "spec_version": "2.1",
        "id": "indicator--994479a7-e19b-4962-b66b-e1ff29f2442b",
        "created": "2024-06-24T12:34:56.000Z",
        "modified": "2024-06-24T12:34:56.000Z",
        "name": "Malicious IP Indicator",
        "pattern": "[ipv4-addr:value = '198.51.100.1']",
        "pattern_type": "stix",
        "valid_from": "2024-06-24T12:34:56.000Z",
    }
    objects = [obj1]
    bundle_id = "bundle--8b29a328-b42b-44b2-a990-2f40df776ddc"
    bundle = TAXIIClient.create_bundle_envelope(objects, bundle_id=bundle_id)
    assert bundle["id"] == bundle_id
