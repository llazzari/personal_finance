from dash import Dash, html, Input, Output, dcc
import plotly.express as px
import i18n

from components import ids
from data.schema import DataSchema
from data.source import DataSource


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, 'children'),
        Input(ids.EXPENSES_TABLE, 'rowData')
    )
    def update_chart(data: list[dict]) -> html.Div:
        source = DataSource(data)
        df = source.expense_evolution()

        fig = px.bar(
            df,
            x=DataSchema.MONTH,
            y=DataSchema.AMOUNT,
            color=DataSchema.RECURRENT,
            labels={
                DataSchema.MONTH: i18n.t(f'columns.{DataSchema.MONTH}'),
                DataSchema.AMOUNT: i18n.t(f'columns.{DataSchema.AMOUNT}'),
                DataSchema.RECURRENT: i18n.t(f'columns.{DataSchema.RECURRENT}')
            },
            # text=DataSchema.RECURRENT
            category_orders={
                DataSchema.RECURRENT: [
                    i18n.t(f'general.recurrent_{option}') for option in [
                        'yes', 'no'
                    ]
                ]
            },
            color_discrete_sequence=['#56A697', '#D9483B']
        )
        fig.update_layout(xaxis_type='category')
        return html.Div(
            dcc.Graph(figure=fig),
            id=ids.BAR_CHART,
        )
    return html.Div(id=ids.BAR_CHART)
