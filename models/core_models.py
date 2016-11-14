import uuid
import abc
import json

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import Timestamp

from app import db


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    @property
    def python_type(self):
        return str

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class Element(db.Model, Timestamp):
    __abstract__ = True

    id = db.Column(GUID, primary_key=True)
    available = db.Column(db.Boolean, default=False)

    def __init__(self, id=''):
        if id:
            self.id = id
        else:
            self.id = uuid.uuid4()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def get_unique(cls, nsid):
        """
        Will get a unique instance of an object, this will use cache, so will
        avoid to handle same element's information in two or more instances.

        :param nsid: the id of the element's to query
        :return: an instance of an Element's child
        """
        session = db.session
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        key = (cls, nsid)
        o = cache.get(key)
        is_new = False
        if o is None:
            o = session.query(cls).filter_by(id=nsid).first()
            if o is None:
                o = cls(id=nsid)
                session.add(o)
                is_new = True
            cache[key] = o
        return (o, is_new)

    @classmethod
    def remove_from_cache(cls, o):
        """
        Will get a unique instance of an object, this will use cache, so will
        avoid to handle same element's information in two or more instances.

        :param nsid: the id of the element's to query
        :return: an instance of an Element's child
        """
        session = db.session
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        del cache[(cls, o.id)]

    @abc.abstractmethod
    def to_json(self, deep):
        """
        This will help flask_restful methods to cast model's instances
        as JSON, in some scenarios could be trivial, but this method will
        centralize how to handle it.
        :param deep: it will indicate if needs to get relationships.
            i.e:
                0 -> just model's own attributes
                1 -> model's own attributes + related own's attributes
                2 -> model's own attributes + relates own's attributes + relate's relates
                ...
        :return: a Valid JSON string
        """
        pass

    def build_children_array(self, objects, deep):
        children_array = []
        for o in objects:
            children_array.append(o.to_json(deep - 1, True))
        return children_array


class Result(Element):
    __tablename__ = 'results'

    url = db.Column(db.String())
    result = db.Column(JSON)
    job_id = db.Column(GUID, db.ForeignKey('jobs.id'))
    job = db.relationship("Job", backref=db.backref("results", uselist=False), foreign_keys=[job_id])

    def __init__(self, url, result):
        super(Result, self).__init__()
        self.url = url
        self.result = result

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self, deep):
        response = {
            "url": self.url,
            "result": self.result,
        }
        if deep > 0:
            response["job"] = self.job.to_json(deep - 1, True)
        return json.dumps(response)


class Job(Element):
    __tablename__ = 'jobs'

    status = db.Column(db.Integer)
    job_type = db.Column(db.String())
    tasks = db.relationship("Task")
    resources = db.relationship("Resource")
    result_id = db.Column(GUID, db.ForeignKey('results.id'))
    result = db.relationship("Result", backref=db.backref("jobs", uselist=False), foreign_keys=[result_id])

    def __init__(self, status=0, job_type='', *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.job_type = job_type
        self.status = status

    def __repr__(self):
        return '<id {} : type {}>'.format(self.id, self.job_type)

    def to_json(self, deep, as_dict=False):
        response = {
            "status": self.status,
            "job_type": self.job_type,
        }
        if deep > 0:
            response["tasks"] = self.build_children_array(self.tasks, deep)
            response["resources"] = self.build_children_array(self.resources, deep)
        return response


class Resource(Element):
    __tablename__ = 'resources'

    space_used_per_unit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    human_name = db.Column(db.String())
    job_id = db.Column(GUID, db.ForeignKey('jobs.id'))
    storage_id = db.Column(GUID, db.ForeignKey('storages.id'))

    def __init__(self, space_used_per_unit=0,
                 quantity=0, human_name=0):
        super(Resource, self).__init__()
        self.space_used_per_unit = space_used_per_unit
        self.quantity = quantity
        self.human_name = human_name

    def __repr__(self):
        return '<id {} : human_name {}>'.format(self.id, self.human_name)

    def to_json(self, deep, as_dict=False):
        response = {
            "space_used_per_unit": self.space_used_per_unit,
            "quantity": self.quantity,
            "human_name": self.human_name,

        }
        if deep > 0:
            if self.job_id:
                job = Job.get_unique(self.job_id)
                response["job"] = job.to_json(deep - 1, True)
            if self.storage_id:
                storage = Job.get_unique(self.storage_id)
                response["storage"] = storage.to_json(deep - 1, True)
        return json.dumps(response)


class Task(Element):
    __tablename__ = 'tasks'

    name = db.Column(db.String())
    steps = result = db.Column(JSON)
    status = db.Column(db.Integer)
    job_id = db.Column(GUID, db.ForeignKey('jobs.id'))

    def __init__(self, name='', status=0, steps=''):
        super(Task, self).__init__()
        self.name = name
        self.steps = steps
        self.status = status

    def __repr__(self):
        return '<id {} : type {}>'.format(self.id, self.job_type)

    def to_json(self, deep):
        pass


class Storage(Element):
    __tablename__ = 'storages'

    name = db.Column(db.String())
    endpoint = db.Column(db.String())
    capacity = db.Column(db.Integer)
    storage_type = db.Column(db.String())
    resources = db.relationship("Resource")
    dispatcher_id = db.Column(GUID, db.ForeignKey('dispatchers.id'))

    def __init__(self, name='', endpoint='', storage_type='', capacity=0):
        super(Storage, self).__init__()
        self.name = name
        self.endpoint = endpoint
        self.capacity = capacity
        self.storage_type = storage_type

    def __repr__(self):
        return '<id {} : name {}>'.format(self.id, self.name)

    def to_json(self, deep):
        pass


class Worker(Element):
    __tablename__ = 'workers'

    id = db.Column(GUID, primary_key=True)
    dispatcher_id = db.Column(GUID, db.ForeignKey('dispatchers.id'))

    def __init__(self):
        super(Worker, self).__init__()
        self.id = uuid.uuid4()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self, deep):
        pass


class Requester(Element):
    __tablename__ = 'requesters'

    id = db.Column(GUID, primary_key=True)
    dispatcher_id = db.Column(GUID, db.ForeignKey('dispatchers.id'))

    def __init__(self):
        super(Requester, self).__init__()
        self.id = uuid.uuid4()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self, deep):
        pass


class Dispatcher(Element):
    __tablename__ = 'dispatchers'

    id = db.Column(GUID, primary_key=True)
    storages = db.relationship("Storage")
    workers = db.relationship("Worker")
    attended_requesters = db.relationship("Requester")

    def __init__(self):
        super(Dispatcher, self).__init__()
        self.id = uuid.uuid4()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self, deep):
        pass
