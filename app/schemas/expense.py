from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Expense(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    id_user: str
    name_user: str
    family_name_user: str
    price: float
    description: str
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
