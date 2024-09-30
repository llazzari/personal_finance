from dash import html, Dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import i18n

from . import tables_tab, monthly_tab, evolution_tab
from .modals import statement_modal, credit_card_modal, save_modal


def render(app: Dash, expenses: list[dict], incomes: list[dict]) -> dbc.Container:
    return dbc.Container(
        [
            html.H3(html.B(app.title), style={"margin-top": "20px"}),
            html.Hr(),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(
                                i18n.t("general.tables"),
                                value="tables",
                                className="tabs",
                            ),
                            dmc.Tab(
                                i18n.t("general.monthly_dashboard"),
                                value="monthly-dashboard",
                                className="tabs",
                            ),
                            dmc.Tab(
                                i18n.t("general.evolution_dashboard"),
                                value="evolution-dashboard",
                                className="tabs",
                            ),
                        ]
                    ),
                    dmc.TabsPanel(tables_tab.render(incomes, expenses), value="tables"),
                    dmc.TabsPanel(monthly_tab.render(), value="monthly-dashboard"),
                    dmc.TabsPanel(evolution_tab.render(), value="evolution-dashboard"),
                ],
                orientation="vertical",
                placement="left",
                value="tables",
            ),
            save_modal.render(),
            statement_modal.render(),
            credit_card_modal.render(),
            html.Div(style={"margin": "20px"}),
        ],
        class_name="dbc dbc-container tabs-container",
        fluid=True,
    )
