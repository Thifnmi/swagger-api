import dataclasses
from typing import Dict, Optional
from uuid import UUID
from .base import BaseID, BaseDatetime

"""
class domain user
"""


@dataclasses.dataclass
class User(BaseID, BaseDatetime):
    uuid: Optional[UUID] = dataclasses.field(default=None)
    email: str = ""

    @classmethod
    def from_dict(cls, adict: Dict):
        return cls(
            uuid=adict["uuid"],
            email=adict["email"],
            created_at=adict["created_at"],
            updated_at=adict["updated_at"],
            delete_at=adict["deleted_at"],
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "delete_at": self.deleted_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
