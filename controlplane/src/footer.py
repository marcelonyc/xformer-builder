import dash_bootstrap_components as dbc
from flask_login import current_user
from dash import html
from config.app_config import AppConfig

app_config = AppConfig()


def create_footer():

    return dbc.Navbar(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    "GitHub Repository",
                                    href="https://github.com/marcelonyc/xformer-builder",
                                    target="_blank",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "Author",
                                    href="https://www.linkedin.com/in/marcelolitovsky/",
                                    target="_blank",
                                )
                            ),
                        ],
                        className="ml-auto",
                        navbar=True,
                    ),
                    width=8,
                ),
                dbc.Col(
                    [
                        html.Div([""], id="logged-in-user-name"),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Div(
                            f"File Size Limit: {app_config.max_file_size} Bytes / Max Storage Size: {app_config.max_storage_size} Bytes"
                        ),
                    ]
                ),
            ]
        ),
        sticky="bottom",
    )
