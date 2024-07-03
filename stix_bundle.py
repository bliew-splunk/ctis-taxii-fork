from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict
from stix2 import Bundle


def new_bundle_id() -> str:
    bundle = Bundle()
    return bundle.id


@dataclass_json
@dataclass
class STIXBundle:
    bundle_id: str = field(default_factory=new_bundle_id)
    indicators: List[Dict] = field(default_factory=list)
    identity: Dict = field(default_factory=dict)


if __name__ == '__main__':
    bundle_with_id_arg = STIXBundle.from_dict({"bundle_id": "abc123"})
    print(bundle_with_id_arg)

    bundle_from_empty = STIXBundle.from_dict({})
    print(bundle_from_empty)
