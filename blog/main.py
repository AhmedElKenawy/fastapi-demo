from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from . import schemas, models, hashing
from sqlalchemy.orm import Session
from .database import engine, sessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def getBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def getById(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "details": f"Blog with Id {id} not founded "})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details" :f"Blog with Id {id} not founded "}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, response: Response, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False
                                                              )
    db.commit()

    return "done"


@app.put('/blog/{id}')
def updateBlog(id, request: schemas.Blog, response: Response, db: Session = Depends(get_db)):
    print(request)
    db.query(models.Blog).filter(models.Blog.id == id).update(
        {'body': request.body, "title": request.title})
    db.commit()
    return 'updated'


@app.post('/user', response_model=schemas.ShowUser)
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser)
def getUser(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "details": f"Blog with Id {id} not founded "})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details" :f"Blog with Id {id} not founded "}
    return user
