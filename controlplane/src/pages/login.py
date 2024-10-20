# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    register_page,
)
import code_editor.editor as editor_utils
from config.app_config import get_settings


register_page(__name__, name="Login", top_nav=True)

app_config = get_settings()


# Button to save code. Uses editor_element_index to identify editor


def layout(status: str = None, **kwargs):

    placeholder = "Enter your Application Token"
    if status == "invalid_token":
        placeholder = "INVALID TOKEN. Enter your Application Token"

    if app_config.smtp_enabled:
        enable_token_recovery = dbc.NavLink(
                    "Forgot your token? Click here to reset it",
                    href="/forgot_token",
                    target="_blank",
                )
    else:
        enable_token_recovery = html.Div()
        
    app_token_input = [
        dbc.Label("Application Token", html_for="app-token"),
        dbc.Input(
            id="app-token",
            type="text",
            maxLength=48,
            name="app_token",
            placeholder=placeholder,
        ),
        dbc.FormText(
            [
                dbc.NavLink(
                    "Enter your Application Token. If you are not registered, click here to register",
                    href="/register",
                    target="_blank",
                ),
                enable_token_recovery,
            ],
            color="secondary",
        ),
    ]
    login_button_input = [
        dbc.Button(
            children="Login",
            n_clicks=0,
            id="login-button",
            type="submit",
            color="primary",
        ),
    ]

    form_layout = html.Form(
        app_token_input
        + login_button_input
        + [html.Div(children="", id="output-state")],
        method="POST",
    )

    login_form = html.Div(
        [
            form_layout,
        ],
        style={"padding": "20px"},
        id="xformers-editor-div",
    )

    return html.Div([login_form])
