from dataclasses import dataclass, fields
from typing import Any, Dict

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Statistics:
    __slots__ = ["name"]
    name: str

    def flatten(self) -> Dict[str, Any]:
        out = {}
        for field in fields(self):
            field_val = getattr(self, field.name)
            if field.name != "name":
                out[f"{self.name}_{field.name}"] = field_val

        return out
