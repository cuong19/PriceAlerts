import uuid

from src.common.database import Database
from src.models.stores.errors import StoreNotFoundError


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one("stores", {"_id": _id}))

    def save_to_mongo(self):
        Database.update("stores", {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one("stores", {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one("stores", {"url_prefix": {"$regex": '^{}$'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        try:
            for i in range(0, len(url) + 1):
                url_prefix = url[:(len(url) - i)]
                try:
                    store = cls.get_by_url_prefix(url_prefix)
                except:
                    store = None
                if store is not None:
                    return store
        except:
            raise StoreNotFoundError("Store not found.")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('stores', {})]

    def delete(self):
        Database.remove('stores', {'_id': self._id})
