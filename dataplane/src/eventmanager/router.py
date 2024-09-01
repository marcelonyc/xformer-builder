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
    event_triggers,
)
from sqlalchemy import insert, select, func, update
from sqlalchemy.exc import IntegrityError
from lib.json_utils import json_object_converter
from lib.models import (
    EmailEventMetadata,
    EventTriggerList,
    EventTriggerPayload,
    WebhookEventMetadata,
)
import json
from typing import Annotated
from config.app_config import get_settings
from eventmanager.service import invoke_webhook_event

router = APIRouter(dependencies=[Depends(service.validate_app_token)])


@router.post("/save-event-trigger/webhook")
async def associate_file_with_xformer(
    request: Request,
    eventtrigger: WebhookEventMetadata,
    test_on_save: bool = False,
) -> JSONResponse:

    if test_on_save:
        try:
            _event_response = invoke_webhook_event(
                eventtrigger, payload={"Test": "Test"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to invoke webhook event: {e}",
            )

        if not _event_response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to invoke webhook event: {_event_response['message']}",
            )

    select_statement = (
        select(event_triggers.c.id)
        .where(event_triggers.c.id == eventtrigger.id)
        .where(event_triggers.c.user_id == request.state.user_profile.id)
    )
    try:
        _event_trigger = await database.fetch_all(select_statement)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to get event trigger from DB",
        )
    _update = False
    if len(_event_trigger) > 0:
        trigger_id = _event_trigger[0]["id"]
        _update = True
    else:
        trigger_id = eventtrigger.id

    if not _update:
        dml_statement = insert(event_triggers).values(
            id=trigger_id,
            user_id=request.state.user_profile.id,
            event_description=eventtrigger.event_description,
            event_type="webhook",
            event_meta=json.loads(eventtrigger.model_dump_json()),
        )
    else:
        dml_statement = (
            update(event_triggers)
            .values(
                event_description=eventtrigger.event_description,
                event_meta=json.loads(eventtrigger.model_dump_json()),
            )
            .where(event_triggers.c.id == trigger_id)
        )
    try:
        await database.execute(dml_statement)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Association already exists {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to save event trigger",
        )
    return JSONResponse(
        content={"trigger_id": trigger_id},
        status_code=status.HTTP_200_OK,
    )


@router.get("/list-event-triggers")
async def get_list_of_uploaded_files(
    request: Request,
) -> EventTriggerList:
    user_id = request.state.user_profile.id

    select_statement = select(
        event_triggers.c.id,
        event_triggers.c.user_id,
        event_triggers.c.event_description,
        event_triggers.c.event_type,
        event_triggers.c.event_meta,
    ).where(event_triggers.c.user_id == user_id)
    try:
        _triggers = await database.fetch_all(select_statement)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files not found",
        )

    if len(_triggers) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No triggers found",
        )

    _triggers_response = []
    for trigger in _triggers:
        _triggers_response.append(json_object_converter(trigger))

    triggers = EventTriggerList(triggers=_triggers_response)

    return triggers
