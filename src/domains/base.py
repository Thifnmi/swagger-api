import dataclasses
import uuid
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class BaseUUID(object):
    uuid: Optional[uuid.UUID]


@dataclasses.dataclass
class BaseID(object):
    id: Optional[int] = 0


@dataclasses.dataclass
class BaseDatetime(object):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
