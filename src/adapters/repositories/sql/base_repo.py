import logging
import pybreaker
import transaction
from uuid import UUID
from pybreaker import CircuitBreakerError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy_pagination import paginate
from zope.sqlalchemy import register
from retrying import retry

"""
use abstract base class for all repository object
"""


class BaseRepo(pybreaker.CircuitBreakerListener):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._open()

    def _close(self):
        self.session.close()

    def _open(self):
        self._local_db = None
        self.engine = create_engine(
            self.connection_string, echo_pool=True
        )  # , checkfirst=True)
        self.db_session = BaseRepo.get_session_factory(
            self.engine
        )  # sessionmaker(bind=self.engine)  # , autocommit=True
        self.session = self.db_session()
        # use transaction module with zope to manage tx sql
        # self.transaction_manager = transaction.TransactionManager(explicit=True)
        # register(self.session, transaction_manager=self.transaction_manager)

    def before_call(self, cb, func, *args, **kwargs):
        "Called before the circuit breaker `cb` calls `func`."
        try:
            self.session.execute("SELECT 1")
            self.session.commit()
        except Exception:
            self.session.rollback()
            yield CircuitBreakerError("cannot connect database")

    def state_change(self, cb, old_state, new_state):
        "Called when the circuit breaker `cb` state changes."
        self._open()

    def failure(self, cb, exc):
        "Called when a function invocation raises a system error."
        pass

    def success(self, cb):
        "Called when a function invocation succeeds."
        pass

    def __parse_field_to_dict(self, field, value):
        _dict = {}
        _dict[field] = value
        return _dict

    @staticmethod
    def get_session_factory(engine):
        maker = sessionmaker()
        maker.configure(bind=engine)
        return maker

    @staticmethod
    def get_tm_session(session_factory, transaction_manager):
        session = session_factory()
        register(session, transaction_manager=transaction_manager)
        return session

    def get_session(self):
        # Store _local_db to avoid confusing it with the one that was
        # passed into us such that we make a new local db for each instance
        db = self.db or self._local_db
        if db is None:
            db_session = self.db_session
            if db_session is None:
                engine = self.engine
                db_session, self.db_session = BaseRepo.get_session_factory(engine)
            if self.transaction_manager:
                db = BaseRepo.get_tm_session(db_session, self.transaction_manager)
            else:
                db = db_session()
            self._local_db = db
        return db

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _create_object(self, domain_obj, depend_obj=None, flush=True, entities=[]):
        """
            creat a new model
            @domain_obj: origin domain object
            @depend_obj: relation object
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            try:
                obj = self.model.load_from(domain_obj=domain_obj, depend_obj=depend_obj)
                session.add(obj)
                # if flush:
                #     session.flush()
                return obj.to_domain(entities=entities)
            except Exception as e:
                logging.error(e)

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _create_object_with_associate(
        self,
        domain_obj,
        associate_field,
        associate_obj,
        associate_model,
        depend_obj=None,
        flush=True,
        entities=[],
    ):
        """
            creat a new model with add associates
            @domain_obj: origin domain object
            @associate_field: field need to use associate in domain obj
            @associate_obj: domain associate object
            @model: model of associate
            @depend_obj: relation object
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            try:
                obj = self.model.load_from(domain_obj=domain_obj, depend_obj=depend_obj)
                associate = (
                    session.query(associate_model)
                    .filter_by(uuid=UUID(associate_obj.uuid))
                    .first()
                )
                if associate:
                    associate_attr = getattr(obj, associate_field)
                    associate_attr.append(associate)
                session.add(associate)
                if flush:
                    session.flush()
                return obj.to_domain(entities=entities)
            except Exception as e:
                logging.error(e)

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _update_object(self, domain_obj, field, flush=True, entities=[]):
        """
            allow update model based by field
            @domain_obj: origin domain object
            @field: key for finding object
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            obj = (
                session.query(self.model)
                .filter_by(
                    **self.__parse_field_to_dict(field, getattr(domain_obj, field))
                )
                .first()
            )
            if obj:
                obj._update(domain_obj=domain_obj, ignore_fields=[field])
                try:
                    if flush:
                        session.flush()
                except Exception as e:
                    logging.error(e)
                    self.session.rollback()
            return obj.to_domain(entities=entities) if obj else None

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _delete_object(self, domain_obj, field, flush=True):
        """
            delete a model
            @domain_obj: origin domain object
            @field: key for finding object
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            obj = (
                session.query(self.model)
                .filter_by(
                    **self.__parse_field_to_dict(field, getattr(domain_obj, field))
                )
                .first()
            )
            if not obj:
                return False

            session.delete(obj)
            try:
                if flush:
                    session.flush()
            except Exception as e:
                logging.error(e)
            return True

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _get_object(self, domain_obj, field, entities=[]):
        """
            get a model
            @domain_obj: origin domain object
            @field: key for finding object
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            obj = (
                session.query(self.model)
                .filter_by(
                    **self.__parse_field_to_dict(field, getattr(domain_obj, field))
                )
                .first()
            )
            return obj.to_domain(entities=entities) if obj else None

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _list_object(
        self, filters=None, orders=None, page=1, limit=20, all=None, entities=[]
    ):
        """
            list a model
            @filters: fields need for filter/search
            @orders: key for finding object
            @page: offset to page
            @limit: total number for per page
            @all: boolean
            @entities: array, include column query in table
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            objs = session.query(self.model)
            if orders:
                order_column, order_type = orders
                objs = objs.order_by(
                    getattr(getattr(self.model, order_column), order_type)()
                )
            if len(entities) > 0:
                objs = objs.options(load_only(*entities))
                # for entity in entities:
                #     field = getattr(self.model, entity, None)
                #     if field:
                #         objs = objs.with_entities(field)
            if all is not None:
                objs = paginate(objs, 1, objs.count())
            elif filters and isinstance(filters, dict):
                objs = paginate(objs.filter(**filters), page, limit)
            elif filters and isinstance(filters, str):
                objs = paginate(objs.filter(eval(filters)), page, limit)
            else:
                objs = paginate(objs, page, limit)

            return [obj.to_domain(entities=entities) for obj in objs.items]

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _list_object_by(
        self, domain_obj, field, page=1, limit=20, all=None, entities=[]
    ):
        """
            list a model
            @domain_obj: origin domain object
            @field: key for finding object
            @page: offset to page
            @limit: total number for per page
            @all: boolean
        """
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            filters = (
                session.query(self.model).filter_by(
                    **self.__parse_field_to_dict(field, getattr(domain_obj, field)),
                ),
            )
            if all is not None:
                objs = paginate(filters, 1, filters.count())
            else:
                objs = paginate(filters, page, limit)
            return [obj.to_domain(entities=entities) for obj in objs.items]

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _delete_associate_obj(
        self, domain_obj, domain_field, obj, model, field, flush=True
    ):
        query_dict = {}
        query_dict[domain_field] = getattr(domain_obj, domain_field)
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            o = session.query(self.model).filter_by(**query_dict).first()
            if o:
                link_obj = session.query(model).filter_by(**{"uuid": UUID(obj.uuid),}).first()
                if link_obj:
                    associate_obj = getattr(o, field)
                    associate_obj.remove(link_obj)
                    try:
                        session.add(associate_obj)
                        if flush:
                            session.flush()
                    except Exception as e:
                        logging.error(e)
                        return False
                    return True
            return False

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _add_associate_obj(
        self, domain_obj, domain_field, obj, model, field, flush=True
    ):

        query_dict = {}
        query_dict[domain_field] = getattr(domain_obj, domain_field)
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            session = BaseRepo.get_tm_session(self.db_session, transaction_manager=tm)
            o = session.query(self.model).filter_by(**query_dict).first()
            if o:
                link_obj = session.query(model).filter_by(**{"uuid": UUID(obj.uuid),}).first()
                if link_obj:
                    associate_obj = getattr(o, field)
                    associate_obj.append(link_obj)
                    try:
                        session.add(associate_obj)
                        if flush:
                            session.flush()
                    except Exception as e:
                        logging.error(e)
                        return False
                    return True
            return False

    @retry(stop_max_attempt_number=3, stop_max_delay=25000)
    def _get_associate_obj(self, domain_obj, domain_field, obj, field, entities=[]):
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            o = self._get_object(domain_obj, domain_field)
            if o:
                associate_obj = getattr(o, field)
                return [obj.to_domain(entities=entities) for obj in associate_obj]
            return []

    def _count(self):
        tm = transaction.TransactionManager(explicit=True)
        with tm:
            return self.session.query(self.model).count()
