# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    register_page,
    callback,
    Output,
    State,
    dcc,
    Input,
)
import json
from flask import session
from pydantic import EmailStr, BaseModel, ValidationError
from dataplane.dataplane import dataplane_post


register_page(__name__, name="Register", top_nav=True)


# Button to save code. Uses editor_element_index to identify editor


register_input_name = "register-input-name"
register_input_email = "register-input-email"
register_input_description = "register-input-description"


register_modal = "register-modal"


def layout(status: str = None):

    register_modal_object = dbc.Modal(
        [
            dbc.ModalHeader("Registration"),
            dbc.ModalBody(
                id=f"{register_modal}-body",
            ),
        ],
        id=f"{register_modal}-modal",
        is_open=False,
    )
    register_input = [
        dbc.Label("Full Name *", html_for=register_input_name),
        dbc.Input(
            id=register_input_name,
            type="text",
            required=True,
            maxLength=48,
            name="name",
            placeholder="Full Name",
        ),
        dbc.Label("Email *", html_for=register_input_name),
        dbc.Input(
            id=register_input_email,
            type="email",
            required=True,
            inputmode="email",
            maxLength=48,
            name="name",
            placeholder="Email",
        ),
        dbc.Label("Tell us about you *", html_for=register_input_name),
        dbc.Textarea(
            id=register_input_description,
            maxlength=360,
            name="description",
            required=True,
        ),
    ]

    register_button_input = [
        dbc.Button(
            children="Register",
            id="register-button",
            color="primary",
        ),
    ]

    form_layout = dbc.Form(
        register_input
        + register_button_input
        + [
            "* indicates required fields",
        ]
        + [
            dbc.Label(id="registered-output-state", children=""),
            register_modal_object,
        ],
    )
    # form_layout = html.Div(register_input + register_button_input)
    register_form = html.Div(
        [
            form_layout,
        ],
        style={"padding": "20px"},
        id="xformers-editor-div",
    )

    return html.Div([register_form])


@callback(
    Output("registered-output-state", "children"),
    Output(f"{register_modal}-body", "children"),
    Output(f"{register_modal}-modal", "is_open"),
    Input("register-button", "n_clicks"),
    State(register_input_name, "value"),
    State(register_input_email, "value"),
    State(register_input_description, "value"),
)
def register_user(n_clicks, name, email, description):

    class EntryModel(BaseModel):
        name: str
        email: EmailStr

    _is_valid = False

    if n_clicks:
        try:
            EntryModel(name=name, email=email)
            _is_valid = True
        except ValidationError as e:
            return "Invalid Input", "", False

        _api_response = dataplane_post(
            "/register",
            data={
                "name": name,
                "email": email,
                "description": description,
            },
            auth=False,
        )

        if "app_token" not in _api_response:
            return (
                "",
                html.H1(
                    "Failed to register user. Contact your platform administrator",
                    className="text-danger",
                ),
                True,
            )
        else:

            return (
                "Registered",
                html.Div(
                    [
                        dbc.Label("App Token"),
                        dcc.Textarea(
                            id="app-token-create-response-textarea",
                            value=_api_response["app_token"],
                            style={"width": "100%"},
                            readOnly=True,
                        ),
                        dbc.Label(
                            "Copy to clipboard. You need this token to access the application ",
                            class_name="text-warning",
                        ),
                        dcc.Clipboard(
                            target_id="app-token-create-response-textarea",
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
    return "", "", False
