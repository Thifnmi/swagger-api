import dataclasses
from uuid import UUID
from typing import Dict
from typing import Optional
from typing import List
from datetime import datetime
from .base import BaseDatetime

"""
class domain resource
"""


@dataclasses.dataclass
class Resource(BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    type: str = ""
    service_type: str = ""
    service_name: str = ""
    endpoint: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            type=adict["type"],
            service_type=adict["service_type"],
            service_name=adict["service_name"],
            endpoint=adict["endpoint"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "uuid": self.uuid,
            "type": self.type,
            "service_type": self.service_type,
            "service_name": self.service_name,
            "endpoint": self.endpoint,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
