from fastapi import (
    Depends,
    APIRouter,
    Request,
    status,
    HTTPException,
)
from fastapi.responses import JSONResponse
from auth import service

from lib.models import (
    XformerAssociationPayload,
)


router = APIRouter(dependencies=[Depends(service.validate_app_token)])


@router.post("/save-function")
async def save_custom_function(
    request: Request, association: XformerAssociationPayload
) -> JSONResponse:

    invalid_xformer_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid transformer",
    )
