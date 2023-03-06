from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, hashing, models, database


router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@router.post('', response_model=schemas.ShowUser)
def createUser(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def getUser(id, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "details": f"Blog with Id {id} not founded "})

    return user
