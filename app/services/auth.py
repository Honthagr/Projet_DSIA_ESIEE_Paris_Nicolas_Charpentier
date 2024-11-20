import os

import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import User
from app import schemas, models

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM")


def _encode_jwt(user: User) -> str:
    return jwt.encode(
        {
            "user_id": str(user.id),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )


def generate_access_token(
    db: Session,
    email: str,
    password:str,
) -> schemas.auth_token:
    user = (
        db.query(models.User)
        .filter(
            models.User.email == email,
            models.User.password == password,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    return _encode_jwt(user)
