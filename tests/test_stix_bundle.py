from stix_bundle import STIXBundleContainer
from stix2 import Identity, Indicator, TLP_RED


class TestSTIXBundle:
    def test_load_from_json_1(self):
        bundle = STIXBundleContainer.from_dict({"bundle_id": "abc123"})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == []
        assert bundle.identities == []

    def test_load_from_json_2(self):
        indicators = [{"type": "indicator"}]
        identities = [{"type": "identity"}]
        bundle = STIXBundleContainer.from_dict(
            {"bundle_id": "abc123", "indicators": indicators, "identities": identities})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == indicators
        assert bundle.identities == identities

    def test_add_identity(self):
        bundle = STIXBundleContainer()
        identity = Identity(name="test")
        bundle.add_identity(identity)
        as_dict = bundle.to_dict()
        bundle_identities = as_dict["identities"]
        assert len(bundle_identities) == 1
        assert bundle_identities[0]["name"] == "test"
        assert bundle_identities[0]["type"] == "identity"

    def test_convert_to_canonical_bundle_dict(self):
        bundle = STIXBundleContainer()
        identity = Identity(name="test")
        bundle.add_identity(identity)
        indicator = Indicator(pattern="[url:value = 'https://www.example.com']", pattern_type="stix",
                              object_marking_refs=TLP_RED)
        bundle.indicators.append(indicator)
        as_dict = bundle.to_canonical_bundle_dict()
        assert as_dict["type"] == "bundle"
        assert as_dict["id"] == bundle.bundle_id
        assert len(as_dict["objects"]) == 3

        object_ids = set([x["id"] for x in as_dict["objects"]])
        assert "marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed" in object_ids
        assert indicator.id in object_ids
        assert identity.id in object_ids
