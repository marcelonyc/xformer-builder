from fastapi import (
    Depends,
    APIRouter,
    Request,
    status,
    HTTPException,
)
from fastapi.responses import Response, JSONResponse
from auth import service
import filemanager.service as filemanager_service
import os
import uuid
from streaming_form_data.targets import ValueTarget

from streaming_form_data import StreamingFormDataParser
from database import (
    database,
    file_xformer_association,
    xformer_store,
    file_manager,
)
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError
from lib.json_utils import json_object_converter
from lib.models import (
    XformerAssociationResponse,
    XformerAssociationPayload,
    ListUploadedFilesResponse,
)
import json
from typing import Annotated

from config.app_config import get_settings


from backgroundprovider.base import BackgroundProvider

router = APIRouter(dependencies=[Depends(service.validate_app_token)])


@router.post("/file-association")
async def associate_file_with_xformer(
    request: Request, association: XformerAssociationPayload
) -> JSONResponse:

    invalid_xformer_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid transformer",
    )
    select_statement = (
        select(xformer_store.c.id)
        .where(xformer_store.c.id == association.xformer_id)
        .where(xformer_store.c.user_id == request.state.user_profile.id)
    )
    try:
        _is_xformer_valid = await database.fetch_all(select_statement)
    except Exception as e:
        raise invalid_xformer_exception

    if len(_is_xformer_valid) == 0:
        raise invalid_xformer_exception

    xformer_id = _is_xformer_valid[0]["id"]
    file_id = f"{str(uuid.uuid4()).replace('-', '')}{str(uuid.uuid4()).replace('-', '')}"
    insert_statement = (
        insert(file_xformer_association)
        .values(
            file_id=file_id,
            xformer_id=xformer_id,
            description=association.description,
            user_id=request.state.user_profile.id,
        )
        .returning(file_xformer_association.c.file_id)
    )
    try:
        await database.execute(insert_statement)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Association already exists {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File association failed",
        )
    return JSONResponse(
        content={"file_id": file_id},
        status_code=status.HTTP_200_OK,
    )


@router.get("/list-uploaded-files")
async def get_list_of_uploaded_files(
    request: Request,
) -> ListUploadedFilesResponse:
    user_id = request.state.user_profile.id

    select_statement = (
        select(
            file_manager.c.file_id,
            file_manager.c.upload_id,
            file_manager.c.file_size,
            file_manager.c.upload_date,
            file_manager.c.last_update_message,
            file_xformer_association.c.description,
        )
        .where(file_manager.c.user_id == user_id)
        .join(
            file_xformer_association,
            file_xformer_association.c.file_id == file_manager.c.file_id,
        )
    )
    try:
        _files = await database.fetch_all(select_statement)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files not found",
        )

    if len(_files) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files not found",
        )

    _files_response = []
    for file in _files:
        _files_response.append(json_object_converter(file))

    files = ListUploadedFilesResponse(files=_files_response)

    for _file_update in range(len((files.files))):
        files.files[_file_update].file_ttl = get_settings().file_ttl
        files.files[_file_update].update_expiration()

    return files
