# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import html, register_page, callback, Output, State, Input, dcc
import base64
from flask import request
import code_editor.editor as editor_utils
from auth.login_handler import require_login
from dataplane.dataplane import dataplane_get, dataplane_post
from lib.models import XformerAllRows


register_page(
    __name__,
    name="File/Transformer association",
    path="/associate-xformer",
    top_nav=True,
)
require_login(__name__)


# Button to save code. Uses editor_element_index to identify editor
xformer_select = "xformer-association-select"
xformer_description = "xformer-association-description"
columns_display = "xformer-association-columns"
source_columns_store = "source-columns-store"
target_columns_store = "target-columns-store"
generate_file_button = "generate-file-button"
code_store = "code-store"
association_modal = "association-modal"


def layout(status: str = None):

    _api_respose = dataplane_get("/list-xformer")

    all_xformers: XformerAllRows = XformerAllRows(**_api_respose)

    xformer_select_options = []
    xformer_source_columns = {}
    xformer_target_columns = {}
    xformer_code = {}
    for _xformer in all_xformers.rows:
        xformer_select_options.append(
            {"label": _xformer.name, "value": _xformer.id}
        )
        xformer_source_columns[_xformer.id] = _xformer.xformer.source_column
        xformer_target_columns[_xformer.id] = _xformer.xformer.target_column
        xformer_code[_xformer.id] = _xformer.xformer.code

    association_modal_object = dbc.Modal(
        [
            dbc.ModalHeader("File/Transformer Association links"),
            dbc.ModalBody(
                id=f"{association_modal}-body",
            ),
        ],
        id=f"{association_modal}-modal",
        is_open=False,
    )

    association_input = [
        dbc.Label(
            "This form returns a unique URL for each file. This URL can be used to upload the file. The file will be processed with the associated transformer.",
            color="normal",
            size="lg",
        ),
        html.P(),
        dbc.Button(
            "Generate File ID", color="primary", id=generate_file_button
        ),
        html.P(),
        dbc.Label("Select Transformer to associate", html_for=xformer_select),
        dbc.Select(
            id=xformer_select,
            options=xformer_select_options,
            required=True,
        ),
        dbc.Label("Description", html_for=xformer_select),
        dbc.Input(
            id=xformer_description,
            type="text",
            maxlength=100,
            required=True,
            placeholder="Something to remind you who uploads this file",
        ),
        html.Div(id=columns_display),
        dcc.Store(id=source_columns_store, data=xformer_source_columns),
        dcc.Store(id=target_columns_store, data=xformer_target_columns),
        dcc.Store(id=code_store, data=xformer_code),
        association_modal_object,
    ]

    # form_layout = html.Form(association_input)

    association_form = html.Div(
        association_input,
        style={"padding": "20px"},
    )

    return html.Div([association_form])


@callback(
    Output(columns_display, "children"),
    Input(xformer_select, "value"),
    State(source_columns_store, "data"),
    State(target_columns_store, "data"),
    State(code_store, "data"),
    prevent_initial_call=True,
)
def show_columns(selected, source_columns, target_columns, code):
    if selected:
        source_columns = source_columns[selected]
        target_columns = target_columns[selected]
        code_store = code[selected]
        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Source Column"),
                        html.Th("Target Columns"),
                        html.Th("Transformed"),
                    ]
                )
            )
        ]
        rows = []
        popovers = []
        for i in range(len(source_columns)):
            if code_store[i] is not None and code_store[i] != "":
                is_transformed = html.I(
                    id=f"{target_columns[i]}-code",
                    className="fa-solid fa-check",
                )
                popovers.append(
                    dbc.Popover(
                        [
                            dbc.PopoverHeader("Code"),
                            dbc.PopoverBody(
                                base64.b64decode(code_store[i]).decode(
                                    "utf-8"
                                ),
                                class_name="bg-secondary text-black",
                            ),
                        ],
                        id=f"{target_columns[i]}-popover",
                        target=f"{target_columns[i]}-code",
                        trigger="hover",
                    )
                )
            else:
                is_transformed = html.I(
                    className="fa-solid fa-x", style={"color": "#f20707"}
                )
            row = html.Tr(
                [
                    html.Td(source_columns[i]),
                    html.Td(target_columns[i]),
                    html.Td(is_transformed),
                ]
            )
            rows.append(row)

        table_body = [html.Tbody(rows)]

        table = [
            dbc.Table(table_header + table_body, bordered=True)
        ] + popovers
        return table
    else:
        return []


@callback(
    Output(f"{association_modal}-body", "children"),
    Output(f"{association_modal}-modal", "is_open"),
    Input(generate_file_button, "n_clicks"),
    State(xformer_description, "value"),
    State(xformer_select, "value"),
)
def save_association(n_clicks, description, xformer_id):
    if not n_clicks:
        return "", False

    _api_response = dataplane_post(
        "/file-association",
        data={
            "xformer_id": xformer_id,
            "description": description,
        },
    )
    if "file_id" not in _api_response:
        return (
            html.H2(
                "Failed to generate file association. Contact your platform administrator",
                className="text-danger",
            ),
            True,
        )
    else:

        return (
            html.Div(
                [
                    dbc.Label("Upload URL"),
                    dcc.Textarea(
                        id="upload-url-create-response-textarea",
                        value=f"{request.host_url}upload/{_api_response['file_id']}",
                        style={"width": "100%"},
                        readOnly=True,
                    ),
                    dbc.Label(
                        "Copy to clipboard. You need this URL to upload the file",
                        class_name="text-warning",
                    ),
                    dcc.Clipboard(
                        target_id="upload-url-create-response-textarea",
                        style={
                            "display": "inline-block",
                            "fontSize": 20,
                            "verticalAlign": "top",
                        },
                    ),
                ]
            ),
            True,
        )
