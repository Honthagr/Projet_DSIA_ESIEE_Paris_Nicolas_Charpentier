from fastapi import APIRouter, Depends, Response, HTTPException
from app.services import admin as admin_service
from app import schemas, models
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.security import HTTPBearer
from app.routers.utils import checkSecurityandUserID

router = APIRouter(prefix="/admin")

security = HTTPBearer()

@router.get("/members", dependencies=[Depends(security)], tags=["admin"])
async def get_members(user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    return admin_service.get_members(user_id=user_id,db=db)

@router.delete("/delete_all_members", dependencies=[Depends(security)], tags=["admin"])
async def delete_all_members(response: Response, user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    admin_service.delete_all_members(user_id=user_id,db=db)
    response.headers["Clear_token"] = "true"
    return {"message": "Authorization header cleared. Reauthenticate to continue."}

@router.post("/admin_transaction", dependencies=[Depends(security)], tags=["admin"])
async def admin_transaction(Amount:int, IBAN_Member:str, user_id = Depends(checkSecurityandUserID), db: Session = Depends(models.get_db)):
    return admin_service.admin_transaction(Amount=Amount,user_id=user_id,IBAN_Member=IBAN_Member,db=db)