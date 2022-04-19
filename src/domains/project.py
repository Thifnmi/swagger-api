import dataclasses
from typing import Dict, List, Optional
from uuid import UUID

from .user import Account
from .base import BaseDatetime, BaseID
from .group import Group
from .role import OwnerMap

"""
class domain project
"""


@dataclasses.dataclass
class Project(BaseID, BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    name: str = ""
    description: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            name=adict["name"],
            description=adict["description"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
            is_active=adict["is_active"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
