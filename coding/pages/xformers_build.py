# Import necessary libraries
import dash_bootstrap_components as dbc
from dash import (
    html,
    Patch,
    register_page,
    callback,
    ALL,
    dcc,
    Output,
    State,
    Input,
    clientside_callback,
    ctx,
)
import pandas as pd
import io
import numpy as np
import code_editor.editor as editor_utils
import code_editor.callbacks as editor_callbacks
import code_editor.editor as editor_utils
import base64
from utils import xformers_build as xformers_utils
from utils.xformers_build import xformer_validator

register_page(__name__, name="Trial", top_nav=True, path="/")

# Element IDs
editor_div = "editor"  # Div name for rendering editor
editor_index = "editor-index"  # Place holder to store index of current editor
editor_modal = "editor-modal"  # Modal to display editor activity
editor_button = "editor-button"  # Button to open editor. Indexed ID (multiple)
editor_code = "editor-code"  # Store code of each editor. Indexed ID (multiple)
editor_close_button = "close-editor-button"
editor_title_h2 = "editor-title"
editor_test_button = "test-code-button"
editor_save_intervals = "editor-save-intervals"
editor_status_id = "edit-status-id"
save_all_link = "save-all-link"
add_column_link = "add-column-link"
editor_test_link = "test-all-xformers-link"
editor_button_row = "editor-button-row"
column_xformer_status = "column-xformer-status"
xformer_name = "transformer-name"
editor_alerts_modal = "editor-alerts-model"
editor_alerts_modal_body = "editor-alerts-modal-body"
editor_saved_status_msg = "editor-saved-status-msg"

# Button to save code. Uses editor_index to identify editor


def layout(new_xformer: bool = True):

    # xformer_rows = xformers_utils.get_xformers(editor_button, editor_code)

    # num_of_xformers = len(xformer_rows)
    # # Hide save button if there are no xformers
    disable_save_all = False
    controls_div = html.Div(
        id="editor-controls-div",
        style={
            "margin": "auto",
            "padding": "20px",
            "position": "sticky",
            "top": "0",
            "zIndex": "1000",
            "border": "10px",
        },
    )
    if new_xformer:
        upload_children = ["Upload Sample CSV File. Limit 3 rows"]
        upload_style = {
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        }
        button_row_hidden = True
    else:
        upload_children = []
        upload_style = {}
        button_row_hidden = False

    status_div = html.Div(
        dbc.Row(
            [
                dbc.Col("Status: ", width="auto"),
                dbc.Col(
                    "Ready",
                    width="auto",
                    id=editor_status_id,
                    class_name="btn-success text-white",
                ),
            ],
        ),
    )
    popover_list = [
        dbc.Popover(
            "Save Transformers",
            target=save_all_link,
            id="save-all-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Add a new column transformer",
            target=add_column_link,
            id="add-column-popover",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
        dbc.Popover(
            "Test all transformers",
            target=editor_test_link,
            id="test-all-transformers",
            body=True,
            placement="bottom",
            trigger="hover",
        ),
    ]
    button_row = html.Div(
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarSimple(
                        [
                            dbc.NavItem(
                                dbc.Label(
                                    "Transformer Name:",
                                    id="transformer-name-label",
                                ),
                                style={"align": "left"},
                            ),
                            dbc.NavItem(
                                dbc.Input(
                                    id=xformer_name,
                                    type="text",
                                    minLength=36,
                                    maxLength=100,
                                ),
                                style={"align": "left"},
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fa fa-floppy-disk fa-xl"
                                        ),
                                        " ",
                                    ],
                                    id=save_all_link,
                                ),
                                style={"align": "right"},
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(className="fa fa-plus fa-xl"),
                                        " ",
                                    ],
                                    id=add_column_link,
                                ),
                                style={"align": "right"},
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className="fa-solid fa-person-running fa-xl"
                                        ),
                                        " ",
                                    ],
                                    id=editor_test_link,
                                ),
                                style={"align": "right"},
                            ),
                        ],
                        brand="Transformer Editor",
                    )
                ),
            ]
            + popover_list
        ),
        id=editor_button_row,
        hidden=button_row_hidden,
    )
    hidden_row = dbc.Row(
        [
            dbc.Input(id=editor_index, type="hidden"),
            dbc.Alert(
                "Code Saved", id="code-saved-success-window", is_open=False
            ),
            dbc.Alert(
                "Failed to save code",
                id="code-saved-failed-window",
                is_open=False,
            ),
            dcc.Interval(id="save-xformer-interval", interval=20000),
            dcc.Interval(id=editor_save_intervals, interval=1000),
            dbc.Modal(
                [
                    dbc.ModalHeader("Editor Alert"),
                    dbc.ModalBody(id=editor_alerts_modal_body),
                ],
                id=editor_alerts_modal,
                class_name="border-danger",
                is_open=False,
            ),
        ]
    )
    add_column_modal = dbc.Modal(
        [
            dbc.ModalHeader("Select a source Column"),
            dbc.ModalBody(id="add-column-modal-body"),
            dbc.ModalFooter(
                [
                    dbc.Button("Add", id="add-column-button"),
                ]
            ),
        ],
        id="add-column-modal",
        is_open=False,
    )

    sample_upload_widget = dcc.Upload(
        upload_children,
        id="upload-sample-data",
        max_size=2500,
        style=upload_style,
        disabled=not new_xformer,
    )

    controls_div.children = [status_div, button_row]

    editor_div_body = html.Div(
        [
            controls_div,
            add_column_modal,
            sample_upload_widget,
            hidden_row,
            editor_utils.editor_div(
                editor_div,
                editor_modal,
                editor_test_button=editor_test_button,
                editor_close_button=editor_close_button,
            ),
            html.Div(
                dbc.Accordion(
                    None,
                    id="xformers-accordion",
                    start_collapsed=True,
                    class_name="card",
                ),
                style={
                    "padding": "30px",
                    "zIndex": "999",
                    "height": "600px",
                    "overflowX": "hidden",
                    "overflowY": "auto",
                },
            ),
        ],
        style={"padding": "20px"},
        id="xformers-editor-div",
    )

    return html.Div([editor_div_body])


