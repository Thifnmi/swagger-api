import dataclasses
from typing import Dict, Optional
from uuid import UUID
from .base import BaseDatetime

"""
class domain resource mapping
"""


@dataclasses.dataclass
class ResourceMapping(BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    resource_uuid: Optional[UUID] = dataclasses.field(default=None)
    url: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            resource_uuid=adict["resource_uuid"],
            url=adict["url"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "resource_uuid": self.resource_uuid,
            "url": self.url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
