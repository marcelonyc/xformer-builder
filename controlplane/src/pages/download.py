# Import necessary libraries
from dash import (
    html,
    register_page,
    callback,
    dcc,
    State,
    Input,
)
import dash_bootstrap_components as dbc
import code_editor.editor as editor_utils
import base64
from config.app_config import get_settings
from auth.login_handler import require_login
from dataplane.dataplane import dataplane_post, dataplane_get
from lib.models import ListUploadedFilesResponse

register_page(
    __name__,
    name="Download File",
    top_nav=True,
    path_template="/download",
)
require_login(__name__)


app_config = get_settings()


def layout(association_id: str = ""):

    _files_list = dataplane_get(f"/list-uploaded-files")
    if "files" not in _files_list:
        return html.Div("Fail to get file association")

    file_list = ListUploadedFilesResponse(files=_files_list["files"])

    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("File ID"),
                    html.Th("File Size"),
                    html.Th("Upload Date"),
                    html.Th("Expires"),
                    html.Th("Last Upload Message"),
                    html.Th("Description"),
                ]
            )
        )
    ]
    rows = []
    for file in file_list.files:
        file_popover_target = f"{file.file_id}-{file.upload_id}-popover-target"
        row = html.Tr(
            [
                html.Td(
                    f"{file.file_id[1:5]}...",
                    id=file_popover_target,
                ),
                html.Td(file.file_size),
                html.Td(file.upload_date),
                html.Td(f"{file.file_expires_in_hours} Hours"),
                html.Td(file.last_update_message),
                html.Td(file.description),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Download"),
                        dbc.PopoverBody(
                            dbc.Button(
                                f"Download: {file.file_id}",
                                href=f"/download-direct/{file.file_id}/{file.upload_id}",
                                target="_blank",
                                color="primary",
                            ),
                        ),
                    ],
                    id=f"{file.file_id}-{file.upload_id}-popover",
                    target=file_popover_target,
                    trigger="hover",
                    placement="top-start",
                ),
            ]
        )
        rows.append(row)

    table_body = [html.Tbody(rows)]

    table = [
        html.H3("Uploaded Files"),
        html.H4("Click on the file ID to download the file"),
        html.Br(),
        dbc.Table(table_header + table_body, bordered=True, responsive=True),
    ]
    return table
