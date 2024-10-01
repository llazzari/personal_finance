import dash_mantine_components as dmc
import i18n

from ..components import tables_tab, monthly_tab, evolution_tab


def render(user) -> dmc.Tabs:
    return dmc.Tabs(
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
            dmc.TabsPanel(
                tables_tab.render(
                    user.expenses.to_dict("records"), user.incomes.to_dict("records")
                ),
                value="tables",
            ),
            dmc.TabsPanel(monthly_tab.render(), value="monthly-dashboard"),
            dmc.TabsPanel(evolution_tab.render(), value="evolution-dashboard"),
        ],
        orientation="vertical",
        placement="left",
        value="tables",
    )
