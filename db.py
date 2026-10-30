"""Database layer (APP-04).
The rest of the app never talks to MongoDB directly, only through these functions."""
import os
from datetime import datetime, timezone
from urllib.parse import quote_plus

from pymongo import MongoClient

# Settings come from environment variables (set in the Helm chart)
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_USER = os.environ.get("MONGO_USER", "root")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")

if MONGO_PASSWORD:
    MONGO_URL = f"mongodb://{MONGO_USER}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:27017/?authSource=admin"
else:
    MONGO_URL = f"mongodb://{MONGO_HOST}:27017/"

# Wait at most 2 seconds for the database, so a problem shows up fast
client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000, connect=False)
visits = client["finalproject"]["visits"]


def add_visit():
    """Save one visit with the current time."""
    visits.insert_one({"time": datetime.now(timezone.utc)})


def count_visits():
    """Return how many visits were saved so far."""
    return visits.count_documents({})


def ping():
    """Check that the database answers. Raises an error if it does not."""
    client.admin.command("ping")
