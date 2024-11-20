from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Transfer(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    id_user: str
    IBAN_user2: str
    name_user1: str
    family_name_user1: str
    price: float
    description: str
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
