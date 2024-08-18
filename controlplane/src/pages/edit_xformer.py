# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    register_page,
    callback,
    Output,
    Input,
)
import code_editor.editor as editor_utils
from auth.login_handler import require_login
from dataplane.dataplane import dataplane_get
from lib.models import XformerAllRows


register_page(
    __name__, name="Edit Transformer", path="/edit-xformer", top_nav=True
)
require_login(__name__)


# Button to save code. Uses editor_element_index to identify editor


def layout(status: str = None):

    _api_respose = dataplane_get("/list-xformer")

    all_xformers: XformerAllRows = XformerAllRows(**_api_respose)

    xformer_select_options = []
    for _xformer in all_xformers.rows:
        xformer_select_options.append(
            {"label": _xformer.name, "value": _xformer.name}
        )

    app_token_input = [
        dbc.Label(
            "Warning: changes will apply to future uploads of files associated with the transformer",
            color="danger",
            size="lg",
        ),
        html.P(),
        dbc.Label("Select Transformer to edit", html_for="xformer-select"),
        dbc.Select(
            id="xformer-name-select",
            options=xformer_select_options,
        ),
        html.Div(id="xformer-name-redirect"),
    ]

    form_layout = html.Form(app_token_input)

    login_form = html.Div(
        [
            form_layout,
        ],
        style={"padding": "20px"},
    )

    return html.Div([login_form])


@callback(
    Output("url", "href", allow_duplicate=True),
    Input("xformer-name-select", "value"),
    prevent_initial_call=True,
)
def update_xformer_name(xformer_name):
    if xformer_name:
        pathname = "/xformer-builder"
        params = {"new_xformer": False, "xformer_name": xformer_name}
        # Construct the full URL
        new_url = (
            f"{pathname}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        )
        return new_url
    else:
        pass
