from typing import Dict
import dash_bootstrap_components as dbc
from dash import html
import python_modules.code_validator.code_validator as code_validator
import config.editor_config as editor_config
from dataclasses import dataclass, field
from dataplane.dataplane import dataplane_get
from lib.models import XformerData, XformerRow
import base64


def generate_xformers_from_file(
    type_sample, editor_button, editor_code
) -> Dict:
    """
    Generate transformers from a file.

    Args:
        type_sample (list): A list of dictionaries representing the type sample.
        editor_button (str): The editor button.
        editor_code (str): The editor code.

    Returns:
        list: A list of xformer rows.

    """
    xformer_rows = []
    column_index = 0
    for column in type_sample:
        _xformer = XformerRow(
            **{
                "name": column["name"],
                "column_index": column_index,
                "column_type": column["type"],
                "code": None,
                "sample": column["sample"],
            }
        )
        column_index += 1
        xformer_rows.append(
            xformer_edit_row_build(
                _xformer,
                editor_button=editor_button,
                editor_code=editor_code,
            )
        )
    return xformer_rows


def generate_xformers_from_api(
    xformer_name, editor_button, editor_code
) -> Dict:

    try:
        _api_response = dataplane_get(
            f"/list-xformer?xformer_name={xformer_name}"
        )
    except Exception as e:
        raise Exception(f"Failed to get xformers. Actual error {str(e)}")

    if len(_api_response) == 0:
        return []

    return xformer_from_json(
        _api_response["rows"][0], editor_button, editor_code
    )


def xformer_from_json(xformer_json, editor_button, editor_code):

    xformer_data = XformerData(**xformer_json)
    columns = xformer_data.xformer.source_column
    code = xformer_data.xformer.code
    source_type = xformer_data.xformer.source_type
    source_column = xformer_data.xformer.source_column
    sample = xformer_data.xformer.sample
    target_type = xformer_data.xformer.target_type
    target_column = xformer_data.xformer.target_column

    xformer_rows = []
    for _column in range(len(columns)):
        _xformer = XformerRow(
            **{
                "name": columns[_column],
                "code": code[_column],
                "column_index": _column,
                "column_type": source_type[_column],
                "sample": sample[_column],
                "target_type": target_type[_column],
                "target_column": target_column[_column],
            }
        )
        xformer_rows.append(
            xformer_edit_row_build(
                _xformer,
                editor_button=editor_button,
                editor_code=editor_code,
            )
        )
    return xformer_rows


def xformer_edit_row_build(
    xformer: XformerRow,
    editor_button: str = "editor-button",
    editor_code: str = "editor-code",
):

    column_row = xformer.column_index
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
                    value=xformer.column_type,
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
                    value=xformer.sample,
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
                    value=xformer.target_column,
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
                    value=xformer.target_sample,
                )
            ),
        ]
    )

    if xformer.code is not None:
        xformer_code = base64.b64decode(xformer.code).decode("utf-8")
    else:
        xformer_code = ""

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
                        value=xformer_code,
                    ),
                    dbc.Button(
                        f"Code Editor",
                        id={
                            "type": editor_button,
                            "index": column_row,
                        },
                        n_clicks=0,
                        value=xformer.name,
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
                    value=xformer.target_type,
                )
            ),
            target_column,
        ]
    )
    return dbc.AccordionItem(
        html.Div([row_columns, row_structure]),
        title=f"Source Coulmn: {xformer.name}",
        style={"height": "auto"},
        id={"type": "accordion-item", "index": column_row},
    )


class TestCode:

    def __init__(
        self,
        test_n_clicks: int,
        close_n_clicks: int,
        editor_button: list,
        code_list: list,
        editor_element_index: int,
        sample_data_list: list,
        target_data_list: list,
        target_data_class: str,
        accordion_class: str,
        column_status: str,
    ):
        self.editor_button = editor_button
        self.code_list = code_list
        self.editor_element_index = editor_element_index
        self.sample_data_list = sample_data_list
        self.target_data_list = target_data_list
        self.target_data_class = target_data_class
        self.accordion_class = accordion_class
        self.column_status = column_status

    def validate(self):
        other_values = {}
        for _value in self.editor_button:
            other_values[_value] = self.sample_data_list[
                self.editor_button.index(_value)
            ]

        if (
            self.code_list[self.editor_element_index] == ""
            or self.code_list[self.editor_element_index] is None
        ):
            return (
                self.target_data_list,
                self.target_data_class,
                self.accordion_class,
                "Transformers are ready",
                "btn-success text-white",
                self.column_status,
            )
        exec_results = code_validator.safe_execute(
            self.code_list[self.editor_element_index],
            self.sample_data_list[self.editor_element_index],
            other_values,
        )

        editor_status_msg = "Transformers with errors"
        classes_failed = "btn-danger text-white"
        classes_sucess = "btn-success text-white"
        if exec_results["status"] != editor_config.EditorStatus.TEST_SUCCESS:
            self.target_data_list[self.editor_element_index] = exec_results[
                "result"
            ]
            self.target_data_class[self.editor_element_index] = "bg-danger"
            self.accordion_class[self.editor_element_index] = "border-danger"
            self.column_status[self.editor_element_index] = (
                editor_config.EditorStatus.TEST_FAILED
            )
            editor_status_msg = editor_status_msg
            editor_status_class = classes_failed
        else:
            self.target_data_list[self.editor_element_index] = exec_results[
                "result"
            ]
            self.target_data_class[self.editor_element_index] = "bg-success"
            self.accordion_class[self.editor_element_index] = "border-success"
            self.column_status[self.editor_element_index] = (
                editor_config.EditorStatus.TEST_SUCCESS
            )
            if editor_config.EditorStatus.TEST_FAILED in self.column_status:
                editor_status_msg = editor_status_msg
                editor_status_class = classes_failed
            else:
                editor_status_msg = "Transformers are ready"
                editor_status_class = classes_sucess

        return (
            self.target_data_list,
            self.target_data_class,
            self.accordion_class,
            editor_status_msg,
            editor_status_class,
            self.column_status,
        )


