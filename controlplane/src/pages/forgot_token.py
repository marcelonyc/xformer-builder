# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    register_page,
    callback,
    Output,
    Input,
    State,
)
from dataplane.dataplane import dataplane_platform_post
import code_editor.editor as editor_utils
from pydantic import EmailStr, BaseModel, ValidationError


register_page(
    __name__, name="Forgot Token", path="/forgot_token", top_nav=True
)


# Button to save code. Uses editor_element_index to identify editor

object_prefix = "reset-token"


def layout(status: str = None):

    placeholder = "Enter the email address you used to register"

    app_token_input = [
        dbc.Label("Email", html_for=f"{object_prefix}-app-email"),
        dbc.Input(
            id=f"{object_prefix}-app-email",
            type="email",
            maxLength=48,
            placeholder=placeholder,
        ),
        dbc.FormText(
            "If the email is registered, a link to reset the token will be sent to you.",
            color="secondary",
        ),
    ]
    login_button_input = [
        dbc.Button(
            children="Submit",
            n_clicks=0,
            id=f"{object_prefix}-button",
            type="submit",
            color="primary",
        ),
    ]

    form_layout = html.Div(
        app_token_input
        + login_button_input
        + [html.Div(children="", id=f"{object_prefix}-output-state")]
    )

    login_form = html.Div(
        [
            form_layout,
        ],
        style={"padding": "20px"},
    )

    return html.Div([login_form])


@callback(
    Output(f"{object_prefix}-output-state", "children"),
    Output(f"{object_prefix}-button", "disabled"),
    Output(f"{object_prefix}-app-email", "disabled"),
    Input(f"{object_prefix}-button", "n_clicks"),
    State(f"{object_prefix}-app-email", "value"),
)
def reset_token(n_clicks, email):
    if n_clicks == 0:
        return "", False, False

    try:

        class Email(BaseModel):
            email: EmailStr

        valid_email = Email(email=email)
    except ValidationError as e:
        return (
            dbc.Alert("Invalid email address", color="danger"),
            False,
            False,
        )
    response = dataplane_platform_post(
        endpoint="/token-reset-request?email={}".format(email),
    )

    reset_message = dbc.Alert(
        "Token reset email sent to {}".format(email),
        color="success",
    )

    return reset_message, True, True
