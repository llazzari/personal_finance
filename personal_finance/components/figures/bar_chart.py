from dash import callback, html, Input, Output, dcc
import plotly.express as px
import i18n

from components import ids
from data.schema import DataSchema
from data.source import DataSource


def render() -> html.Div:
    return html.Div(id=ids.BAR_CHART)


@callback(
    Output(ids.BAR_CHART, 'children'),
    Input(ids.EXPENSES_TABLE, 'rowData'),
    Input(ids.INCOMES_TABLE, 'rowData')
)
def update_chart(expenses: list[dict], incomes: list[dict]) -> html.Div:
    if not expenses and not incomes:
        return html.Div(id=ids.BAR_CHART)
    for e in expenses:
        e[DataSchema.TYPE] = i18n.t('general.expenses')
    for i in incomes:
        i[DataSchema.TYPE] = i18n.t('general.incomes')

    data: list[dict] = expenses + incomes
    source = DataSource(data)
    df = source.evolution()

    fig = px.bar(
        df,
        x=DataSchema.MONTH,
        y=DataSchema.AMOUNT,
        color=DataSchema.TYPE,
        # pattern_shape=DataSchema.RECURRENT,
        labels={
            DataSchema.MONTH: i18n.t(f'columns.{DataSchema.MONTH}'),
            DataSchema.AMOUNT: i18n.t(f'columns.{DataSchema.AMOUNT}'),
            DataSchema.RECURRENT: i18n.t(f'columns.{DataSchema.RECURRENT}'),
            DataSchema.TYPE: i18n.t(f'columns.{DataSchema.TYPE}'),
        },
        text=DataSchema.RECURRENT,
        category_orders={
            DataSchema.RECURRENT: [
                i18n.t(f'general.recurrent_{option}') for option in [
                    'yes', 'no'
                ]
            ],
            DataSchema.TYPE: [
                i18n.t(f'general.{typee}') for typee in ['incomes', 'expenses']
            ],
        },
        color_discrete_sequence=['#56A697', '#D9483B'],
        barmode='group'
    )
    fig.update_layout(xaxis_type='category')
    return html.Div(
        dcc.Graph(figure=fig),
        id=ids.BAR_CHART,
    )
