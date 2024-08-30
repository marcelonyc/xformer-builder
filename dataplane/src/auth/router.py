from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse, Response, HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import service
from auth.models import RegisterUser, RegisterUserResponse
from secrets import token_bytes, token_hex, token_urlsafe
from sqlalchemy import insert, select, update, func
from database import database, users, xformer_store
from config.app_config import get_settings
from auth.utils import TokenManager
import logging
import uuid

router = APIRouter()


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
