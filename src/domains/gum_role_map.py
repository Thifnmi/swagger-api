import dataclasses
from uuid import UUID
from datetime import datetime
from typing import Dict
from typing import Optional
from .base import BaseDatetime

"""
class domain gum role map
"""


@dataclasses.dataclass
class GUMRoleMap(BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    gum_uuid: Optional[UUID] = dataclasses.field(default=None)
    role_uuid: Optional[UUID] = dataclasses.field(default=None)

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            gum_uuid=adict["gum_uuid"],
            role_uuid=adict["role_uuid"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "gum_uuid": self.gum_uuid,
            "role_uuid": self.role_uuid,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

