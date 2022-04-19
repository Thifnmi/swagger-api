from email.policy import default
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


class Permission(Base, BaseMixin):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)

    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    role_uuid = Column(String(36), name="role_uuid", default=generate_uuid)
    resource_uuid = Column(String(36), name="resource_uuid", default=generate_uuid)
    action = Column(String)