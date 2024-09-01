# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    register_page,
    callback,
    Output,
    State,
    Input,
    dcc,
    Patch,
    ALL,
)
import base64
from pydantic import AnyUrl
import uuid
import json
from flask import request
import code_editor.editor as editor_utils
from auth.login_handler import require_login
from dataplane.dataplane import dataplane_get, dataplane_post
from lib.models import (
    EventTriggerList,
    EventTriggerPayload,
    EventTriggerTypes,
    WebhookEventMetadata,
)
from config.app_config import get_settings


register_page(
    __name__,
    name="Event Triggers Management",
    path="/event-triggers",
    top_nav=True,
)
require_login(__name__)


# Button to save code. Uses editor_element_index to identify editor
event_trigger_select = "event-trigger-select"
event_trigger_form_div = "event-trigger-form-div"
event_type_select = "event-type-select"
webhooks_input = "webhooks-input"
webhook_body = "webhook-body"
webhook_headers = "webhook-headers"
webhook_method = "webhook-method"
webhook_url = "webhook-url"
webhook_headers_div = "webhook-headers-div"
webhook_add_header_button = "webhook-add-header-button"
webhook_header_key = "webhook-header-key"
webhook_header_value = "webhook-header-value"
form_style = {
    "border": "2px",
    "border-style": "solid",
    "border-color": "black",
}
existing_trigger_id = "existing-trigger-id"
save_event_trigger_button = "save-event-trigger"
event_trigger_status_div = "event-trigger-status"
all_triggers_store = "all-triggers-store"
event_trigger_description = "event-trigger-description"
event_trigger_assign_to = "event-trigger-assign-to"
failed_event_trigger = "event-trigger-failed-event-trigger"
success_event_trigger = "event-trigger-success-event-trigger"
columns_display = "event-trigger-columns"
source_columns_store = "source-columns-store"
target_columns_store = "target-columns-store"
generate_file_button = "generate-file-button"
code_store = "code-store"
association_modal = "modal"


def layout():

    _api_respose = dataplane_get("/list-event-triggers")

    trigger_select_options = []

    trigger_store = None
    if _api_respose.get("triggers"):
        all_triggers: EventTriggerList = EventTriggerList(**_api_respose)

        for _trigger in all_triggers.triggers:
            trigger_select_options.append(
                {"label": _trigger.event_description, "value": _trigger.id}
            )
        trigger_store = dcc.Store(
            id=all_triggers_store, data=all_triggers.model_dump()
        )

    select_existing_input = [
        dbc.Label(
            "Create new or select Event Trigger to modify (if any exists)",
            html_for=event_trigger_select,
        ),
        dbc.Select(
            id=event_trigger_select,
            options=trigger_select_options,
            required=False,
        ),
        trigger_store,
        dbc.Input(id=existing_trigger_id, type="hidden"),
    ]

    _event_types = list(EventTriggerTypes)
    _event_type_selection = []
    _event_type_selection.append(
        {
            "label": "None",
            "value": None,
        }
    )
    for i in range(len(_event_types)):
        _event_type_selection.append(
            {
                "label": _event_types[i].value.capitalize(),
                "value": _event_types[i].value,
            }
        )

    general_edit_trigger_input = [
        html.Div(id="event-trigger-status"),
        dbc.Label("Description"),
        dbc.Input(
            id=event_trigger_description,
            type="text",
            maxlength=100,
            required=True,
            placeholder="How will this event be used?",
        ),
        dbc.Label("Event Type"),
        dbc.Select(
            id=event_type_select,
            options=_event_type_selection,
            required=True,
        ),
        html.P(),
    ]

    webhooks_input_div = [
        html.Div(
            [
                dbc.Label("Webhook URL"),
                dbc.Input(
                    id=webhook_url,
                    type="url",
                    placeholder=f"Enter webhook URL. Allowed domains: {get_settings().webhook_domain_whitelist}",
                    required=True,
                ),
                dbc.Label("Method"),
                dbc.Select(
                    id=webhook_method,
                    options=[
                        {"label": "GET", "value": "GET"},
                        {"label": "POST", "value": "POST"},
                        {"label": "PUT", "value": "PUT"},
                        {"label": "DELETE", "value": "DELETE"},
                    ],
                ),
                dbc.Label("Headers"),
                html.P(),
                dbc.Button(
                    "Add Header",
                    id=webhook_add_header_button,
                    color="primary",
                    n_clicks=0,
                ),
                html.Div(
                    id=webhook_headers_div,
                    style={
                        "padding": "10px",
                        "margin": "10px",
                        "border": "1px solid black",
                        "border-radius": "5px",
                    },
                ),
                dbc.Label("Body"),
                dbc.Input(
                    id=webhook_body,
                    type="text",
                    placeholder="Enter additional text to add to payload",
                    required=False,
                ),
            ],
            id=webhooks_input,
            hidden=True,
        )
    ]

    save_trigger = [
        dbc.Button(
            "Save Event Trigger",
            id=save_event_trigger_button,
            color="secondary",
            style={"margin-top": "20px"},
        )
    ]

    event_trigger_form = dbc.Form(
        select_existing_input
        + general_edit_trigger_input
        + webhooks_input_div
        + save_trigger,
        style={"padding": "20px"},
    )

    return html.Div(
        [event_trigger_form], id=event_trigger_form_div, style=form_style
    )


