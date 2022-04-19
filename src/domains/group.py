import dataclasses
from uuid import UUID
from datetime import datetime
from typing import Dict
from typing import Optional
from .base import BaseDatetime

"""
class domain group
"""

@dataclasses.dataclass
class Group(BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    name: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            name=adict["name"],
            uuid=adict["uuid"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "uuid": self.uuid,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
