from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..oautth2 import get_current_user


router = APIRouter(
    tags=['blogs'],
    prefix='/blogs'
)


@router.get('')
def getBlogs(db: Session = Depends(database.get_db ) , current_user : schemas.TokenData = Depends(get_current_user)):

    blogs = db.query(models.Blog).all()
    return blogs


@router.post('', status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}')
def getById(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "details": f"Blog with Id {id} not founded "})
    return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, response: Response, db: Session = Depends(database.get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False
                                                              )
    db.commit()

    return "done"


@router.put('/{id}')
def updateBlog(id, request: schemas.Blog, response: Response, db: Session = Depends(database.get_db)):
    print(request)
    db.query(models.Blog).filter(models.Blog.id == id).update(
        {'body': request.body, "title": request.title})
    db.commit()
    return 'updated'