editor_callbacks.load_editor_callback(
    editor_div,
    editor_index,
    editor_modal,
    editor_button,
    editor_code,
    editor_title_h2,
)

editor_callbacks.save_editor_callback(
    editor_div,
    editor_index,
    editor_code,
    editor_modal,
    editor_save_intervals=editor_save_intervals,
)


@callback(
    Output("upload-sample-data", "disabled"),
    Output("upload-sample-data", "style"),
    Output("upload-sample-data", "children"),
    Output("xformers-accordion", "children"),
    Output(editor_modal, "hidden"),
    Output(editor_button_row, "hidden"),
    Input("upload-sample-data", "contents"),
    State("upload-sample-data", "filename"),
    prevent_initial_call=True,
)
def upload_sample_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    read_csv = pd.read_csv(io.StringIO(decoded.decode("utf-8")), nrows=3)
    sample = read_csv.head(1).to_dict("records")
    columns = read_csv.dtypes.to_dict()
    type_sample = []
    for key in sample[0]:
        col_type = "string"
        # print(type(columns[key]))
        if type(columns[key]) != np.dtypes.ObjectDType:
            col_type = "number"
        type_sample.append(
            {"name": key, "type": col_type, "sample": sample[0][key]}
        )
    xformer_rows = xformers_utils.generate_xformers_from_file(
        type_sample, editor_button, editor_code
    )
    return True, None, None, xformer_rows, True, False


