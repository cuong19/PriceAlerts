import os

DEBUG = False
ADMINS = frozenset([
    "admin@example.com"
])
DATABASE_URI = os.environ.get("MONGODB_URI")
DATABASE_COLLECTION = os.environ.get("MONGODB_DATABASE")
