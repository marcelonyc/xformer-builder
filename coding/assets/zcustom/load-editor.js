function python_load_editor(editor_div,
    editor_button_n_clicks, button_value, code) {
    // Editor button n_cliks is not used but it is necessary to keep it
    // Determine what button trigger the edit (Buton index goes along with code index)
    triggered_id = window.dash_clientside.callback_context.triggered_id;
    if (document.getElementById(editor_div) != null && triggered_id != null) {
        editor = ace.edit(editor_div);
        editor_index = triggered_id["index"];
        editor.setValue(code[editor_index] ?? "");
        editor.setTheme("ace/theme/monokai");
        editor.session.setMode("ace/mode/python");
        return [editor_index, "Editing code for: " + button_value[editor_index]];
    } else {
        return [0, ""];
    }
}

function python_save_code_by_index(editor_div,
    n_clicks,
    editor_index, code) {
    // if (n_clicks == 0) {
    //     return null;
    // }
    editor_index = editor_index;
    code[editor_index] = ace.edit(editor_div).getValue();
    return [editor_index, code];
}