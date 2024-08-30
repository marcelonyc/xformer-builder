from fastapi import (
    Depends,
    APIRouter,
    Request,
    status,
    HTTPException,
)
from fastapi.responses import StreamingResponse, JSONResponse
import filexchange.service as filexchange_service
import uuid
from streaming_form_data.targets import ValueTarget
from config.app_config import get_settings
from streaming_form_data import StreamingFormDataParser
from database import (
    database,
    file_xformer_association,
    file_manager,
)
import io
from sqlalchemy import select, func
from filexchange.service import process_file_status


from backgroundprovider.base import BackgroundProvider

# WARNING - These routes are not protected by the auth service
router = APIRouter()

backgroundprovider: BackgroundProvider = get_settings().backgroundprovider

MAX_FILE_SIZE = get_settings().max_file_size
MAX_REQUEST_BODY_SIZE = MAX_FILE_SIZE + 1024


class MaxBodySizeException(Exception):
    def __init__(self, body_len: str):
        self.body_len = body_len


class MaxBodySizeValidator:
    def __init__(self, max_size: int):
        self.body_len = 0
        self.max_size = max_size

    def __call__(self, chunk: bytes):
        self.body_len += len(chunk)
        if self.body_len > self.max_size:
            raise MaxBodySizeException(body_len=self.body_len)


@router.post(
    "/upload/{file_id}",
    dependencies=[
        Depends(filexchange_service.validate_file_id),
        Depends(filexchange_service.check_account_total_size),
    ],
)
async def upload_file(
    request: Request,
    background_tasks: backgroundprovider,
    file_id: str,
    # file_limit: dict = Depends(service.get_file_limits),
) -> JSONResponse:
    upload_id = str(uuid.uuid4())

    filename = request.headers.get("Filename")
    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)

    file_ = get_settings().filestoreprovider.Target(upload_id, file_id)
    data = ValueTarget()
    parser = StreamingFormDataParser(headers=request.headers)
    parser.register("file", file_)
    parser.register("data", data)
    try:
        async for chunk in request.stream():
            body_validator(chunk)
            parser.data_received(chunk)
    except MaxBodySizeException as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File is too large to upload. Limit is {}".format(
                MAX_FILE_SIZE
            ),
        )

    if not file_.multipart_filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is missing",
        )

    background_tasks.add_task(
        filexchange_service.process_file, file_id, upload_id, filename
    )

    call_url = request.url
    if call_url.port:
        call_url_port = f":{call_url.port}"
    else:
        call_url_port = ""

    return JSONResponse(
        content={
            "upload_id": upload_id,
            "url": f"{call_url.scheme}//{call_url.hostname}{call_url_port}/download/{file_id}/{upload_id}",
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/download/{file_id}/{upload_id}")
async def upload_file(
    request: Request,
    file_id: str,
    upload_id: str,
    # file_limit: dict = Depends(service.get_file_limits),
) -> StreamingResponse:

    try:
        file_df = get_settings().filestoreprovider.get_file(
            file_id, upload_id, True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    stream = io.StringIO()
    file_df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv"
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename={file_id}-{upload_id}.csv"
    )
    return response


@router.get("/download-latest/{file_id}")
async def upload_file(
    request: Request,
    file_id: str,
) -> StreamingResponse:

    # Get latest upload_id
    select_query = (
        select(file_manager.c.upload_id, func.max(file_manager.c.upload_date))
        .where(file_manager.c.file_id == file_id)
        .group_by(file_manager.c.file_id)
    )
    try:
        _upload_id = await database.fetch_all(select_query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    if len(_upload_id) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    upload_id = _upload_id[0]["upload_id"]
    file_df = get_settings().filestoreprovider.get_file(
        file_id, upload_id, True
    )
    stream = io.StringIO()
    file_df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv"
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename={file_id}-{upload_id}.csv"
    )
    return response


@router.get("/association-exists/{file_id}")
async def association_exists(file_id: str) -> JSONResponse:
    select_query = select(file_xformer_association).where(
        file_xformer_association.c.file_id == file_id
    )
    try:
        file_exists = await database.fetch_all(select_query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to locate file",
        )
    if len(file_exists) == 0:
        return JSONResponse(content={"exists": False})
    return JSONResponse(content={"exists": True})