@callback(
    Input("save-xformer-interval", "n_intervals"),
    State({"type": editor_button, "index": ALL}, "value"),
    State({"type": editor_code, "index": ALL}, "value"),
    State({"type": "column-source-type", "index": ALL}, "value"),
    State({"type": "column-target-type", "index": ALL}, "value"),
    State({"type": "editor-target-column", "index": ALL}, "value"),
)
def auto_save_all_code(
    save_interval,
    editor_buttons,
    code_list,
    source_type_list,
    target_type_list,
    target_column_list,
):

    for code in range(0, len(code_list)):
        if code_list[code] is None:
            code_list[code] = None
        else:
            code_list[code] = base64.b64encode(bytes(code_list[code], "utf-8"))
    xformers_definition = {
        "source_column": editor_buttons,
        "code": code_list,
        "source_type": source_type_list,
        "target_type": target_type_list,
        "target_column": target_column_list,
    }


@callback(
    Output(
        {"type": "column-target-data", "index": ALL},
        "value",
        allow_duplicate=True,
    ),
    Output(
        {"type": "column-target-data", "index": ALL},
        "class_name",
        allow_duplicate=True,
    ),
    Output(
        {"type": "accordion-item", "index": ALL},
        "class_name",
        allow_duplicate=True,
    ),
    Output(editor_status_id, "children", allow_duplicate=True),
    Output(editor_status_id, "class_name", allow_duplicate=True),
    Output(
        {"type": column_xformer_status, "index": ALL},
        "value",
        allow_duplicate=True,
    ),
    Output(editor_modal, "hidden", allow_duplicate=True),
    Output(editor_alerts_modal, "is_open", allow_duplicate=True),
    Output(editor_alerts_modal_body, "children", allow_duplicate=True),
    Input(save_all_link, "n_clicks"),
    Input(editor_test_link, "n_clicks"),
    State({"type": editor_button, "index": ALL}, "value"),
    State({"type": editor_code, "index": ALL}, "value"),
    State({"type": "column-sample-data", "index": ALL}, "value"),
    State({"type": "column-target-data", "index": ALL}, "value"),
    State({"type": "column-target-data", "index": ALL}, "class_name"),
    State({"type": "accordion-item", "index": ALL}, "class_name"),
    State({"type": column_xformer_status, "index": ALL}, "value"),
    State(xformer_name, "value"),
    prevent_initial_call=True,
)
def save_all_code(
    n_clicks,
    editort_test_n_clicks,
    editor_button,
    code_list,
    sample_data_list,
    target_data_list,
    target_data_class,
    accordion_class,
    column_status,
    xformer_name,
):

    if xformer_name is None:
        return (
            target_data_list,
            target_data_class,
            accordion_class,
            "Transformer Name Required",
            "btn-danger text-white",
            column_status,
            False,
            True,
            "Transformer Name Required",
        )

    editor_index = 0
    return_values = ()
    syntax_status = "success"
    for _col in editor_button:
        syntax_check = test_code(
            n_clicks,
            0,
            editor_button,
            code_list,
            editor_index,
            sample_data_list,
            target_data_list,
            target_data_class,
            accordion_class,
            column_status,
        )

        if (
            syntax_check[5][editor_index] == "failed"
            and syntax_status == "success"
        ):
            syntax_status = "failed"
            return_values = syntax_check

        if return_values == ():
            return_values = syntax_check

        editor_index += 1

    saved_msg = "Saved Successfully"
    if syntax_status == "failed":
        saved_msg = "Syntax Error. Review list for highlighted errors"

    if ctx.triggered_id != editor_test_link:
        # open(f"/tmp/{xformer_name}.json", "w").write(str(return_values))
        # Set up a function here to save the xformers
        print(return_values)

    return return_values + (
        True,
        saved_msg,
    )


@callback(
    Output("add-column-modal-body", "children", allow_duplicate=True),
    Output("add-column-modal", "is_open", allow_duplicate=True),
    Input(add_column_link, "n_clicks"),
    State({"type": editor_button, "index": ALL}, "value"),
    prevent_initial_call=True,
)
def add_column_selection(
    n_clicks,
    editor_buttons,
):
    if n_clicks is None:
        return [], False

    select_options = []

    for _col in editor_buttons:
        if _col not in select_options:

            select_options.append(
                {"label": _col, "value": _col},
            )

    select_div = html.Div(
        dbc.Select(
            id="column-list-selection",
            options=select_options,
            value=None,
        )
    )

    return select_div, True


