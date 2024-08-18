from dash import html
import dash_bootstrap_components as dbc

editor_close_button = "close-editor-button"
editor_test_button = "test-button"


def editor_div(
    editor_div: str,
    editor_modal: str,
    editor_title: str = "Code Editor",
    editor_test_button: str = "test-button",
    editor_close_button: str = "close-editor-button",
):
    """
    Creates a code editor div component.

    Args:
        editor_div (str): The id of the editor div.
        editor_modal (str): The id of the editor modal.
        editor_title (str, optional): The title of the code editor. Defaults to "Code Editor".
        editor_test_button (str, optional): The id of the test button. Defaults to "test-button".
        editor_close_button (str, optional): The id of the close button. Defaults to "close-editor-button".

    Returns:
        html.Div: The code editor div component.
    """

    button_style = {
        "width": "100%",
        "zIndex": "1000",
    }
    return html.Div(
        [
            dbc.Row(dbc.Col(html.H2(editor_title, id="editor-title"))),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        "pass",
                        id=editor_div,
                        style={
                            "width": "100%",
                            "height": "150px",
                            "border": "1px solid green",
                            "zIndex": "1000",
                        },
                    )
                ),
                justify="left",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Close",
                            id=editor_close_button,
                            style=button_style,
                        ),
                        align="left",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Test",
                            id=editor_test_button,
                            style=button_style,
                        ),
                        align="left",
                    ),
                ],
            ),
        ],
        id=editor_modal,
        hidden=True,
        className="bg-light border-success",
        style={
            "width": "50%",
            "margin": "auto",
            "padding": "20px",
            "position": "sticky",
            "top": "0",
            "zIndex": "1000",
            "border": "10px",
        },
    )
