CATEGORIES: dict[str, list[str]] = {
    "housing": [
        "mortgage_rent",
        "home_maintenance",
        "property_taxes",
        "home_purchases",
    ],
    "transportation": [
        "gas",
        "auto_insurance",
        "auto_maintenance",
        "auto_taxes_and_fees",
        "public_transportation",
        "ride_sharing",
    ],
    "utilities": ["electricity", "water", "bank_fees", "mobile_cell_phone", "internet"],
    "food": ["groceries", "dining_out"],
    "savings_debt_payments": ["savings", "debt_payments", "investments"],
    "health": [
        "health_insurance",
        "health_plan",
        "medical_expenses",
        "fitness",
        "medications",
        "supplements",
    ],
    "personal_spending": [
        "clothing",
        "beauty_and_personal_care",
        "hobbies_and_recreation",
        "subscriptions",
        "studies",
    ],
    "entertainment": ["movies_and_shows", "events_and_activities", "bars_pubs"],
    "travel": ["transportation_travel", "lodging_travel", "other_travel_costs"],
    "miscellaneous": [
        "gifts_and_donations",
        "miscellaneous_expenses",
        "vacations",
        "pets",
    ],
}

RECURRENT_SUBCATEGORIES: list[str] = [
    "mortgage_rent",
    "auto_insurance",
    "electricity",
    "water",
    "internet",
    "bank_fees",
    "mobile_cell_phone",
    "groceries",
    "health_plan",
    "health_insurance",
    "fitness",
    "subscriptions",
    "gas",
]
