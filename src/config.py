import os

DEBUG = False
ADMINS = frozenset([
    "admin@example.com"
])
DATABASE_URI = os.environ.get("MONGOLAB_URI")
DATABASE_COLLECTION = 'price_alerts'
