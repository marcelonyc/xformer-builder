import dash_bootstrap_components as dbc
from flask_login import current_user
from dash import html
from config.app_config import get_settings

app_config = get_settings()


def create_footer():

    return dbc.Navbar(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                html.I("This is an Open Source Project: ")
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "GitHub Repository",
                                    href="https://github.com/marcelonyc/xformer-builder",
                                    target="_blank",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "Documentation",
                                    href="https://marcelonyc.github.io/xformer-builder",
                                    target="_blank",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        "Run in Docker",
                                        html.I(" - "),
                                        html.I(
                                            className="fa-brands fa-docker"
                                        ),
                                    ],
                                    href="https://hub.docker.com/repository/docker/marcelonyc/xformer/general",
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
