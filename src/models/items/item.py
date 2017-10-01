import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.stores.errors import StoreNotFoundError
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        try:
            self.store = Store.find_by_url(self.url)
        except StoreNotFoundError:
            self.store = None
        self.tag_name = self.store.tag_name if self.store is not None else None
        self.query = self.store.query if self.store is not None else None
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):

        if self.store is not None:
            element = None
            while element is None:
                request = requests.get(self.url)
                content = request.content

                soup = BeautifulSoup(content, "html.parser")

                element = soup.find(self.tag_name, self.query)

            string_price = element.text.strip()

            pattern = re.compile("(\d+.\d+)")
            match = pattern.search(string_price)

            self.price = float(match.group().replace(',', ''))
            return self.price
        else:
            return None

    def save_to_mongo(self):
        Database.update("items", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one("items", {"_id": item_id}))
