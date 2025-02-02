from typing import Any, Protocol

import dash_mantine_components as dmc
import i18n
import pandas as pd
from dash import Input, Output, State, callback, callback_context, dcc, no_update
from dash_iconify import DashIconify

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
        Input(ids.PROFILE_BTN, "n_clicks"),
        *USER_INPUTS,
        State(ids.PROFILE_MODAL, "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal_opened(*inputs) -> bool:
        is_open = inputs[-1]
        return not is_open

    @callback(
        Output(ids.PROFILE_BTN, "children"),
        Input(ids.PROFILE_BTN, "n_clicks"),
        *USER_INPUTS,
        prevent_initial_call=True,
    )
    def update_profile_button(*_) -> DashIconify:
        triggered = callback_context.triggered[0]
        button_id = triggered["prop_id"].split(".")[0]
        user: User | None = USERS.get(button_id, None)

        if user is None:
            return create_icon("mdi:account")
        return create_icon(user.icon)

    @callback(
        Output(ids.MAINBODY, "children"),
        Input(ids.PROFILE_BTN, "n_clicks"),
        *USER_INPUTS,
        prevent_initial_call=True,
    )
    def update_main_body(*_) -> Any:
        triggered = callback_context.triggered[0]
        button_id = triggered["prop_id"].split(".")[0]
        user: User | None = USERS.get(button_id, None)

        if user is None:
            return no_update
        return tabs.render(user)

    @callback(
        Output(ids.ACTIVE_USER, "data"),
        Input(ids.PROFILE_BTN, "n_clicks"),
        *USER_INPUTS,
        prevent_initial_call=True,
    )
    def update_active_user(*_) -> Any:
        triggered = callback_context.triggered[0]
        button_id = triggered["prop_id"].split(".")[0]
        user: User | None = USERS.get(button_id, None)

        if user is None:
            return no_update
        return user.name

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
