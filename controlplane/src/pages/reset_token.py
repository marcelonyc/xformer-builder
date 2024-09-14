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
    __name__,
    name="Reset Token",
    path_template="/reset_token/<reset_code>",
    top_nav=False,
)


# Button to save code. Uses editor_element_index to identify editor

object_prefix = "token-reset"


def layout(reset_code: str = None):

    response = dataplane_platform_post(
        endpoint="/token-reset/{}".format(reset_code),
    )

    return "New Token: {}".format(response)
