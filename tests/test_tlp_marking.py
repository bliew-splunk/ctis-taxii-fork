from tlp_marking import gather_tlp_marking_definition_ids, get_tlp_marking_definition_for_id, \
    generate_tlp_marking_definitions

MARKING_DEFINITION_TLP_RED = "marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed"
MARKING_DEFINITION_TLP_WHITE = "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"
MARKING_DEFINITION_TLP_GREEN = "marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"
MARKING_DEFINITION_TLP_AMBER = "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"

MARKING_DEFINITION_NON_TLP_EXAMPLE = "marking-definition-abc123"


class TestGatherTLPMarkingDefinitionIDs:
    def test_single_object_list_non_tlp_value(self):
        objects = [{"object_marking_refs": [MARKING_DEFINITION_NON_TLP_EXAMPLE]}]
        assert gather_tlp_marking_definition_ids(objects) == set()

    def test_single_object_list_tlp_value(self):
        objects = [{"object_marking_refs": [MARKING_DEFINITION_TLP_RED]}]
        assert gather_tlp_marking_definition_ids(objects) == {MARKING_DEFINITION_TLP_RED}

    def test_empty_list(self):
        assert gather_tlp_marking_definition_ids([]) == set()

    def test_objects_list(self):
        objects = [
            {"object_marking_refs": [MARKING_DEFINITION_TLP_AMBER, MARKING_DEFINITION_TLP_GREEN]},
            {"object_marking_refs": [MARKING_DEFINITION_TLP_RED, MARKING_DEFINITION_TLP_WHITE]},
            {"object_marking_refs": [MARKING_DEFINITION_TLP_AMBER, MARKING_DEFINITION_NON_TLP_EXAMPLE]},
            {"something_else": 123},
        ]
        assert gather_tlp_marking_definition_ids(objects) == {
            MARKING_DEFINITION_TLP_WHITE,
            MARKING_DEFINITION_TLP_GREEN,
            MARKING_DEFINITION_TLP_AMBER,
            MARKING_DEFINITION_TLP_RED,
        }


class TestGetTLPMarkingDefinitionForID:
    def test_get_tlp_red(self):
        definition = get_tlp_marking_definition_for_id(marking_definition_id=MARKING_DEFINITION_TLP_RED)
        assert type(definition) == dict
        assert definition["name"] == "TLP:RED"
        assert definition["id"] == MARKING_DEFINITION_TLP_RED
        assert definition["type"] == "marking-definition"
        assert definition["definition"]["tlp"] == "red"

    def test_get_tlp_white(self):
        definition = get_tlp_marking_definition_for_id(marking_definition_id=MARKING_DEFINITION_TLP_WHITE)
        assert definition["name"] == "TLP:WHITE"
        assert definition["id"] == MARKING_DEFINITION_TLP_WHITE

    def test_get_tlp_amber(self):
        definition = get_tlp_marking_definition_for_id(marking_definition_id=MARKING_DEFINITION_TLP_GREEN)
        assert definition["name"] == "TLP:GREEN"
        assert definition["id"] == MARKING_DEFINITION_TLP_GREEN

    def test_get_tlp_green(self):
        definition = get_tlp_marking_definition_for_id(marking_definition_id=MARKING_DEFINITION_TLP_AMBER)
        assert definition["name"] == "TLP:AMBER"
        assert definition["id"] == MARKING_DEFINITION_TLP_AMBER


class TestGenerateTLPMarkingDefinitionsForObjects:
    def test_empty_list(self):
        assert generate_tlp_marking_definitions([]) == []

    def test_that_only_unique_definitions_are_generated(self):
        objects = [
            {"object_marking_refs": [MARKING_DEFINITION_TLP_RED]},
            {"object_marking_refs": [MARKING_DEFINITION_TLP_RED, MARKING_DEFINITION_TLP_WHITE,
                                     MARKING_DEFINITION_TLP_GREEN]},
        ]
        result = generate_tlp_marking_definitions(objects)
        assert type(result) == list
        assert len(result) == 3
        assert type(result[0]) == dict
        assert set([x["name"] for x in result]) == {"TLP:RED", "TLP:WHITE", "TLP:GREEN"}