@dataclass
class XformerValidatorReturn:

    # Valid Values
    transformer_status_ready = "Transformers are ready"
    transformer_status_error = "Transformers with errors"
    button_class_success = "btn-success text-white"
    button_class_failed = "btn-danger text-white"
    column_status_success = "success"
    column_status_failed = "failed"
    target_data_class_error = "bg-danger"
    target_data_class_success = "bg-success"
    accordion_class_error = "border-danger"
    accordion_class_success = "border-success"
    editor_classes_failed = "btn-danger text-white"
    editor_classes_sucess = "btn-success text-white"

    target_data_list: list = field(default_factory=list)
    target_data_class: str = None
    accordion_class: str = None
    transformer_status: str = transformer_status_ready
    button_class: str = button_class_success
    column_status: str = None

    def return_values_in_tuple(self):
        return (
            self.target_data_list,
            self.target_data_class,
            self.accordion_class,
            self.transformer_status,
            self.button_class,
            self.column_status,
        )


class XformerValidator:

    def __init__(
        self,
        editor_button: str,
        code_list,
        editor_element_index,
        sample_data_list,
        target_data_list,
        target_data_class,
        accordion_class,
        column_status: str = None,
    ):
        self.editor_button = editor_button
        self.code_list = code_list
        self.editor_element_index = editor_element_index
        self.sample_data_list = sample_data_list
        self.target_data_list = target_data_list
        self.target_data_class = target_data_class
        self.accordion_class = accordion_class
        self.column_status = column_status
        self.editor_status_msg = "Transformers with errors"
        self.editor_status_class = "btn-danger text-white"

    def validate(self):

        return_values = XformerValidatorReturn()

        other_values = {}
        for _value in self.editor_button:
            other_values[_value] = self.sample_data_list[
                self.editor_button.index(_value)
            ]

        if (
            self.code_list[self.editor_element_index] == ""
            or self.code_list[self.editor_element_index] is None
        ):
            return_values.target_data_list = self.target_data_list
            return_values.target_data_class = self.target_data_class
            return_values.accordion_class = self.accordion_class
            return_values.transformer_status = (
                return_values.transformer_status_ready
            )
            return_values.button_class = return_values.button_class_success
            return_values.column_status = self.column_status
            return return_values.return_values_in_tuple()

        exec_results = code_validator.safe_execute(
            self.code_list[self.editor_element_index],
            self.sample_data_list[self.editor_element_index],
            other_values,
        )

        return_values.transformer_status = (
            return_values.transformer_status_error
        )
        if exec_results["status"] != editor_config.EditorStatus.TEST_SUCCESS:
            self.target_data_list[self.editor_element_index] = exec_results[
                "result"
            ]
            self.target_data_class[self.editor_element_index] = (
                return_values.target_data_class_error
            )
            self.accordion_class[self.editor_element_index] = (
                return_values.accordion_class_error
            )
            self.column_status[self.editor_element_index] = (
                editor_config.EditorStatus.TEST_FAILED
            )
            self.editor_status_msg = return_values.transformer_status_error
            self.editor_status_class = return_values.editor_classes_failed
        else:
            self.target_data_list[self.editor_element_index] = exec_results[
                "result"
            ]
            self.target_data_class[self.editor_element_index] = (
                return_values.target_data_class_success
            )
            self.accordion_class[self.editor_element_index] = (
                return_values.accordion_class_success
            )
            self.column_status[self.editor_element_index] = (
                editor_config.EditorStatus.TEST_SUCCESS
            )
            if editor_config.EditorStatus.TEST_FAILED in self.column_status:
                self.editor_status_msg = return_values.transformer_status_error
                self.editor_status_class = return_values.button_class_failed
            else:
                self.editor_status_msg = return_values.transformer_status_ready
                self.editor_status_class = return_values.editor_classes_sucess

    def return_values_in_tuple(self):
        """
        Returns a tuple containing the following values:
        - target_data_list: The target data list.
        - target_data_class: The target data class.
        - accordion_class: The accordion class.
        - editor_status_msg: The editor status message.
        - editor_status_class: The editor status class.
        - column_status: The column status.
        """
        return (
            self.target_data_list,
            self.target_data_class,
            self.accordion_class,
            self.editor_status_msg,
            self.editor_status_class,
            self.column_status,
        )
