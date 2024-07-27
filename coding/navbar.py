import dash_bootstrap_components as dbc
from dash import html


def create_navbar():
    pop_overs = dbc.Popover(
        "Questions? Issues? Suggestions? Please, let me know!",
        target="issue-tracker",
        id="issues-popover",
        body=True,
        placement="bottom",
        trigger="hover",
    )

    return dbc.NavbarSimple(
        dbc.Row(
            dbc.Col(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="fa-brands fa-github"),
                                    " ",
                                ],
                                href="https://github.com/marcelonyc/xformer-builder",
                                target="_blank",
                                id="github-repo",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="fa-brands fa-linkedin"),
                                    " ",
                                ],
                                href="https://www.linkedin.com/in/marcelolitovsky/",
                                target="_blank",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="fa fa-life-ring"),
                                    " ",
                                ],
                                href="https://github.com/marcelonyc/xformer-builder/issues",
                                target="_blank",
                                id="issue-tracker",
                            )
                        ),
                        pop_overs,
                    ],
                    navbar=True,
                )
            )
        ),
        sticky="top",
        brand="Data Transformer",
    )
