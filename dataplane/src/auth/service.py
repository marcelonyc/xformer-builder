from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer
from typing import Annotated
from database import database, users, xformer_store
from auth.models import (
    RegisterUser,
    UserInDB,
    UserProfile,
    TokenData,
    Token,
    User,
)
from sqlalchemy import insert, select, update, func


security = HTTPBearer()


async def validate_app_token(
    request: Request,
    security: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if security.scheme.lower() != "bearer":
        raise credentials_exception
    get_user_query = select(users).where(users.c.token == security.credentials)
    try:
        user = await database.fetch_all(get_user_query)
    except Exception as e:
        raise credentials_exception
    _validation = {}
    if len(user) <= 0 or "Not authenticated" in user:
        raise credentials_exception
        _validation["status"] = False
    else:
        request.state.user_profile = UserProfile(**dict(user[0]))
        _validation["status"] = True
        _validation["user_profile"] = request.state.user_profile.model_dump()
        del _validation["user_profile"]["token"]

        # security.credentials

    return _validation


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
