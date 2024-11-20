from fastapi import APIRouter, Depends
from app.services import config_account as config_service
from app import schemas, models
from sqlalchemy.orm import Session
from app.schemas.auth_token import AuthToken
from fastapi.security import HTTPBearer

router = APIRouter()

security = HTTPBearer()

@router.post("/nouveau_user", tags=["accueil"])
async def new_account(user:schemas.User, password_admin:int = None, db: Session = Depends(models.get_db)):
    return config_service.new_account(user=user,db=db,password_admin=password_admin)

@router.get("/connection", tags=["accueil"])
async def login(email:str, password:str,db: Session = Depends(models.get_db)) -> AuthToken:
    return config_service.login(db=db,email=email,password=password)