from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel;


app = FastAPI()


@app.get('/')
def index():
    return {'data': {"name": 'shark'}}


@app.get('/about/{id}')
def about(id: int, type: str):
    return {'data': 'this s return from about ', 'id': {id}, 'type': type}


@app.get('/blog/{id}')
def blog(id: str = 'hi', sorting: Optional[str] = None):
    if sorting:
        return {'data': 'this a blog return with sorting', 'id': id, sorting: sorting}
    else:
        return {'data': "this an about with no sorting params", 'id': id}

@app.get('/blog/{id}/comments')
def blog(id: str = 'hi', sorting: Optional[str] = None):
    if sorting:
        return {'data': 'this a blog comments return with sorting', 'id': id, sorting: sorting}
    else:
        return {'data': "this an about ammount with no sorting params", 'id': id}

class Blog (BaseModel):
    title : str
    body:str
    published : Optional[bool] 

@app.post('/blog')
def createBlog(blog :Blog):
    return {'data':f"request of blog {blog.title} is"}


        

