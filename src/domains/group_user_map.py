import dataclasses
from uuid import UUID
from datetime import datetime
from typing import Dict
from typing import Optional
from .base import BaseDatetime

"""
class domain group user map
"""


@dataclasses.dataclass
class GroupUserMap(BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    group_uuid: Optional[UUID] = dataclasses.field(default=None)
    user_uuid: Optional[UUID] = dataclasses.field(default=None)

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            group_uuid=adict["group_uuid"],
            user_uuid=adict["user_uuid"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "group_uuid": self.group_uuid,
            "user_uuid": self.user_uuid,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