@callback(
    Output(webhooks_input, "hidden"),
    Input(event_type_select, "value"),
    prevent_initial_call=True,
)
def show_webhooks_input(trigger_type):
    if trigger_type == "webhook":
        return False
    return True


@callback(
    Output(webhook_headers_div, "children", allow_duplicate=True),
    Input(webhook_add_header_button, "n_clicks"),
    State({"type": webhook_header_key, "index": ALL}, "value"),
    prevent_initial_call=True,
)
def add_header_input(n_clicks, header_keys):
    header_div_patched = Patch()
    new_index = len(header_keys)
    new_input = dbc.Row(
        [
            dbc.Col(
                dbc.Input(
                    id={
                        "type": webhook_header_key,
                        "index": new_index,
                    },
                    type="text",
                    placeholder="Header Key",
                )
            ),
            dbc.Col(
                dbc.Input(
                    id={
                        "type": webhook_header_value,
                        "index": new_index,
                    },
                    type="text",
                    placeholder="Header Value",
                )
            ),
        ]
    )

    header_div_patched.append(new_input)

    return header_div_patched


@callback(
    Output(event_trigger_status_div, "children"),
    Output(event_trigger_form_div, "style"),
    Input(save_event_trigger_button, "n_clicks"),
    State(event_trigger_description, "value"),
    State(event_type_select, "value"),
    State(webhook_url, "value"),
    State(webhook_method, "value"),
    State(webhook_body, "value"),
    State({"type": webhook_header_key, "index": ALL}, "value"),
    State({"type": webhook_header_value, "index": ALL}, "value"),
    State(existing_trigger_id, "value"),
    prevent_initial_call=True,
)
def save_event_trigger(
    n_clicks,
    description,
    event_type,
    url,
    method,
    body,
    header_keys,
    header_values,
    existing_trigger_id,
):
    try:
        _url = AnyUrl(url)
    except Exception as e:
        form_style["border-color"] = "red"
        return (
            html.Div(
                [
                    html.P("Failed to save Event Trigger"),
                    html.P("Error: " + str(e)),
                ],
                style={"color": "red"},
            ),
            form_style,
        )
    if _url.host not in get_settings().webhook_domain_whitelist:
        form_style["border-color"] = "red"
        return (
            html.Div(
                [
                    html.P("Failed to save Event Trigger"),
                    html.P("Error: URL is not in the list of accepted hosts"),
                ],
                style={"color": "red"},
            ),
            form_style,
        )

    headers = {}
    for i in range(len(header_keys)):
        headers[header_keys[i]] = header_values[i]

    try:
        if existing_trigger_id:
            _trigger_id = existing_trigger_id
        else:
            _trigger_id = str(uuid.uuid4())

        _event_trigger = WebhookEventMetadata(
            id=_trigger_id,
            event_description=description,
            event_type=event_type,
            url=str(url),
            method=method,
            headers=headers,
            body=body,
        )
    except Exception as e:
        form_style["border-color"] = "red"
        return (
            html.Div(
                [
                    html.P("Failed to save Event Trigger"),
                    html.P("Error: " + str(e)),
                ],
                style={"color": "red"},
            ),
            form_style,
        )
    _api_response = dataplane_post(
        "/save-event-trigger/webhook",
        json.loads(_event_trigger.model_dump_json()),
    )

    if _api_response.get("trigger_id"):
        form_style["border-color"] = "green"
        return (
            html.Div(
                [
                    html.P("Event Trigger saved successfully"),
                    html.P("Event Trigger ID: " + _api_response["trigger_id"]),
                ],
                style={"color": "green"},
            ),
            form_style,
        )
    else:
        form_style["border-color"] = "red"
        return (
            html.Div(
                [
                    html.P("Failed to save Event Trigger"),
                    html.P("Error: " + _api_response["error"]),
                ],
                style={"color": "red"},
            ),
            form_style,
        )


@callback(
    Output(event_trigger_description, "value"),
    Output(event_type_select, "value"),
    Output(existing_trigger_id, "value"),
    Output(webhook_url, "value"),
    Output(webhook_method, "value"),
    Output(webhook_body, "value"),
    Output(webhook_headers_div, "children", allow_duplicate=True),
    Input(event_trigger_select, "value"),
    State(all_triggers_store, "data"),
    prevent_initial_call=True,
)
def load_event_trigger(trigger_id, all_triggers):
    if not trigger_id:
        return [None] * 8

    all_triggers = EventTriggerList(**all_triggers)

    for _trigger in all_triggers.triggers:
        if _trigger.id == trigger_id:
            _event_trigger = _trigger.event_meta
            break

    _event_trigger = WebhookEventMetadata(**_event_trigger)

    header_div_patched = Patch()
    _index_counter = 0
    for key, value in _event_trigger.headers.items():
        new_input = dbc.Row(
            [
                dbc.Col(
                    dbc.Input(
                        id={
                            "type": webhook_header_key,
                            "index": _index_counter,
                        },
                        type="text",
                        value=key,
                    )
                ),
                dbc.Col(
                    dbc.Input(
                        id={
                            "type": webhook_header_value,
                            "index": _index_counter,
                        },
                        type="text",
                        value=value,
                    )
                ),
            ]
        )

        header_div_patched.append(new_input)
        _index_counter += 1

    return (
        _event_trigger.event_description,
        _event_trigger.event_type,
        _event_trigger.id,
        str(_event_trigger.url),
        _event_trigger.method,
        _event_trigger.body,
        header_div_patched,
    )
