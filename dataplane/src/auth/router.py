from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse, Response, HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import service
from pydantic import EmailStr
from auth.models import RegisterUser, RegisterUserResponse
from secrets import token_bytes, token_hex, token_urlsafe
from sqlalchemy import insert, select, update, func, delete
from database import database, users, xformer_store, password_reset
from config.app_config import get_settings
from auth.utils import TokenManager
import logging
import uuid
from backgroundprovider.base import BackgroundProvider


router = APIRouter()

backgroundprovider: BackgroundProvider = get_settings().backgroundprovider


@router.get("/login")
def login_user_with_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(service.validate_app_token)
    ]
):
    security = credentials
    return security


@router.post("/register")
async def register_user(user: RegisterUser) -> RegisterUserResponse:

    token_manager = TokenManager()
    user_data = token_manager.generate_user_data()

    # TODO: Check if email verification is required
    _is_email_verification_required = get_settings().require_email_verification
    insert_statement = (
        insert(users)
        .values(
            id=user_data.id,
            username=user_data.id,
            salt=user_data.salt,
            hashed_token=user_data.hashed_token,
            name=user.name,
            email=user.email,
            description=user.description,
        )
        .returning(users.c.id)
    )
    try:
        await database.execute(insert_statement)
    except Exception as e:
        # logging.error(
        #     f"Account already exists: {user.name}. Actual error {str(e)}"
        # )
        return HTMLResponse(
            content="Account already exists. Please login",
            status_code=400,
        )
    return RegisterUserResponse(app_token=user_data.token)


@router.post("/token-reset-request")
async def reset_password(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(service.validate_platform_token)
    ],
    background_tasks: backgroundprovider,
    email: EmailStr,
) -> JSONResponse:

    background_tasks.add_task(service.send_token_reset_email, email)

    return JSONResponse(content="Password reset")


@router.post("/token-reset/{reset_code}")
async def reset_password(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(service.validate_platform_token)
    ],
    reset_code: str,
) -> JSONResponse:

    select_token = (
        select(password_reset)
        .where(password_reset.c.reset_code == reset_code)
        .where(password_reset.c.expires_at > func.now())
    )

    try:
        token_result = await database.fetch_all(select_token)
    except Exception as e:
        return JSONResponse(content="Token reset failed. Invalid token")

    if len(token_result) == 0:
        return JSONResponse(
            content="Password reset failed. Invalid token provided"
        )

    select_user = select(users).where(
        users.c.email == token_result[0]["email"]
    )
    try:
        user_record = await database.fetch_all(select_user)
        user_record = user_record[0]
    except Exception as e:
        return JSONResponse(
            content="Password reset failed. Failed to get user"
        )

    if len(user_record) == 0:
        return JSONResponse(
            content="Password reset failed. User does not exist"
        )

    token_manager = TokenManager()
    user_data = token_manager.generate_user_data()

    # TODO: Check if email verification is required
    update_statement = (
        update(users)
        .values(
            username=user_data.id,
            salt=user_data.salt,
            hashed_token=user_data.hashed_token,
        )
        .where(users.c.email == token_result[0]["email"])
    )
    try:
        await database.execute(update_statement)
    except Exception as e:
        return JSONResponse(
            content=f"Failed to update account {str(e)}",
            status_code=400,
        )

    delete_token = delete(password_reset).where(
        password_reset.c.reset_code == reset_code
    )
    try:
        delete_token = await database.execute(delete_token)
    except Exception as e:
        pass

    return RegisterUserResponse(app_token=user_data.token)
