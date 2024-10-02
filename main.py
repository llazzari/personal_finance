from pathlib import Path
import os
from dash import Dash
from dash_bootstrap_templates import load_figure_template
import i18n
import dash_bootstrap_components as dbc

from src.components.layout import User
from src.components import layout
from src.data.user import Profile, HouseholdProfile


LOCALE = "pt"
os.environ["LOCALE"] = LOCALE

load_figure_template("darkly")


def main() -> None:
    # set the locale and load the translations
    i18n.set("locale", LOCALE)  # type: ignore
    locale_path: Path = Path.cwd() / "locale"
    i18n.load_path.append(locale_path)  # type: ignore

    # Creating individual profiles
    user1_profile = Profile("Lucas", "fontisto:male")
    user2_profile = Profile("Nic", "fontisto:famale")

    # Creating combined household profile
    household_profile = HouseholdProfile(user1_profile, user2_profile)

    users: list[User] = [user1_profile]  # , user2_profile, household_profile]

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = Dash(
        __name__, external_stylesheets=[dbc_css, dbc.themes.DARKLY, dbc.icons.BOOTSTRAP]
    )
    app.title = i18n.t("general.app_title")  # type: ignore
    app.layout = layout.render(app, users)
    app.config["suppress_callback_exceptions"] = True
    app.scripts.config.serve_locally = True
    # server = app.server
    app.run(debug=True, port="8050")


if __name__ == "__main__":
    main()
