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


class Group(Base, BaseMixin):
    __tablename__ = "group_x"

    id = Column(Integer, primary_key=True)

    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    name = Column(String, nullable=False)