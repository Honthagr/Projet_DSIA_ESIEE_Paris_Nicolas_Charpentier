from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import models
from uuid import uuid4
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.db import get_db

def checkLockedAccount(db:Session,user_id: str):
    checkLock = db.query(models.User).filter(models.User.id == user_id).first()
    if not checkLock:
        raise HTTPException(status_code=404, detail=f"User not found")
    IsLocked = checkLock.Lock

    if IsLocked == True:
        raise HTTPException(status_code=401, detail=f"This account is locked, you can't do this operation. Unlock this account if you want to proceed.")
    return

def balance(db:Session,user_id: str) -> int:
    record = db.query(models.User).filter(models.User.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"User not found")
    Amount = record.money
    return Amount

def IBAN(db:Session,user_id: str) -> str:
    record = db.query(models.User).filter(models.User.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"User not found")
    UserIBAN = record.IBAN
    return UserIBAN

def historique(db:Session,user_id: str) -> List:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    record1 = db.query(models.Expense).filter(models.Expense.id_user == user_id).all()
    record2 = db.query(models.Transfer).filter(models.Transfer.id_user == user_id).all()
    record3 = db.query(models.Transfer).filter(models.Transfer.IBAN_user2 == user.IBAN).all()
    record4 = db.query(models.Subscription).filter(models.Subscription.id_user == user_id).all()
    record5 = db.query(models.Subscription).filter(models.Subscription.IBAN_user2 == user.IBAN).all()
    for record in record1:
        record.id = str(record.id)
    for record in record2:
        record.id = str(record.id)
    for record in record3:
        record.id = str(record.id)
    for record in record4:
        record.id = str(record.id)
    for record in record5:
        record.id = str(record.id)
    return [record1, record2, record3, record4, record5]

def depense(Amount:int,db:Session,user_id: str) -> models.Expense:
    checkLockedAccount(db,user_id)
    
    if Amount < 0 :
        raise HTTPException(status_code=401, detail=f"Can't have a negative expense")
    
    record = db.query(models.User).filter(models.User.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"User not found")
    record.money -= Amount
    record.updated_at = datetime.now()

    db_expense = models.Expense(
        id = str(uuid4()),
        id_user = user_id,
        name_user = record.name,
        family_name_user = record.family_name,
        price=Amount,
        description="Expense from this account",
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db.add(db_expense)
    db.add(record)
    db.commit()
    db.refresh(record)
    db.refresh(db_expense)
    return db_expense

def virement(user_id:str,db:Session,IBAN_User2:str,Amount:int) -> models.Transfer:
    checkLockedAccount(db,user_id)
    
    if Amount < 0 :
        raise HTTPException(status_code=409, detail=f"Can't have a negative expense")
    
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User 1 not found")
    db_user2 = db.query(models.User).filter(models.User.IBAN == IBAN_User2).first()
    if not db_user2:
        raise HTTPException(status_code=404, detail=f"Wrond IBAN")
    
    if db_user.money < Amount:
        raise HTTPException(status_code=409, detail=f"Your account doesn't have enough money to proceed this transfer.")

    db_transfer = models.Transfer(
        id = str(uuid4()),
        id_user = user_id,
        IBAN_user2=IBAN_User2,
        name_user1 = db_user.name,
        family_name_user1 = db_user.family_name,
        price=Amount,
        description="Transfer from "+ db_user.name + " " + db_user.family_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db_user.updated_at = datetime.now()
    db_user.money -= Amount

    db_user2.updated_at = datetime.now()
    db_user2.money += Amount

    db.add(db_transfer)
    db.add(db_user2)
    db.add(db_user)
    db.commit()
    db.refresh(db_transfer)
    db.refresh(db_user2)
    db.refresh(db_user)    
    return db_transfer

def abonnement(user_id:str,db:Session,IBAN_User2:str,Amount:int):
    checkLockedAccount(db,user_id)
    
    if Amount < 0 :
        raise HTTPException(status_code=409, detail=f"Can't have a negative expense")
    
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User not found")

    if db_user.money < Amount:
        raise HTTPException(status_code=409, detail=f"Your account doesn't have enough money to proceed this transfer.")
    
    db_subscription = models.Subscription(
        id = str(uuid4()),
        id_user = user_id,
        IBAN_user2=IBAN_User2,
        name_user1 = db_user.name,
        family_name_user1 = db_user.family_name,
        price=Amount,
        description="Subscription from "+ db_user.name + " " + db_user.family_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def delete_abonnement(user_id:str,ID_Subscription:str,db:Session) -> str:
    checkLockedAccount(db,user_id)
    db_subscription= db.query(models.Subscription).filter(models.Subscription.id_user==user_id and models.Subscription.id==ID_Subscription).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail=f"Subscription not found")
    db.delete(db_subscription)
    db.commit()
    return {f"Subscription deleted"}

def securite(db:Session,user_id: str):
    record = db.query(models.User).filter(models.User.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Account not found")
    record.Lock = not record.Lock
    record.updated_at = datetime.now()
    db.add(record)
    db.commit()
    db.refresh(record)
    if record.Lock == True:
        return {"message":"The account is now Locked"}
    else:
        return {"message":"The account is no longer Locked"}

def delete(db:Session,user_id: str):
    checkLockedAccount(db,user_id)
    record = db.query(models.User).filter(models.User.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Account not found")
    db.delete(record)
    db.commit()
    return {f"Account deleted"}


## Done with ChatGPT

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

def process_subscriptions():
    """
    Process all active subscriptions every minute.
    """
    try:  # Open a new session for each job
        db = next(get_db())
        subscriptions = db.query(models.Subscription).all()

        for sub in subscriptions:
            # Fetch user details
            user = db.query(models.User).filter(models.User.id == sub.id_user).first()
            if not user:
                print(f"Missing an User in the database. Got Deleted")
                db.delete(sub)
                db.commit()
                continue

            # Fetch recipient user details
            recipient = db.query(models.User).filter(models.User.IBAN == sub.IBAN_user2).first()
            if not recipient:
                print(f"Missing an User in the database. Got Deleted")
                db.delete(sub)
                db.commit()
                continue

            # Check user's balance
            if user.money < sub.price:
                print(f"User {user.id} has insufficient funds for subscription {sub.id}.")
                db.delete(sub)
                db.commit()               
                continue

            # Create a transfer record
            transfer = models.Transfer(
                id=str(uuid4()),
                id_user=user.id,
                IBAN_user2=sub.IBAN_user2,
                name_user1=user.name,
                family_name_user1=user.family_name,
                price=sub.price,
                description=sub.description,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            # Update user balances
            user.money -= sub.price
            recipient.money += sub.price
            user.updated_at = datetime.now()
            recipient.updated_at = datetime.now()

            # Save changes to the database
            db.add(transfer)
            db.add(user)
            db.add(recipient)
            db.commit()
            db.refresh(transfer)
            db.refresh(user)
            db.refresh(recipient)

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error while processing subscription")