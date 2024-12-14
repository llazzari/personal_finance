import dash_mantine_components as dmc
import i18n

from . import dashboard_tab

from ..components import tables_tab


def render(user) -> dmc.Tabs:
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab(
                        "Dashboard",
                        value="dashboard",
                        className="tabs",
                    ),
                    dmc.Tab(
                        i18n.t("general.tables"),
                        value="tables",
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
            dmc.TabsPanel(dashboard_tab.render(), value="dashboard"),
        ],
        orientation="horizontal",
        placement="center",
        value="dashboard",
    )
