from typing import Annotated
from fastapi import Depends, APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import service
from lib.models import Xformer
from secrets import token_bytes, token_hex, token_urlsafe
from sqlalchemy import insert, select, update, func
from sqlalchemy.engine import CursorResult
from database import database, xformer_store, users
from auth.models import UserProfile
from pydantic import Field
import logging
import uuid
import json
from lib.json_utils import json_object_converter

router = APIRouter(dependencies=[Depends(service.validate_app_token)])


@router.post("/save-xformer")
async def save_xformer(request: Request, xformer: Xformer) -> JSONResponse:

    user_profile: UserProfile = request.state.user_profile
    if xformer.update:
        insert_statement: CursorResult = (
            update(xformer_store)
            .where(xformer_store.c.name == xformer.name)
            .where(xformer_store.c.user_id == user_profile.id)
            .values(
                description=xformer.description,
                xformer=json.loads(xformer.xformer.model_dump_json()),
            )
            .returning(xformer_store.c.id)
        )
    else:
        insert_statement: CursorResult = (
            insert(xformer_store)
            .values(
                id=str(uuid.uuid4()),
                name=xformer.name,
                user_id=user_profile.id,
                description=xformer.description,
                xformer=json.loads(xformer.xformer.model_dump_json()),
            )
            .returning(xformer_store.c.id)
        )

    xformer_id = "failed"

    try:
        insert_row = await database.execute(insert_statement)
        xformer_id = insert_row.fetchall()[0][0]
    except Exception as e:
        logging.error(
            f"Failed to save/update xformer: {xformer.name}. Actual error {str(e)}"
        )

    return JSONResponse({"status": str(xformer), "id": xformer_id})


@router.get("/list-xformer")
async def list_xformer(
    request: Request, xformer_name: str = "all"
) -> JSONResponse:

    select_statement = (
        select(
            xformer_store.c.id,
            xformer_store.c.name,
            xformer_store.c.description,
            xformer_store.c.xformer,
        )
        .join(users, xformer_store.c.user_id == users.c.id)
        .where(users.c.id == request.state.user_profile.id)
    )

    if xformer_name != "all":
        select_statement = select_statement.where(
            xformer_store.c.name == xformer_name
        ).where(xformer_store.c.user_id == request.state.user_profile.id)

    try:
        selected_rows = await database.fetch_all(select_statement)
    except Exception as e:
        logging.error(f"Failed to get xformers. Actual error {str(e)}")

    xformers_list = []
    for row in selected_rows:
        json_checked = json_object_converter(row)
        xformers_list.append(
            {key: json_checked[key] for key in json_checked.keys()}
        )
    return JSONResponse({"rows": xformers_list})
