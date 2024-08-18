# Import necessary libraries
from dash import html, register_page, callback, dcc, State, Input, Output
import dash_bootstrap_components as dbc
import code_editor.editor as editor_utils
import base64
from flask import request
from config.app_config import AppConfig
from dataplane.dataplane import dataplane_post, dataplane_get

register_page(
    __name__,
    name="Upload File",
    top_nav=True,
    path_template="/upload/<association_id>",
)

app_config = AppConfig()

association_upload_id = "upload-association-data"
hidden_association_id = "hidden-association-id"
upload_modal = "upload-modal"


def layout(association_id: str = ""):

    _file_exists = dataplane_get(
        f"/association-exists/{association_id}", auth=False
    )
    if "exists" not in _file_exists:
        return html.Div("Fail to get file association")

    if not _file_exists["exists"]:
        return html.Div("File association not found")

    upload_modal_object = dbc.Modal(
        [
            dbc.ModalHeader("File Download URL"),
            dbc.ModalBody(
                id=f"{upload_modal}-body",
            ),
        ],
        id=f"{upload_modal}-modal",
        is_open=False,
    )
    upload_children = [
        "Upload CSV File. Max file size {}".format(app_config.max_file_size)
    ]
    upload_style = {
        "width": "100%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
    }
    sample_upload_widget = dcc.Upload(
        upload_children,
        id=association_upload_id,
        max_size=app_config.max_file_size,
        style=upload_style,
    )

    hidden_div = html.Div(
        association_id,
        id=hidden_association_id,
        hidden=True,
    )

    return html.Div([upload_modal_object, hidden_div, sample_upload_widget])


@callback(
    Output(f"{upload_modal}-body", "children"),
    Output(f"{upload_modal}-modal", "is_open"),
    Input(association_upload_id, "contents"),
    State(association_upload_id, "filename"),
    State(hidden_association_id, "children"),
    prevent_initial_call=True,
)
def upload_sample_data(contents, filename, association_id):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    files = {
        "file": (filename, decoded, "text/csv"),
    }
    headers = {"Filename": association_id}

    _api_response = dataplane_post(
        f"/upload/{association_id}", files=files, headers=headers, auth=False
    )

    if "upload_id" not in _api_response:
        return html.Div(f"Failed to upload file{_api_response}"), True

    modal_return = html.Div(
        [
            dbc.Label("Download URL"),
            dcc.Textarea(
                id="download-url-create-response-textarea",
                value=f"{request.host_url}download-direct/{association_id}/{_api_response['upload_id']}",
                style={"width": "100%"},
                readOnly=True,
            ),
            dbc.Label(
                "Copy to clipboard. You need this URL to download the file",
                class_name="text-warning",
            ),
            dcc.Clipboard(
                target_id="download-url-create-response-textarea",
                style={
                    "display": "inline-block",
                    "fontSize": 20,
                    "verticalAlign": "top",
                },
            ),
        ]
    )
    return modal_return, True
