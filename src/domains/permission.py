import dataclasses
from uuid import UUID
from typing import Dict, List, Optional
from datetime import datetime
from .base import BaseID, BaseDatetime

"""
class domain permission
"""


@dataclasses.dataclass
class Permission(BaseID, BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    role_uuid: Optional[UUID] = dataclasses.field(default=None)
    resource_uuid: Optional[UUID] = dataclasses.field(default=None)
    acction: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            role_uuid=adict["role_uuid"],
            resource_uuid=adict["resource_uuid"],
            acction=adict["acction"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "role_uuid": self.role_uuid,
            "resource_uuid": self.resource_uuid,
            "acction": self.acction,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
