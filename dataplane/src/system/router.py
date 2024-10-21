from fastapi import (
    Depends,
    APIRouter,
    Request,
    status,
    HTTPException,
)
from fastapi.responses import Response, JSONResponse
from datetime import datetime, timedelta
from auth import service
from system.service import delete_expired_files
import os
import uuid
from streaming_form_data.targets import ValueTarget
from backgroundprovider.base import BackgroundProvider
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
from config.app_config import get_settings


from backgroundprovider.base import BackgroundProvider

router = APIRouter(dependencies=[Depends(service.validate_platform_token)])


backgroundprovider: BackgroundProvider = get_settings().backgroundprovider


@router.get("/delete-expired-files")
async def get_list_of_uploaded_files(
    request: Request,
    background_tasks: backgroundprovider,
) -> JSONResponse:

    hours_to_expire = get_settings().file_ttl
    delete_older_than = datetime.now() - timedelta(hours=hours_to_expire)
    select_statement = select(
        file_manager.c.file_id,
        file_manager.c.upload_id,
        file_manager.c.file_size,
        file_manager.c.upload_date,
        file_manager.c.last_update_message,
    ).where(file_manager.c.upload_date < delete_older_than)
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

    background_tasks.add_task(delete_expired_files, _files_response)

    return JSONResponse(
        content={"files": _files_response},
        status_code=status.HTTP_200_OK,
    )
