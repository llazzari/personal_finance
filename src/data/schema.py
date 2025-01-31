from pydantic import BaseModel, Field


class DataSchema:
    """Column names that are used throughout the app."""

    AMOUNT = "amount"
    CATEGORY = "category"
    SUBCATEGORY = "subcategory"
    DATE = "date"
    DESCRIPTION = "description"
    YEAR = "year"
    MONTH = "month"
    BANK = "bank"
    RECURRENT = "recurrent"
    CLEANED_DESCRIPTION = "cleaned_description"
    TYPE = "type"


class Transaction(BaseModel):
    description: str = Field(alias="Description", description="Transaction description")
    amount: float = Field(alias="Amount", description="Transaction amount")
    date: int = Field(alias="Date", description="The date in unix time")
    bank: str = Field(alias="Bank", description="Bank name")
