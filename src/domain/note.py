from datetime import date
from src.domain.entry import Entry # Import Entry from the same domain package

class Note(Entry):
    def __init__(self, id: str, content: str, creation_date: date, last_modified_date: date):
        super().__init__(id, content, creation_date, last_modified_date)

    def edit_content(self, new_content: str) -> None:
        """Overrides the abstract edit_content method from Entry."""
        self.content = new_content
        self.last_modified_date = date.today()

    def delete(self) -> None:
        """Overrides the abstract delete method from Entry."""
        # 実際の削除ロジックは永続化を考慮する際に洗練されるため、ここではpassとする
        pass
