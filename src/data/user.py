from pathlib import Path
import pandas as pd

from src.data.schema import DataSchema

DATABASE_PATH: Path = Path.cwd() / "database"


class Profile:
    def __init__(self, name: str, icon: str) -> None:
        self.name: str = name
        self.icon: str = icon
        self.expenses = self.load_data(DATABASE_PATH / f"{name.lower()}_expenses.csv")
        self.incomes = self.load_data(DATABASE_PATH / f"{name.lower()}_incomes.csv")

    def load_data(self, file_path: Path) -> pd.DataFrame:
        """
        Load data from a file and return it as a pandas DataFrame.

        Parameters:
            file_path (Path): The path to the file to be loaded.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame. If the file does not exist, an empty DataFrame is returned.

        Examples:
            >>> file_path = Path("data.csv")
            >>> load_data(file_path)
                YEAR  MONTH  AMOUNT  BANK  CATEGORY  SUBCATEGORY  RECURRENT  DESCRIPTION  id
            0   2021      1   100.0    A         B             C         D        E1        0
            1   2021      2   200.0    A         B             C         D        E2        1
            2   2021      3   300.0    A         B             C         D        E3        2

        Notes:
            - The DataFrame returned has an additional column 'id' which contains the index of each row.
            - The DataFrame is sorted by date before being returned.
        """

        if not file_path.exists():
            return pd.DataFrame()

        dtype: dict[str, type] = {
            DataSchema.YEAR: int,
            DataSchema.MONTH: int,
            DataSchema.AMOUNT: float,
            DataSchema.BANK: str,
            DataSchema.CATEGORY: str,
            DataSchema.SUBCATEGORY: str,
            DataSchema.RECURRENT: str,
            DataSchema.DESCRIPTION: str,
        }
        df: pd.DataFrame = pd.read_csv(
            file_path,
            dtype=dtype,
            usecols=list(dtype.keys()),
        )
        df["id"] = df.index
        return self.sort_by_date(df)

    def sort_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df.sort_values(
            by=[DataSchema.YEAR, DataSchema.MONTH],
            ascending=False,
            inplace=True,
        )
        return df


class HouseholdProfile:
    def __init__(self, profile1: Profile, profile2: Profile) -> None:
        self.name: str = "Household"
        self.icon: str = "fontisto:home"
        self.expenses = self.combine_data(profile1.expenses, profile2.expenses)
        self.incomes = self.combine_data(profile1.incomes, profile2.incomes)

    def combine_data(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """Combine data from both profiles."""
        combined = pd.concat([df1, df2], ignore_index=True)
        if combined.empty:
            return combined
        return combined.sort_values(
            by=[DataSchema.YEAR, DataSchema.MONTH], ascending=False
        )
