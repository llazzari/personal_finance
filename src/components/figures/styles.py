from plotly import graph_objects as go

COLOR_DISCRETE_SEQUENCE: list[str] = [
    "#DB8937",
    "#DB4F37",
    "#37DBCB",
    "#4E9C94",
    "#9C754E",
    "#9C594E",
    "#455C5A",
    "#5C5045",
    "#5C4845",
    "#293332",
]


def standardize(fig: go.Figure) -> None:
    fig.update_xaxes(title_font=dict(size=18), tickfont=dict(size=16))
    fig.update_yaxes(title_font=dict(size=18), tickfont=dict(size=16))

    fig.update_layout(legend=dict(font=dict(size=16)))
    fig.update_layout(height=400, width=550, margin=dict(l=10, r=10, t=40, b=40))


categories_palette: dict[str, str] = {
    "housing": "#DB8937",
    "transportation": "#DB4F37",
    "utilities": "#37DBCB",
    "food": "#4E9C94",
    "savings_debt_payments": "#9C754E",
    "health": "#9C594E",
    "personal_spending": "#455C5A",
    "entertainment": "#5C5045",
    "travel": "#5C4845",
    "miscellaneous": "#293332",
}

subcategories_palette: dict[str, str] = {
    "mortgage_rent": "#C87827",
    "home_maintenance": "#C77023",
    "property_taxes": "#C6671D",
    "home_purchases": "#C56017",
    "gas": "#B33D2C",
    "auto_insurance": "#B13A26",
    "auto_maintenance": "#AF371F",
    "auto_taxes_and_fees": "#AD3419",
    "public_transportation": "#AA3112",
    "ride_sharing": "#AA3112",
    "electricity": "#308F8F",
    "water": "#2F8C8A",
    "bank_fees": "#2E8886",
    "mobile_cell_phone": "#2D8582",
    "internet": "#2C827E",
    "groceries": "#3E7A6B",
    "dining_out": "#3D7965",
    "savings": "#7C6137",
    "debt_payments": "#7A5F31",
    "investments": "#785C2B",
    "health_insurance": "#793D2A",
    "health_plan": "#793C24",
    "medical_expenses": "#793A1E",
    "fitness": "#793817",
    "medications": "#793611",
    "supplements": "#793611",
    "clothing": "#3F4C50",
    "beauty_and_personal_care": "#3F4A49",
    "hobbies_and_recreation": "#3F4843",
    "subscriptions": "#3F463E",
    "studies": "#3F4536",
    "movies_and_shows": "#4E403B",
    "events_and_activities": "#4E3E34",
    "bars_pubs": "#4E3D2E",
    "transportation_travel": "#453A32",
    "lodging_travel": "#45392C",
    "other_travel_costs": "#453827",
    "gifts_and_donations": "#292B2A",
    "miscellaneous_expenses": "#292A24",
    "vacations": "#29291E",
    "pets": "#292818",
}
