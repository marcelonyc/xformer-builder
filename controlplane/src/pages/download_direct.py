# Import necessary libraries
from dash import html, register_page, callback, dcc, Output, Input, State
from config.app_config import AppConfig
from dataplane.dataplane import dataplane_get_file

register_page(
    __name__,
    name="Download File",
    top_nav=True,
    path_template="/download-direct/<file_id>/<upload_id>",
)


app_config = AppConfig()


def layout(file_id: str = "", upload_id: str = ""):

    out_layout = html.Div(
        [
            html.H2("Downloading File"),
            dcc.Download(id="download-single-file"),
            dcc.Interval(
                id="download-single-file-interval",
                interval=1000,
                max_intervals=1,
            ),
            html.Div(id="file_id_div", children=file_id, hidden=True),
            html.Div(id="upload_id_div", children=upload_id, hidden=True),
        ]
    )
    return out_layout


@callback(
    Output("download-single-file", "data"),
    Input("download-single-file-interval", "n_intervals"),
    State("file_id_div", "children"),
    State("upload_id_div", "children"),
    prevent_initial_call=True,
)
def download_single_file(n_intervals, file_id, upload_id):

    _api_response = dataplane_get_file(
        f"/download/{file_id}/{upload_id}", auth=False
    )
    # return download_url
    return dict(content=_api_response.text, filename=f"{file_id}.csv")
