from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.database import BaseSQL


class User(BaseSQL):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    family_name = Column(String)
    email = Column(String)
    password = Column(String)
    money = Column(Float)
    IBAN = Column(String)
    Lock = Column(Boolean)
    typeAccount = Column(Integer)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
