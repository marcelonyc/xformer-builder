from dash import Output, Input, State, ALL, clientside_callback

editor_save_button = "save-button"


def load_editor_callback(
    editor_div: str,
    editor_index: str,
    editor_modal: str,
    editor_button: str,
    editor_code: str,
    editor_title_h2: str,
):

    clientside_callback(
        """
        function (n_clicks, button_value, code) {
            ret_val = python_load_editor("%s",n_clicks, button_value, code);
            ret_val.push(false);
            return ret_val
    }
        """
        % editor_div,
        Output(editor_index, "value", allow_duplicate=True),
        Output(editor_title_h2, "children", allow_duplicate=True),
        Output(editor_modal, "hidden", allow_duplicate=True),
        Input({"type": editor_button, "index": ALL}, "n_clicks"),
        State({"type": editor_button, "index": ALL}, "value"),
        State({"type": editor_code, "index": ALL}, "value"),
        prevent_initial_call=True,
    )


def save_editor_callback(
    editor_div: str,
    editor_index: str,
    editor_code: str,
    editor_modal: str,
    editor_save_intervals: str = "editor-save-intervals",
):

    clientside_callback(
        """
        function (n_clicks, editor_index, code) {
            return_values = python_save_code_by_index("%s",
            n_clicks, editor_index, code)
            // return_values.push(true);
            return return_values;
    }
        """
        % editor_div,
        Output(editor_index, "value", allow_duplicate=True),
        Output({"type": editor_code, "index": ALL}, "value"),
        # Output(editor_modal, "hidden", allow_duplicate=True),
        Input(editor_save_intervals, "n_intervals"),
        State(editor_index, "value"),
        State({"type": editor_code, "index": ALL}, "value"),
        prevent_initial_call=True,
    )


# def close_editor_callback(
#     editor_modal: str,
# ):

#     clientside_callback(
#         """
#         function (n_clicks) {
#             return true;
#     }
#         """,
#         Output(editor_modal, "hidden", allow_duplicate=True),
#         Input(editor_close_button, "n_clicks"),
#         prevent_initial_call=True,
#     )
