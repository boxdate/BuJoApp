from typing import Optional

class Tag:
    def __init__(self, name: str, color: Optional[str] = None):
        self.name = name
        self.color = color
