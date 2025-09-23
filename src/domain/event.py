from datetime import datetime, date
from typing import Optional
from src.domain.entry import Entry # Import Entry from the same domain package

class Event(Entry):
    def __init__(self, id: str, content: str, creation_date: date, last_modified_date: date,
                 start_datetime: datetime, end_datetime: Optional[datetime] = None,
                 location: Optional[str] = None):
        super().__init__(id, content, creation_date, last_modified_date)
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.location = location

    def set_time_range(self, start: datetime, end: Optional[datetime] = None) -> None:
        """Sets or updates the time range for the event."""
        self.start_datetime = start
        self.end_datetime = end
        self.last_modified_date = date.today()

    def set_location(self, loc: str) -> None:
        """Sets or updates the location for the event."""
        self.location = loc
        self.last_modified_date = date.today()

    def edit_content(self, new_content: str) -> None:
        """Overrides the abstract edit_content method from Entry."""
        self.content = new_content
        self.last_modified_date = date.today()

    def delete(self) -> None:
        """Overrides the abstract delete method from Entry."""
        # 実際の削除ロジックは永続化を考慮する際に洗練されるため、ここではpassとする
        pass