@callback(
    Output("xformers-accordion", "children", allow_duplicate=True),
    Output("add-column-modal", "is_open", allow_duplicate=True),
    Input("add-column-button", "n_clicks"),
    State("column-list-selection", "value"),
    State({"type": editor_button, "index": ALL}, "value"),
    State({"type": "column-source-type", "index": ALL}, "value"),
    State({"type": "column-sample-data", "index": ALL}, "value"),
    State("add-column-modal", "is_open"),
    prevent_initial_call=True,
)
def add_column(
    n_clicks,
    column_name,
    editor_buttons,
    source_type,
    column_sample,
    modal_state,
):
    if column_name is None:
        return [], modal_state

    col_list_position = editor_buttons.index(column_name)

    accordion_patched = Patch()
    new_column = {
        "column_index": len(editor_buttons),
        "column_type": source_type[col_list_position],
        "sample": column_sample[col_list_position],
    }
    new_column_row = xformers_utils.xformer_edit_row_build(
        xformer=column_name,
        xformer_dict=new_column,
        editor_button=editor_button,
        editor_code=editor_code,
    )
    accordion_patched.append(new_column_row)
    return accordion_patched, False


@callback(
    Output(
        {"type": "column-target-data", "index": ALL},
        "value",
        allow_duplicate=True,
    ),
    Output(
        {"type": "column-target-data", "index": ALL},
        "class_name",
        allow_duplicate=True,
    ),
    Output(
        {"type": "accordion-item", "index": ALL},
        "class_name",
        allow_duplicate=True,
    ),
    Output(editor_status_id, "children", allow_duplicate=True),
    Output(editor_status_id, "class_name", allow_duplicate=True),
    Output(
        {"type": column_xformer_status, "index": ALL},
        "value",
        allow_duplicate=True,
    ),
    Output(editor_modal, "hidden", allow_duplicate=True),
    Input(editor_test_button, "n_clicks"),
    Input(editor_close_button, "n_clicks"),
    State({"type": editor_button, "index": ALL}, "value"),
    State({"type": editor_code, "index": ALL}, "value"),
    State(editor_index, "value"),
    State({"type": "column-sample-data", "index": ALL}, "value"),
    State({"type": "column-target-data", "index": ALL}, "value"),
    State({"type": "column-target-data", "index": ALL}, "class_name"),
    State({"type": "accordion-item", "index": ALL}, "class_name"),
    State({"type": column_xformer_status, "index": ALL}, "value"),
    prevent_initial_call=True,
)
def test_code(
    test_n_clicks,
    close_n_clicks,
    editor_button,
    code_list,
    editor_index,
    sample_data_list,
    target_data_list,
    target_data_class,
    accordion_class,
    column_status,
):
    """
    This function is used to test the code.

    Parameters:
    - test_n_clicks (int): Number of times the test button is clicked.
    - close_n_clicks (int): Number of times the close button is clicked.
    - editor_button (str): The button used to trigger the editor.
    - code_list (list): List of code snippets.
    - editor_index (int): Index of the editor.
    - sample_data_list (list): List of sample data.
    - target_data_list (list): List of target data.
    - target_data_class (str): Class of the target data.
    - accordion_class (str): Class of the accordion.
    - column_status (str): Status of the column.

    Returns:
    - tuple: A tuple containing the return values of the xformer_validator function and the is_hide_editor flag.
    """
    return_values = xformer_validator(
        editor_button,
        code_list,
        editor_index,
        sample_data_list,
        target_data_list,
        target_data_class,
        accordion_class,
        column_status,
    )
    is_hide_editor = (False,)
    if ctx.triggered_id == editor_close_button:
        if (
            return_values[5][editor_index] != "success"
            and return_values[5][editor_index] is not None
        ):
            is_hide_editor = (False,)
        else:
            is_hide_editor = (True,)

    return return_values + is_hide_editor
