from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

class Entry(ABC):
    def __init__(self, id: str, content: str, creation_date: date, last_modified_date: date):
        self.id = id
        self.content = content
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date

    @abstractmethod
    def edit_content(self, new_content: str) -> None:
        """
        Updates the content of the entry and sets the last modified date to today.
        This method must be implemented by concrete subclasses.
        """
        pass

    @abstractmethod
    def delete(self) -> None:
        """
        Abstract method to be implemented by concrete subclasses for deleting an entry.
        """
        pass