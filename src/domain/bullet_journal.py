from datetime import date
from typing import List
from src.domain.collection import Collection # Import Collection from the same domain package

class BulletJournal:
    def __init__(self, name: str, creation_date: date):
        self.name = name
        self.creation_date = creation_date
        self._collections: List[Collection] = [] # Private list to hold collections

    def add_collection(self, collection: Collection) -> None:
        """Adds a collection to the bullet journal."""
        self._collections.append(collection)

    def remove_collection(self, collection: Collection) -> None:
        """Removes a collection from the bullet journal."""
        if collection in self._collections:
            self._collections.remove(collection)

    @property
    def collections(self) -> List[Collection]:
        """Returns a copy of the collections list to prevent external modification."""
        return list(self._collections)
