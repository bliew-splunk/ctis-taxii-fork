from stix2 import Identity
import json


def test_identity_with_id_arg():
    my_id = "identity--ff0ade7d-a24a-4cad-b2c9-0230abd483a4"
    identity_with_autogen_id = Identity(id=my_id, name="Corpa", identity_class="organization")
    assert identity_with_autogen_id.id == my_id
    assert identity_with_autogen_id.name == "Corpa"


def test_identity_with_autogen_id():
    identity_with_autogen_id = Identity(name="Alice", identity_class="individual")
    assert identity_with_autogen_id.id.startswith("identity--")

    identity_dict = json.loads(identity_with_autogen_id.serialize())
    assert identity_dict["name"] == "Alice"
    assert identity_dict["identity_class"] == "individual"
