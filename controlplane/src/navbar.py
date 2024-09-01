import dash_bootstrap_components as dbc
from dash import html, dcc
from flask_login import current_user


def create_editor_navbar():
    pop_overs = dbc.Popover(
        "Questions? Issues? Suggestions? Please, let me know!",
        target="issue-tracker",
        id="issues-popover",
        body=True,
        placement="bottom",
        trigger="hover",
    )

    _disable_auth_nav = True
    try:
        current_user = current_user.is_authenticated
        if current_user:
            _is_authenticated = False
    except:
        pass

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
                                disabled=_disable_auth_nav,
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


def create_navbar():
    _disable_auth_nav = False
    try:
        current_user = current_user.is_authenticated
        if current_user:
            _is_authenticated = False
    except:
        pass

    pop_overs = [
        dbc.Popover(
            "Create a transformer",
            target="xformer-builder-menu-link",
            id="xformer-builder-menu-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Edit transformer",
            target="edit-xformer-menu-link",
            id="edit-xformer-menu-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Register for an Account",
            target="xformer-register-link",
            id="xformer-register-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Create unique file upload link",
            target="assign-xformer-menu-link",
            id="assign-xformer-menu-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Available Downloads",
            target="download-menu-link",
            id="download-menu-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Report Issues",
            target="issue-tracker",
            id="issue-tracker-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Event Triggers",
            target="event-triggers-link",
            id="event-triggers-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
    ]

    if _disable_auth_nav:
        register_link = dbc.NavItem(
            dbc.NavLink(
                [html.I(className="fa-solid fa-cash-register fa-xl")],
                href="/register",
                target="_blank",
                id="xformer-register-link",
            )
        )
    else:
        register_link = ""

    interval_objects = [
        dcc.Interval(
            id="dataplane-status-alert-interval",
            interval=300000,
            n_intervals=0,
        )
    ]

    admin_nav = dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(
                [html.I(className="fa-solid fa-square-share-nodes fa-xl")],
                href="/event-triggers",
                id="event-triggers-link",
            )
        ],
        label=html.I(className="fa-solid fa-gear fa-xl"),
        nav=True,
    )

    return dbc.NavbarSimple(
        dbc.Row(
            dbc.Col(
                dbc.Nav(
                    [
                        register_link,
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="fa-solid fa-home fa-xl")],
                                href="/",
                                target="_blank",
                                id="xformer-home-menu-link",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-solid fa-arrow-right-arrow-left fa-xl"
                                    )
                                ],
                                href="/xformer-builder",
                                target="_blank",
                                id="xformer-builder-menu-link",
                                disabled=_disable_auth_nav,
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-solid fa-pen-to-square fa-xl"
                                    )
                                ],
                                href="/edit-xformer",
                                target="_blank",
                                id="edit-xformer-menu-link",
                                disabled=_disable_auth_nav,
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="fa-solid fa-link fa-xl")],
                                href="/associate-xformer",
                                target="_blank",
                                id="assign-xformer-menu-link",
                                disabled=_disable_auth_nav,
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-solid fa-download fa-xl"
                                    )
                                ],
                                href="/download",
                                target="_blank",
                                id="download-menu-link",
                                disabled=_disable_auth_nav,
                            )
                        ),
                        dbc.NavItem(admin_nav),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-solid fa-life-ring fa-xl"
                                    )
                                ],
                                href="https://github.com/marcelonyc/xformer-builder/issues",
                                target="_blank",
                                id="issue-tracker",
                            ),
                        ),
                        dbc.NavItem(id="user-status-header"),
                    ]
                    + pop_overs
                    + interval_objects,
                    navbar=True,
                )
            )
        ),
        sticky="top",
        brand="Data Onboarding",
    )
