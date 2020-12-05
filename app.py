import uuid

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

copy_alert = dbc.Alert(
    "Code copied to clipboard!", id="copy_alert", duration=4000, is_open=False
)

code = html.P(html.Code("Some text", id="text_to_copy"), className="lead")

buttons = html.Div(
    [
        dbc.Button(
            "Generate New Code",
            id="generate_button",
            color="primary",
            className="d-inline-block, mr-1",
        ),
        dbc.Button(
            "Copy Code to Clipboard",
            id="copy_button",
            color="primary",
            outline=True,
            className="d-inline-block",
        ),
    ]
)

app.layout = dbc.Container(
    [
        copy_alert,
        code,
        buttons,
        html.Div(id="dummy_output"),
    ],
    className="mt-5",
)


@app.callback(Output("text_to_copy", "children"), Input("generate_button", "n_clicks"))
def generate_code(n_clicks):
    return str(uuid.uuid4())


copy_to_clipboard_js = """
function copyStringToClipboard (nClicks, text) {
    var el = document.createElement('textarea');
    el.value = text;
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}"""

app.clientside_callback(
    copy_to_clipboard_js,
    Output("dummy_output", "children"),
    Input("copy_button", "n_clicks"),
    State("text_to_copy", "children"),
)


@app.callback(Output("copy_alert", "is_open"), Input("copy_button", "n_clicks"))
def show_copy_alert(n_clicks):
    if n_clicks:
        return True
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5000, debug=True)
