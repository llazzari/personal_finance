import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import dash_bootstrap_components as dbc
import i18n
from dash import Dash
from dash_bootstrap_templates import load_figure_template

from src.components import layout
from src.data.db_manager import create_tables, get_transactions
from src.data.schema import Transaction

LOCALE = "pt"
os.environ["LOCALE"] = LOCALE

load_figure_template("darkly")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",
)

log_handler = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=5)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def main() -> None:
    logger.info("Starting application")

    # set the locale and load the translations
    i18n.set("locale", LOCALE)  # type: ignore
    locale_path: Path = Path.cwd() / "locale"
    i18n.load_path.append(locale_path)  # type: ignore
    logger.info(f"Locale set to {LOCALE}")

    # create the tables in the database
    logger.info("Creating database tables")
    create_tables()

    # load transactions from the database
    logger.info("Loading transactions from database")
    transactions: list[Transaction] = get_transactions()
    logger.info(f"Loaded {len(transactions)} users")

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    logger.info("Initializing Dash application")
    app = Dash(
        __name__,
        external_stylesheets=[dbc_css, dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    )
    app.title = i18n.t("general.app_title")  # type: ignore
    app.layout = layout.render(app, transactions)
    app.config["suppress_callback_exceptions"] = True
    app.scripts.config.serve_locally = True

    logger.info("Starting Dash server on port 8050")
    app.run(debug=True, port="8050")


if __name__ == "__main__":
    main()
