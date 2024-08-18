from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(User):
    hashed_password: str = None


class RegisterUser(BaseModel):
    name: str = ""
    email: EmailStr = ""
    description: Optional[str] = ""


class RegisterUserResponse(BaseModel):
    app_token: str = ""


class UserProfile(RegisterUser):
    id: str = None
    token: str = None
