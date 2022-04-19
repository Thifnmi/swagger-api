import logging
from uuid import UUID

import transaction
from retrying import retry
from sqlalchemy_pagination import paginate

from src.adapters.repositories.sql.base_repo import BaseRepo
from src.adapters.repositories.sql.models import Group as GM
from src.domains import Group as G
from src.utils.circult_breaker import db_breaker


class GroupRepo(BaseRepo):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.domain = G
        self.model = GM
        self.model.metadata.bind = self.engine

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _update_group(self, uuid, name, flush=True, entities=[], **kwargs):
        """
        allow update name in group
        @uuid: uuid of group
        @name: name field in group
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            obj = session.query(self.model).filter(self.model.uuid == str(UUID(uuid))).first()
            if obj:
                obj.name = name
                try:
                    if flush:
                        session.flush()
                except Exception as e:
                    logging.error(e)
                    self.session.rollback()
            return obj.to_domain(entities=entities, **kwargs) if obj else None

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _get_object_with_uuid(self, uuid, entities=[], **kwargs):
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            obj = session.query(self.model).filter(self.model.uuid == str(UUID(uuid))).first()
            return obj.to_domain(entities=entities, **kwargs) if obj else None

