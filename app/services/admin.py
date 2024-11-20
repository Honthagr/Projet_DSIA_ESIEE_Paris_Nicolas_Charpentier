from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import models
from uuid import uuid4


def checkAdminAccount(db:Session,user_id: str):
    checktype = db.query(models.User).filter(models.User.id == user_id).first()
    if not checktype:
        raise HTTPException(status_code=404, detail=f"User Not Found")
    usertype = checktype.typeAccount

    if usertype == 0:
        raise HTTPException(status_code=401, detail=f"Your account doesn't have the right to do that")
    return

def get_members(db:Session,user_id: str) -> List[models.User]:
    checkAdminAccount(db,user_id)
    records = db.query(models.User).filter().all()
    for record in records:
        record.id = str(record.id)
    return records

def delete_all_members(db:Session,user_id: str) -> List[models.User]:
    checkAdminAccount(db,user_id)
    records = db.query(models.User).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records

def admin_transaction(Amount:int,IBAN_Member:str,db:Session,user_id: str) -> models.Transfer:
    checkAdminAccount(db,user_id)
    db_user2 = db.query(models.User).filter(models.User.IBAN == IBAN_Member).first()
    if not db_user2:
        raise HTTPException(status_code=404, detail=f"Wrond IBAN")
    
    db_transfer = models.Transfer(
        id = str(uuid4()),
        id_user = 0,
        IBAN_user2=IBAN_Member,
        name_user1 = "Admin",
        family_name_user1 = "Admin",
        price=Amount,
        description="Transaction from Admin Account",
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db_user2.updated_at = datetime.now()
    db_user2.money += Amount

    db.add(db_transfer)
    db.add(db_user2)
    db.commit()
    db.refresh(db_transfer)
    db.refresh(db_user2)    
    return db_transfer