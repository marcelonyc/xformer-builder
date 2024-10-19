from lib.models import WebhookEventMetadata, EventTriggerResponse
import requests
from database import database, event_triggers
from sqlalchemy.sql import select
import json


def get_event_trigger_by_id(event_id: str = None) -> EventTriggerResponse:
    if event_id is None:
        return None

    select_query = select(event_triggers).where(
        event_triggers.c.id == event_id
    )
    try:
        _event_trigger = database.fetch_all_sync(select_query)
    except Exception as e:
        return None

    return EventTriggerResponse(**_event_trigger[0])


def invoke_webhook_event(
    eventtrigger: WebhookEventMetadata, payload: dict = {}
) -> dict:
    """
    This function is responsible for invoking the webhook event.
    :param eventtrigger: WebhookEventMetadata
    :param payload: dict
    :return: None
    """
    _invoke_success = False
    response_text = ""
    payload["body"] = eventtrigger.body
    try:
        response = requests.request(
            method=eventtrigger.method,
            url=eventtrigger.url,
            headers=eventtrigger.headers,
            json=payload,
        )
        _invoke_success = True
        response_text = response.text
    except requests.exceptions.RequestException as e:
        response_text = f"Error while invoking webhook event: {e}"
    except Exception as e:
        response_text = f"Error while invoking webhook event: {e}"

    return {"success": _invoke_success, "message": response_text}


class EventTriggerInvoke:

    def __init__(
        self, success_trigger_id: str = None, failed_trigger_id: str = None
    ):
        self.success_trigger_id = success_trigger_id
        self.failed_trigger_id = failed_trigger_id

    def send_success_trigger(self, payload: dict = {}):
        # Success trigger
        _sucess_trigger_meta = get_event_trigger_by_id(self.success_trigger_id)

        if _sucess_trigger_meta is None:
            return
        
        if _sucess_trigger_meta.event_type == "webhook":
            _payload = WebhookEventMetadata(**_sucess_trigger_meta.event_meta)
            invoke_webhook_event(_payload, payload)


    def send_failed_trigger(self, payload: dict = {}):
        _failed_trigger_meta = get_event_trigger_by_id(self.failed_trigger_id)
        
        if _failed_trigger_meta is None:
            return
        
        if _failed_trigger_meta.event_type == "webhook":
            _payload = WebhookEventMetadata(**_failed_trigger_meta.event_meta)
            invoke_webhook_event(_payload, payload)

