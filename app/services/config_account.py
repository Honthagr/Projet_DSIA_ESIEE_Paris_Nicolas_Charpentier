from pydantic import Field
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import models, schemas
from app.services.auth import generate_access_token
from uuid import uuid4
import string
import random
from datetime import datetime
from app.schemas.auth_token import AuthToken

def generate_iban():
    """Generate a random 20-character IBAN."""
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))


def new_account(db: Session, user: schemas.User, password_admin:int) -> models.User:
    record = db.query(models.User).filter(models.User.email == user.email).first()
    if record:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    typeUser = 0
    if password_admin == 9999:
        typeUser = 1

    db_user = models.User(
        id = str(uuid4()),
        name = user.name,
        family_name = user.family_name,
        email = user.email,
        password=user.password,
        money=1000,
        IBAN=generate_iban(),
        Lock=False,
        typeAccount = typeUser,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.id = str(db_user.id)
    return db_user

def login(email:str,password:str,db: Session) -> schemas.auth_token:

    token = generate_access_token(db,email=email,password=password)

    return AuthToken(access_token=token)

