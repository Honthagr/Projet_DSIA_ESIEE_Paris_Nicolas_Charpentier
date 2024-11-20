from fastapi import APIRouter, Depends, Response
from app.services import user as user_service
from app import schemas, models
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from app.routers.utils import checkSecurityandUserID


router = APIRouter(prefix="/user")

security = HTTPBearer()

@router.get("/balance", dependencies=[Depends(security)], tags=["user"])
async def balance(user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    return user_service.balance(user_id=user_id,db=db)

@router.get("/IBAN", dependencies=[Depends(security)], tags=["user"])
async def IBAN(user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    return user_service.IBAN(user_id=user_id,db=db)

@router.get("/historique", dependencies=[Depends(security)], tags=["user"])
async def historique(user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    return user_service.historique(user_id=user_id,db=db)

@router.post("/depense", dependencies=[Depends(security)], tags=["user"] )
async def depense(Amount: int, user_id = Depends(checkSecurityandUserID), db: Session = Depends(models.get_db)):
    return user_service.depense(user_id=user_id,Amount=Amount,db=db)

@router.post("/virement", dependencies=[Depends(security)], tags=["user"] )
async def viremennt(IBAN_User2: str, Amount: int, user_id = Depends(checkSecurityandUserID), db: Session = Depends(models.get_db)):
    return user_service.virement(user_id=user_id,db=db,IBAN_User2=IBAN_User2,Amount=Amount)

@router.post("/abonnement", dependencies=[Depends(security)], tags=["user"] )
async def abonnement(IBAN_User2: str, Amount: int, user_id = Depends(checkSecurityandUserID), db: Session = Depends(models.get_db)):
    return user_service.abonnement(user_id=user_id,db=db,IBAN_User2=IBAN_User2,Amount=Amount)

@router.delete("/delete_abonnement", dependencies=[Depends(security)], tags=["user"] )
async def delete_abonnement(ID_Subscription: str, user_id = Depends(checkSecurityandUserID), db: Session = Depends(models.get_db)):
    return user_service.delete_abonnement(user_id=user_id,db=db,ID_Subscription=ID_Subscription)

@router.post("/securite", dependencies=[Depends(security)], tags=["user"] )
async def securite(user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    return user_service.securite(user_id=user_id,db=db)

@router.delete("/delete", dependencies=[Depends(security)], tags=["user"] )
async def delete(response: Response,user_id = Depends(checkSecurityandUserID),db: Session = Depends(models.get_db)):
    user_service.delete(user_id=user_id,db=db)
    response.headers["Clear_token"] = "true"
    return {"message": "Authorization header cleared. Reauthenticate to continue."}