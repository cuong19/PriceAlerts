import datetime
import uuid

from src.common.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        # return requests.post(
        #     AlertConstants.URL,
        #     auth=("api", AlertConstants.API_KEY),
        #     data={
        #         "from": AlertConstants.FROM,
        #         "to": self.user_email,
        #         "subject": "Price limit reached for {}".format(self.item.name),
        #         "text": "We've found a deal! ({}).".format(self.item.url)
        #     }
        # )
        print("Now just pretend there is a mail is already sent to {} here.".format(self.user_email))

    @classmethod
    def find_needing_update(cls, minutes_since_update=10):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in
                Database.find("alerts", {"last_checked": {"$lte": last_updated_limit}, "active": True})]

    def save_to_mongo(self):
        Database.update("alerts", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        price = self.item.load_price()
        if price is not None:
            self.last_checked = datetime.datetime.utcnow()
            self.item.save_to_mongo()
            self.save_to_mongo()
            return self.item.price
        else:
            return None

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return (cls(**elem) for elem in Database.find("alerts", {'user_email': user_email}))

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one("alerts", {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove('alerts', {"_id": self._id})
