# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import html
import code_editor.callbacks as editor_callbacks
import code_editor.editor as editor_utils


# Create a Dash application
external_stylesheets = [
    dbc.themes.SOLAR,
    "https://use.fontawesome.com/releases/v6.2.1/css/all.css",
]

suppress_callback_exceptions = True

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=suppress_callback_exceptions,
)


app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>Data Transformer</title>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>     
    </body>
</html>
"""

# Run the application
if __name__ == "__main__":
    app.run(debug=False)
