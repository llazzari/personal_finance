import os
from dash import Dash, html, Input, Output, dcc
import pandas as pd
import plotly.express as px
import i18n
import babel.dates
from datetime import datetime

from components import ids
from data.schema import DataSchema


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, 'children'),
        Input(ids.EXPENSES_TABLE, 'rowData')
    )
    def update_chart(data: dict) -> html.Div:
        df = pd.DataFrame.from_records(data)
        if df.empty:
            return html.Div(id=ids.BAR_CHART)

        dff = df.groupby(
            [DataSchema.YEAR, DataSchema.MONTH, DataSchema.RECURRENT]
        ).sum(numeric_only=True)
        dff.reset_index(inplace=True)
        dff[DataSchema.MONTH] = dff[DataSchema.MONTH].apply(
            convert_month_locale
        )
        fig = px.bar(
            dff,
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


def convert_month_locale(month_number: float) -> str:
    date = datetime(2000, int(month_number), 1)
    locale: str = os.environ['LOCALE']
    month: str = babel.dates.format_date(date, format='MMM', locale=locale)
    return month.capitalize().strip('.')
