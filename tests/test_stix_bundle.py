from stix_bundle import STIXBundle


class TestSTIXBundle:
    def test_load_from_json_1(self):
        bundle = STIXBundle.from_dict({"bundle_id": "abc123"})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == []
        assert bundle.identity == {}

    def test_load_from_json_2(self):
        indicators = [{"type": "indicator"}]
        identity = {"type": "identity"}
        bundle = STIXBundle.from_dict({"bundle_id": "abc123", "indicators": indicators, "identity": identity})
        assert bundle.bundle_id == "abc123"
        assert bundle.indicators == indicators
        assert bundle.identity == identity
