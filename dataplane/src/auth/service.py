from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer
from typing import Annotated
import datetime
from database import database, users, xformer_store, password_reset
from auth.models import (
    RegisterUser,
    UserInDB,
    UserProfile,
    TokenData,
    Token,
    User,
)
import os
from secrets import token_urlsafe

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
        _validation["status"] = False
    else:
        _validation["status"] = True

    return _validation


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def send_token_reset_email(email: str):

    select_query = select(users).where(users.c.email == email)
    try:
        user = await database.fetch_all(select_query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if len(user) == 0:
        return

    reset_code = token_urlsafe(65)

    insert_statement = (
        insert(password_reset)
        .values(
            email=email,
            reset_code=reset_code,
            expires_at=datetime.datetime.now() + datetime.timedelta(hours=12),
        )
        .returning(password_reset.c.email)
    )
    try:
        await database.execute(insert_statement)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error sending email",
        )

    emailprovider = get_settings().emailprovider
    controlplane_url = get_settings().controlplane_url
    site_name = get_settings().APP_TITLE

    emailprovider.send_email(
        to=email,
        subject="{}: Token reset request".format(site_name),
        body=f"{site_name}\nClick here to reset your password: {controlplane_url}/reset_token/{reset_code}\n"
        "This link will expire in 12 hours",
    )

    return reset_code
