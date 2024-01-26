from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    status: Optional[str] = "Active"

    class Config():
        orm_mode = True
