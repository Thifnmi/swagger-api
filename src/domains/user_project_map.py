import dataclasses
from uuid import UUID
from typing import Dict
from typing import Optional
from .base import BaseID, BaseDatetime

"""
class project namespace maps
"""


@dataclasses.dataclass
class ProjectNamespaceMap(BaseID, BaseDatetime):
    parent_uuid: Optional[UUID] = dataclasses.field(default=None)
    child_uuid: Optional[UUID] = dataclasses.field(default=None)
    is_active: bool = True

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            parent_uuid=adict["parent_uuid"],
            child_uuid=adict["child_uuid"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
            is_active=adict["is_active"],
        )

    def to_dict(self) -> Dict:
        return {
            "parent_uuid": self.parent_uuid,
            "child_uuid": self.child_uuid,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
            "is_active": self.is_active,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
