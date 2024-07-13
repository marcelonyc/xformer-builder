from typing import Dict
import dash_bootstrap_components as dbc
from dash import html, ctx
import python_modules.code_validator.code_validator as code_validator


def generate_xformers_from_file(
    type_sample, editor_button, editor_code
) -> Dict:

    Xformers = {}
    column_index = 0
    for column in type_sample:
        Xformers[column["name"]] = {
            "column_index": column_index,
            "column_type": column["type"],
            "sample": column["sample"],
        }
        column_index += 1

    num_of_xformers = len(Xformers)
    xformer_rows = []

    if num_of_xformers > 0:
        for xformer in Xformers.keys():
            xformer_rows.append(
                xformer_edit_row_build(
                    xformer,
                    xformer_dict=Xformers[xformer],
                    editor_button=editor_button,
                    editor_code=editor_code,
                )
            )
    return xformer_rows


def xformer_edit_row_build(
    xformer: str,
    xformer_dict: Dict,
    editor_button: str = "editor-button",
    editor_code: str = "editor-code",
):
    column_row = xformer_dict["column_index"]
    row_columns = dbc.Row(
        [
            dbc.Col(dbc.Label("Source Type")),
            dbc.Col(dbc.Label("Code")),
            dbc.Col(dbc.Label("Target Type")),
            dbc.Col(dbc.Label("Target Column")),
        ]
    )
    source_column = dbc.Col(
        [
            dbc.Row(
                dbc.Select(
                    id={
                        "type": "column-source-type",
                        "index": column_row,
                    },
                    options=[
                        {"label": "string", "value": "string"},
                        {"label": "number", "value": "number"},
                    ],
                    value=xformer_dict["column_type"],
                )
            ),
            dbc.Input(
                id={"type": "column-xformer-status", "index": column_row},
                type="hidden",
                value=None,
            ),
            dbc.Row(
                dbc.Input(
                    id={
                        "type": "column-sample-data",
                        "index": column_row,
                    },
                    type="text",
                    readonly=True,
                    value=xformer_dict["sample"],
                )
            ),
        ]
    )

    target_column = dbc.Col(
        [
            dbc.Row(
                dbc.Input(
                    id={
                        "type": "editor-target-column",
                        "index": column_row,
                    },
                    type="text",
                    readonly=False,
                    value=xformer,
                ),
                style={"float": "auto"},
            ),
            dbc.Row(
                dbc.Input(
                    id={
                        "type": "column-target-data",
                        "index": column_row,
                    },
                    type="text",
                    readonly=True,
                    value=xformer_dict["sample"],
                )
            ),
        ]
    )
    row_structure = dbc.Row(
        [
            source_column,
            dbc.Col(
                [
                    dbc.Textarea(
                        id={
                            "type": editor_code,
                            "index": column_row,
                        },
                        readonly=True,
                    ),
                    dbc.Button(
                        f"Code Editor",
                        id={
                            "type": editor_button,
                            "index": column_row,
                        },
                        n_clicks=0,
                        value=xformer,
                    ),
                ]
            ),
            dbc.Col(
                dbc.Select(
                    id={
                        "type": "column-target-type",
                        "index": column_row,
                    },
                    options=[
                        {"label": "string", "value": "string"},
                        {"label": "number", "value": "number"},
                    ],
                    value=xformer_dict["column_type"],
                )
            ),
            target_column,
        ]
    )
    return dbc.AccordionItem(
        html.Div([row_columns, row_structure]),
        title=f"Source Coulmn: {xformer}",
        style={"height": "auto"},
        id={"type": "accordion-item", "index": column_row},
    )


def xformer_validator(
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
    Validates and executes transformers based on the provided inputs.

    Args:
        editor_button (list): List of editor buttons.
        code_list (list): List of code snippets.
        editor_index (int): Index of the current editor.
        sample_data_list (list): List of sample data.
        target_data_list (list): List of target data.
        target_data_class (list): List of target data classes.
        accordion_class (list): List of accordion classes.
        column_status (list): List of column statuses.

    Returns:
        tuple: A tuple containing the updated target_data_list, target_data_class,
        accordion_class, editor_status_msg, editor_status_class, and column_status.
    """

    other_values = {}
    for _value in editor_button:
        other_values[_value] = sample_data_list[editor_button.index(_value)]

    if code_list[editor_index] == "" or code_list[editor_index] is None:
        return (
            target_data_list,
            target_data_class,
            accordion_class,
            "Transformers are ready",
            "btn-success text-white",
            column_status,
        )
    exec_results = code_validator.safe_execute(
        code_list[editor_index],
        sample_data_list[editor_index],
        other_values,
    )

    editor_status_msg = "Transformers with errors"
    classes_failed = "btn-danger text-white"
    classes_sucess = "btn-success text-white"
    if exec_results["status"] != "success":
        target_data_list[editor_index] = exec_results["result"]
        target_data_class[editor_index] = "bg-danger"
        accordion_class[editor_index] = "border-danger"
        column_status[editor_index] = "failed"
        editor_status_msg = editor_status_msg
        editor_status_class = classes_failed
    else:
        target_data_list[editor_index] = exec_results["result"]
        target_data_class[editor_index] = "bg-success"
        accordion_class[editor_index] = "border-success"
        column_status[editor_index] = "success"
        if "failed" in column_status:
            editor_status_msg = editor_status_msg
            editor_status_class = classes_failed
        else:
            editor_status_msg = "Transformers are ready"
            editor_status_class = classes_sucess

    return (
        target_data_list,
        target_data_class,
        accordion_class,
        editor_status_msg,
        editor_status_class,
        column_status,
    )
