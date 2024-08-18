from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse, Response, HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import service
from auth.models import RegisterUser, RegisterUserResponse
from secrets import token_bytes, token_hex, token_urlsafe
from sqlalchemy import insert, select, update, func
from database import database, users, xformer_store
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
    token_url: str = token_urlsafe(36)
    user_id: str = str(uuid.uuid4())
    insert_statement = (
        insert(users)
        .values(
            id=user_id,
            token=token_url,
            name=user.name,
            email=user.email,
            description=user.description,
        )
        .returning(users.c.token)
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
    return RegisterUserResponse(app_token=token_url)
