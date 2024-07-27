import dataclasses

@dataclases(slots=True)
class EditorRow():
    text: str
    cursor: int