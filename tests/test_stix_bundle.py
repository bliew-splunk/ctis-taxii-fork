from stix_bundle import STIXBundle
from stix2 import Identity

class TestSTIXBundle:
    def test_load_from_json_1(self):
        bundle = STIXBundle.from_dict({"bundle_id": "abc123"})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == []
        assert bundle.identities == []

    def test_load_from_json_2(self):
        indicators = [{"type": "indicator"}]
        identities = [{"type": "identity"}]
        bundle = STIXBundle.from_dict({"bundle_id": "abc123", "indicators": indicators, "identities": identities})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == indicators
        assert bundle.identities == identities

    def test_add_identity(self):
        bundle = STIXBundle()
        identity = Identity(name="test")
        bundle.add_identity(identity)
        as_dict = bundle.to_dict()
        bundle_identities = as_dict["identities"]
        assert len(bundle_identities) == 1
        assert bundle_identities[0]["name"] == "test"
        assert bundle_identities[0]["type"] == "identity"
