# Import necessary libraries
from dash import (
    html,
    register_page,
)
import code_editor.editor as editor_utils
import dash_bootstrap_components as dbc
from auth.login_handler import require_login


register_page(__name__, name="Home", top_nav=True, path="/")


# Button to save code. Uses editor_element_index to identify editor


def layout(new_xformer: bool = True):

    title = html.H1("Onboard customer's data with ease")
    subtitle = html.H4(
        "Sample, transform, map and simplify you data exchanges"
    )
    getting_started = html.H3("Getting started")

    rows = []
    row_data = [
        {
            "number": "fa-solid fa-1 fa-xl",
            "class": "fa-solid fa-cash-register fa-xl",
            "href": "/register",
            "text": "Register for an Account. You will get a token to login.",
        },
        {
            "number": "fa-solid fa-2 fa-xl",
            "class": "fa-solid fa-arrow-right-arrow-left fa-xl",
            "href": "/xformer-builder",
            "text": "Create a transformer with a sample of "
            "the CSV/XLS file you want to transform.You can later "
            "associate one or more file uploads with this transformer.",
        },
        {
            "number": "fa-solid fa-3 fa-xl",
            "class": "fa-solid fa-pen-to-square fa-xl",
            "href": "/edit-xformer",
            "text": "Edit and existing transformer. "
            "Warning: This will overwrite the existing transformer and change future file uploads",
        },
        {
            "number": "fa-solid fa-4 fa-xl",
            "class": "fa-solid fa-link fa-xl",
            "href": "/associate-xformer",
            "text": "Associate a transformer with a file upload. "
            "This steps generates a unique URL for the file upload",
        },
        {
            "number": "fa-solid fa-5 fa-xl",
            "class": "fa-solid fa-share-from-square fa-xl",
            "href": "/",
            "text": "Share the unique URL with the user who will upload the file",
        },
        {
            "number": "fa-solid fa-6 fa-xl",
            "class": "fa-solid fa-download fa-xl",
            "href": "/download",
            "text": "When a user uploads a file, a unique URL will be generated for the file download. "
            "As an administrator you can also list the files available for download",
        },
    ]
    for row in row_data:
        rows.append(
            html.Tr(
                [
                    html.Td(
                        html.A(
                            html.I(className=row["number"]),
                            href=row["href"],
                        )
                    ),
                    html.Td(
                        html.A(
                            html.I(className=row["class"]),
                            href=row["href"],
                        )
                    ),
                    html.Td(row["text"]),
                ]
            )
        )

    table_body = [html.Tbody(rows)]

    table = html.Div(
        dbc.Table(
            table_body,
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
        ),
        style={"margin": "auto", "width": "80%"},
    )

    return dbc.Container(
        [title, subtitle, html.Hr(), getting_started, html.Br(), table],
        className="p-3 bg-body-secondary rounded-3",
        style={"margin": "20px", "width": "80%", "position": "center"},
    )
