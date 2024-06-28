import json
from typing import List, Dict, Set
from stix2 import TLP_WHITE, TLP_RED, TLP_AMBER, TLP_GREEN

ID_TO_TLP_MARKING_DEFINITION = {
    TLP_WHITE.id: TLP_WHITE,
    TLP_RED.id: TLP_RED,
    TLP_AMBER.id: TLP_AMBER,
    TLP_GREEN.id: TLP_GREEN
}
TLP_MARKING_DEFINITION_IDS = set(ID_TO_TLP_MARKING_DEFINITION.keys())


def gather_object_marking_refs(objects: List[Dict]) -> Set:
    marking_refs = set()
    for object_ in objects:
        object_marking_refs = object_.get("object_marking_refs", [])
        assert type(object_marking_refs) == list
        marking_refs.update(object_marking_refs)
    return marking_refs


def gather_tlp_marking_definition_ids(objects: List[Dict]) -> Set:
    marking_refs = gather_object_marking_refs(objects)
    filtered = TLP_MARKING_DEFINITION_IDS.intersection(marking_refs)
    return filtered


def get_tlp_marking_definition_for_id(marking_definition_id: str) -> dict:
    as_json = ID_TO_TLP_MARKING_DEFINITION[marking_definition_id].serialize()
    as_dict = json.loads(as_json)
    return as_dict


def generate_tlp_marking_definitions(objects: List[Dict]) -> List:
    tlp_marking_def_ids = gather_tlp_marking_definition_ids(objects)
    result = [get_tlp_marking_definition_for_id(x) for x in tlp_marking_def_ids]
    return result
