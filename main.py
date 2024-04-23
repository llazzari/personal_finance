from pathlib import Path
import os
from dash import Dash
from dash_bootstrap_templates import load_figure_template
import i18n
import pandas as pd
import dash_bootstrap_components as dbc

from src.components import layout
from src.data.loader import load_data


EXPENSES_PATH: Path = Path.cwd() / "database" / "expenses.csv"
os.environ["EXPENSES_PATH"] = str(EXPENSES_PATH)
INCOMES_PATH: Path = Path.cwd() / "database" / "incomes.csv"
os.environ["INCOMES_PATH"] = str(INCOMES_PATH)

LOCALE = "pt"
os.environ["LOCALE"] = LOCALE

load_figure_template("darkly")


def main() -> None:
    # set the locale and load the translations
    i18n.set("locale", LOCALE)  # type: ignore
    locale_path: Path = Path.cwd() / "locale"
    i18n.load_path.append(locale_path)  # type: ignore

    # load expenses and incomes
    df_exp: pd.DataFrame = load_data(EXPENSES_PATH)
    expenses: list[dict] = df_exp.to_dict("records")
    df_inc: pd.DataFrame = load_data(INCOMES_PATH)
    incomes: list[dict] = df_inc.to_dict("records")

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = Dash(
        __name__, external_stylesheets=[dbc_css, dbc.themes.DARKLY, dbc.icons.BOOTSTRAP]
    )
    app.title = i18n.t("general.app_title")  # type: ignore
    app.layout = layout.render(app, expenses, incomes)
    app.config["suppress_callback_exceptions"] = True
    app.scripts.config.serve_locally = True
    # server = app.server
    app.run(debug=True, port="8050")


if __name__ == "__main__":
    main()
