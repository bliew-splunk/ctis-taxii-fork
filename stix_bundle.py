from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict


@dataclass_json
@dataclass
class STIXBundle:
    bundle_id: str
    indicators: List[Dict] = field(default_factory=list)
    identity: Dict = field(default_factory=dict)


if __name__ == '__main__':
    bundle = STIXBundle.from_dict({"bundle_id": "abc123"})
    print(bundle)
