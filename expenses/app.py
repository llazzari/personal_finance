import os
import i18n
import dash_bootstrap_components as dbc
from dash import Dash
import pandas as pd
from pathlib import Path
from dash_bootstrap_templates import load_figure_template

from components import layout
from data.loader import load_data
from data.source import DataSource


LOCALE = 'pt'
os.environ['LOCALE'] = LOCALE
load_figure_template('darkly')


def main() -> None:
    # set the locale and load the translations
    i18n.set("locale", LOCALE)  # type: ignore
    locale_path = Path.cwd() / "locale"
    i18n.load_path.append(locale_path)  # type: ignore

    df: pd.DataFrame = load_data()
    data: list[dict] = df.to_dict('records')
    source = DataSource(data)

    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

    app = Dash(__name__, external_stylesheets=[dbc_css, dbc.themes.DARKLY])
    app.title = i18n.t("general.app_title")  # type: ignore
    app.layout = layout.render(app, source)
    app.config['suppress_callback_exceptions'] = True
    app.scripts.config.serve_locally = True
    # server = app.server
    app.run(debug=True, port='8050')


if __name__ == '__main__':
    main()
