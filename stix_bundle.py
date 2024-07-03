import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict
from stix2 import Bundle, Identity


def new_bundle_id() -> str:
    bundle = Bundle()
    return bundle.id


@dataclass_json
@dataclass
class STIXBundle:
    bundle_id: str = field(default_factory=new_bundle_id)
    indicators: List[Dict] = field(default_factory=list)
    identities: List[Dict] = field(default_factory=list)

    def add_identity(self, identity: Identity):
        identity_dict = json.loads(identity.serialize())
        self.identities.append(identity_dict)


if __name__ == '__main__':
    bundle_with_id_arg = STIXBundle.from_dict({"bundle_id": "abc123"})
    print(bundle_with_id_arg)

    bundle_from_empty = STIXBundle.from_dict({})
    print(bundle_from_empty)
