from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from src.adapters.repositories.sql.models.base import Base
from src.adapters.repositories.sql.models.base import BaseMixin
from src.adapters.repositories.sql.models.base import generate_uuid


class UserProjectMap(Base, BaseMixin):
    __tablename__ = "user_poroject_map"

    id = Column(Integer, primary_key=True)

    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    user_uuid = Column(String(36), name="user_uuid", default=generate_uuid)
    project_uuid = Column(String(36), name="project_uuid", default=generate_uuid)