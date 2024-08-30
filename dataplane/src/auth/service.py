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
from config.app_config import get_settings
from auth.utils import TokenManager


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
    _tm = TokenManager()
    get_user_query = select(users).where(
        users.c.username == security.credentials[: _tm.id_position]
    )
    try:
        user = await database.fetch_all(get_user_query)
    except Exception as e:
        raise credentials_exception
    _validation = {}
    _user_profile = UserProfile(**dict(user[0]))
    if len(user) <= 0 or "Not authenticated" in user:
        raise credentials_exception
    elif not _tm.verify_token(
        _user_profile.salt, _user_profile.hashed_token, security.credentials
    ):
        raise credentials_exception
    else:
        request.state.user_profile = _user_profile
        _validation["status"] = True
        _validation["user_profile"] = request.state.user_profile.model_dump()
        del _validation["user_profile"]["hashed_token"]
        del _validation["user_profile"]["salt"]

        # security.credentials

    return _validation


def validate_platform_token(
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

    get_user_query = get_settings().dataplane_token

    _validation = {}
    if get_user_query != security.credentials:
        raise credentials_exception
        _validation["status"] = False
    else:
        _validation["status"] = True

    return _validation


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
