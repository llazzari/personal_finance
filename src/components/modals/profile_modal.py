from dash import callback, Output, Input, State, callback_context
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import i18n

from .. import ids

PROFILES_SIZES = 50
PROFILE_BUTTONS_ICONS: dict[str, str] = {
    ids.PROFILE_BTN: "mdi:account",
    ids.USER_ONE_BTN: "fontisto:male",
    ids.USER_TWO_BTN: "fontisto:famale",
    ids.USER_HOUSEHOLD_BTN: "fontisto:home",
}


def create_icon(id_: str) -> DashIconify:
    return DashIconify(
        icon=PROFILE_BUTTONS_ICONS[id_], width=PROFILES_SIZES, height=PROFILES_SIZES
    )


def create_action_icon(id_: str) -> dmc.ActionIcon:
    return dmc.ActionIcon(
        create_icon(id_),
        id=id_,
        size="xl",
        radius="xl",
        variant="subtle",
        mt=10,
    )


def render() -> dmc.Modal:
    return dmc.Modal(
        title=i18n.t("general.profile"),
        id=ids.PROFILE_MODAL,
        size="35%",
        children=[
            dmc.Group(
                [
                    create_action_icon(ids.USER_ONE_BTN),
                    create_action_icon(ids.USER_TWO_BTN),
                    create_action_icon(ids.USER_HOUSEHOLD_BTN),
                ],
                position="center",
                grow=True,
            )
        ],
    )


@callback(
    Output(ids.PROFILE_MODAL, "opened"),
    Output(ids.PROFILE_BTN, "children"),
    Input(ids.PROFILE_BTN, "n_clicks"),
    Input(ids.USER_ONE_BTN, "n_clicks"),
    Input(ids.USER_TWO_BTN, "n_clicks"),
    Input(ids.USER_HOUSEHOLD_BTN, "n_clicks"),
    State(ids.PROFILE_MODAL, "opened"),
    prevent_initial_call=True,
)
def toggle_modal(
    n1: int, n2: int, n3: int, n4: int, is_open: bool
) -> tuple[bool, DashIconify]:
    triggered = callback_context.triggered[0]
    button_id = triggered["prop_id"].split(".")[0]

    return not is_open, DashIconify(
        icon=PROFILE_BUTTONS_ICONS[button_id],
        width=PROFILES_SIZES,
        height=PROFILES_SIZES,
    )
