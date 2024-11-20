from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from app.models.database import BaseSQL


class Transfer(BaseSQL):
    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    id_user = Column(String)
    IBAN_user2 = Column(String)
    name_user1 = Column(String)
    family_name_user1 = Column(String)
    price = Column(Float)
    description = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
