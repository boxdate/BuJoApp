from datetime import date
from typing import Optional, List
from enum import Enum
from src.domain.entry import Entry # Import Entry from the same domain package

class CollectionType(Enum):
    DAILY = "Daily"
    MONTHLY = "Monthly"
    CUSTOM = "Custom"

class Collection:
    def __init__(self, name: str, type: CollectionType,
                 start_date: Optional[date] = None, end_date: Optional[date] = None):
        self.name = name
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        self._entries: List[Entry] = [] # Private list to hold entries

    def add_entry(self, entry: Entry) -> None:
        """Adds an entry to the collection."""
        self._entries.append(entry)

    def remove_entry(self, entry: Entry) -> None:
        """Removes an entry from the collection."""
        if entry in self._entries:
            self._entries.remove(entry)

    def get_entries_by_date(self, target_date: date) -> List[Entry]:
        """Returns entries within the collection for a specific date."""
        # This logic might need refinement based on how entries are dated and filtered.
        # For now, a simple filter based on creation_date.
        return [entry for entry in self._entries if entry.creation_date == target_date]

    @property
    def entries(self) -> List[Entry]:
        """Returns a copy of the entries list to prevent external modification."""
        return list(self._entries)
