import dataclasses
from uuid import UUID
from typing import Dict
from typing import Optional
from .base import BaseID, BaseDatetime

"""
class domain role
"""


@dataclasses.dataclass
class OwnerMap(BaseID, BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    name: str = ""
    description: str = ""
    is_custom: bool = True

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            name=adict["name"],
            description=adict["description"],
            is_custom=adict["is_custom"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "is_custom": self.is_custom,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
