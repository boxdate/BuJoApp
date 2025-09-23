from datetime import date
from typing import Optional
from enum import Enum
from src.domain.entry import Entry # Import Entry from the same domain package

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(Entry):
    def __init__(self, id: str, content: str, creation_date: date, last_modified_date: date,
                 is_completed: bool = False, due_date: Optional[date] = None,
                 priority: Optional[TaskPriority] = None):
        super().__init__(id, content, creation_date, last_modified_date)
        self.is_completed = is_completed
        self.due_date = due_date
        self.priority = priority

    def mark_as_completed(self) -> None:
        """Marks the task as completed."""
        self.is_completed = True
        self.last_modified_date = date.today()

    def set_due_date(self, new_due_date: date) -> None:
        """Sets or updates the due date for the task."""
        self.due_date = new_due_date
        self.last_modified_date = date.today()

    def edit_content(self, new_content: str) -> None:
        """Overrides the abstract edit_content method from Entry."""
        # Entryのedit_contentは抽象メソッドなので、ここでは具体的な実装を行う
        self.content = new_content
        self.last_modified_date = date.today()

    def delete(self) -> None:
        """
        Overrides the abstract delete method from Entry."""
        # 実際の削除ロジックは永続化を考慮する際に洗練されるため、ここではpassとする
        pass
