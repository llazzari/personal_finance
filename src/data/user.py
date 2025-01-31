from pathlib import Path

from pydantic import BaseModel, Field

DATABASE_PATH: Path = Path.cwd() / "database"


class User(BaseModel):
    id: int = Field(description="The ID of the user", ge=1)
    name: str = Field(description="The name of the user")
    email: str = Field(email=True, description="The email of the user")
    icon: str = Field(description="The icon of the user")
