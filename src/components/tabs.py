import dash_mantine_components as dmc
import i18n

from src.data.schema import Transaction

from ..components import tables_tab
from . import dashboard_tab


def render(transactions: list[Transaction]) -> dmc.Tabs:
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
                tables_tab.render(transactions),
                value="tables",
            ),
            dmc.TabsPanel(dashboard_tab.render(), value="dashboard"),
        ],
        orientation="horizontal",
        placement="center",
        value="dashboard",
    )
