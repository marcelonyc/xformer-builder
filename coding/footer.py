import dash_bootstrap_components as dbc


def create_footer():
    return dbc.Navbar(
        dbc.Row(
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
                )
            )
        ),
        sticky="bottom",
    )
