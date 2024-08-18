from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str = None
    email: str = None
    description: str = None
    id: str = None
