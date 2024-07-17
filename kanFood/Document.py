from kanFood.mongodb import  db
from uitls.utils import generate_id


class Document:
    __TABLE__ = None
    _id = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def db(self):
        return db[self.__TABLE__]

    def save(self):
        if self._id:
            self.db().update_one({"_id": self._id}, {"$set": self.to_dict()})
        else:
            self._id = generate_id()
            self.db().insert_one(self.to_dict())
        return self

    def save_all(self, items):
        # Generate id only if not present
        items = [{**item, "_id": item.get("_id", generate_id())} for item in items]
        self.db().insert_many(items)

    def load(self, query=None):
        if not query:
            query = {"_id": self._id}
        self.from_dict(self.db().find_one(query))
        return self

    def delete(self, query=None):
        if self._id:
            if not query:
                query = {"_id": self._id}
            self.db().delete_one(query)
        return self

    def to_dict(self):
        return self.__dict__

    def from_dict(self, d):
        if d:
            self.__dict__ = d
        else:
            self._id = None
        return self

    def aggregate(self, pipeline):
        return self.db().aggregate(pipeline)

    @classmethod
    def get_all(cls, query={}):
        return [cls(**r) for r in cls().db().find(query)]

    @classmethod
    def drop(cls):
        return cls().db().drop()