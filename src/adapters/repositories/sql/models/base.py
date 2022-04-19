import re
import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utc import UtcDateTime, utcnow


Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4)


class BaseMixin():
    id = Column(Integer, primary_key=True)
    uuid  = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    created_at = Column(UtcDateTime, nullable=True, default=utcnow())
    updated_at = Column(UtcDateTime, nullable=True, onupdate=utcnow())
    deleted_at = Column(UtcDateTime, nullable=True)

    @staticmethod
    def load_from(domain_obj, depend_obj=None):
        raise NotImplementedError

    def to_domain(self, entities=[], **kwargs):
        raise NotImplementedError

    def _update(self, domain_obj, ignore_fields=[]):
        domain_keys = domain_obj.__dict__.keys()
        for key in self.__dict__.keys():
            if (
                key not in domain_keys
                or key in ignore_fields
                or key == "_sa_instance_state"
                or key == "id"
            ):
                continue
            value = getattr(domain_obj, key)
            if value is not None and value != "":
                setattr(self, key, value)
