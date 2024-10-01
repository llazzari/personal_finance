from typing import Protocol, Any
import pandas as pd
from dash import callback, Output, Input, State, callback_context, no_update, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import i18n

from .. import ids, tabs


class User(Protocol):
    name: str
    icon: str
    expenses: pd.DataFrame
    incomes: pd.DataFrame


ICON_SIZE = 50


def create_icon(icon: str) -> DashIconify:
    return DashIconify(icon=icon, width=ICON_SIZE, height=ICON_SIZE)


def create_action_icon(user: User) -> dmc.ActionIcon:
    return dmc.ActionIcon(
        create_icon(user.icon),
        id=user.name,
        size="xl",
        radius="xl",
        variant="subtle",
        mt=10,
    )


def render(users: list[User]) -> dmc.Modal:
    USER_INPUTS = [Input(user.name, "n_clicks") for user in users]
    USERS = {user.name: user for user in users}

    @callback(
        Output(ids.PROFILE_MODAL, "opened"),
        Output(ids.PROFILE_BTN, "children"),
        Output(ids.MAINBODY, "children"),
        Output(ids.ACTIVE_USER, "data"),
        Input(ids.PROFILE_BTN, "n_clicks"),
        *USER_INPUTS,
        State(ids.PROFILE_MODAL, "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal(*inputs) -> tuple[bool, DashIconify, Any, Any]:
        is_open = inputs[-1]

        triggered = callback_context.triggered[0]
        button_id = triggered["prop_id"].split(".")[0]
        user: User | None = USERS.get(button_id, None)

        if user is None:
            return not is_open, create_icon("mdi:account"), no_update, no_update

        return (not is_open, create_icon(user.icon), tabs.render(user), user.name)

    return dmc.Modal(
        title=i18n.t("general.profile"),
        id=ids.PROFILE_MODAL,
        size="35%",
        opened=True,
        children=[
            dmc.Group(
                [create_action_icon(user) for user in users],
                position="center",
                grow=True,
            ),
            dcc.Store(id=ids.ACTIVE_USER, data=None, storage_type="session"),
        ],
    )
