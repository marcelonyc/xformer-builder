# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, ALL, callback
import os
from config.app_config import get_settings
import base64
from flask import Flask, request, redirect, session
from flask_login import login_user, LoginManager, current_user
from dataplane.dataplane import dataplane_get


from auth.auth import controlplane_auth
from auth.login_handler import restricted_page
from navigation import NavigationElements
from auth.models import UserAuthenticated


# Create a Dash application
external_stylesheets = [
    dbc.themes.SANDSTONE,
    "https://use.fontawesome.com/releases/v6.2.1/css/all.css",
]

server = Flask(__name__)


@server.route("/login", methods=["POST"])
def login_button_click():
    if request.form:
        app_token = request.form["app_token"]
        _auth_response = controlplane_auth(app_token)
        if _auth_response.status:
            login_user(
                UserAuthenticated(app_token),
                remember=True,
            )

            if "url" in session:
                if session["url"]:
                    url = session["url"]
                    session["url"] = None
                    return redirect(url)  ## redirect to target url
            return redirect("/")  ## redirect to home
        return redirect("/login?status=invalid_token")


suppress_callback_exceptions = True

app = dash.Dash(
    __name__,
    use_pages=True,
    server=server,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=suppress_callback_exceptions,
)

# session_secret = base64.b64encode(os.urandom(30)).decode("utf-8")

server.config.update(SECRET_KEY=os.getenv("SESSION_SECRET"))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_profile: str):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return UserAuthenticated(user_profile)


config = get_settings()

navigation_parts = NavigationElements()
NAVBAR = navigation_parts.navbar
FOOTER = navigation_parts.footer


def my_app_layout():
    return html.Div(
        [
            dcc.Location(id="url"),
            html.Div(id="dataplane-status-alert"),
            NAVBAR,
            dash.page_container,
            FOOTER,
        ],
        style={"margin": "10", "padding": "10"},
    )


app.layout = my_app_layout


@callback(
    Output("user-status-header", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Output("logged-in-user-name", "children"),
    Input("url", "pathname"),
    Input({"index": ALL, "type": "redirect"}, "n_intervals"),
    prevent_initial_call=True,
)
def update_authentication_status(path, n):

    login_nav = (
        dbc.NavLink(
            html.I(className="fa-solid fa-right-to-bracket fa-xl"),
            href="/login",
            target="_blank",
            id="login-menu-link",
        ),
        dbc.Popover(
            "Login",
            target="login-menu-link",
            id="login-menu-link-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
    )

    ### logout redirect
    if n:
        if not n[0]:
            return "", dash.no_update, ""
        else:
            return login_nav, "/login", ""

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == "/login":
            return (
                dcc.Link("logout", href="/logout"),
                "/",
                current_user.user_profile.name,
            )

        logout_nav = (
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(
                            className="fa-solid fa-arrow-right-from-bracket fa-xl"
                        )
                    ],
                    href="/logout",
                    id="logout-menu-link",
                )
            ),
            dbc.Popover(
                "Logout",
                target="logout-menu-link",
                id="logout-menu-link-popover",
                body=True,
                placement="bottom",
                trigger="hover",
            ),
        )
        # return dcc.Link("logout", href="/logout"), dash.no_update
        return logout_nav, dash.no_update, current_user.user_profile.name
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session["url"] = path
            return login_nav, "/login", ""

    ### if path not login and logout display login link
    if current_user and path not in ["/login", "/logout"]:
        # return dcc.Link("login", href="/login"), dash.no_update, ""
        return login_nav, dash.no_update, ""

    ### if path login and logout hide links
    if path in ["/login", "/logout"]:
        return "", dash.no_update, ""


@callback(
    Output("dataplane-status-alert", "children"),
    Input("dataplane-status-alert-interval", "n_intervals"),
    prevent_initial_call=True,
)
def update_dataplane_status(n):

    alert = dbc.Alert(
        "DataPlane is down. Contact your administrator",
        color="danger",
        dismissable=True,
    )

    try:
        _api_response = dataplane_get("/healthcheck", auth=False)
    except Exception as e:
        return alert

    if "status" in _api_response:
        if _api_response["status"] == "ok":
            return ""
        else:
            return alert


# if os.getenv("DASH_DEBUG", False):
#     app.enable_dev_tools(debug=True)


application = app.server
# Run the application
if __name__ == "__main__":
    app.run(debug=config.debug)
