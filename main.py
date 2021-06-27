<<<<<<< main
#uvicorn main:app --reload
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


@app.get("/profile")
def profile_details():
    return {"Hello": "World"}


@app.get("/leaderboard")
def read_item():
    pass

@app.get("/search")
def profile_details():
    pass

@app.get("/star")
def profile_details():
    pass


@app.post("/api/register/", status_code=status.HTTP_201_CREATED)
def register(username: str, password: str, db: Session = Depends(get_db)):
    new_user = models.User(username=username)
    new_user.hash_password(password)
    new_user.create_access_token(data={'username': username})
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User registered successfully!"
    }

@app.post("/api/login", status_code=status.HTTP_200_OK)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.verify_password(password) == False:
        return {"message": "Invalid credentials", "status": 503}
    return {
        "message": "Login successfull!",
        "token": user.jwt_token
    }

@app.get("/")
def index():
    return {
        "message": "Hello, World!"
    }
=======
#uvicorn main:app --reload
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


@app.get("/api/profile", "/{id}")
def profile_details(id: int, db: Session = Depends(get_db)):
    name = db.execute((models.User).select(models.User.name).where(models.User.c.id == id)).fetchall()
    profile_pic_url = db.execute((models.User).select(models.User.profile_pic).where(models.User.c.id == id)).fetchall()
    level = db.execute((models.User).select(models.User.level).where(models.User.c.id == id)).fetchall()
    watch_time = db.execute((models.User).select(models.User.time_watch).where(models.User.c.id == id)).fetchall()
    return{
        "name" : name,
        "profilepic" : profile_pic_url,
        "level" : level,
        "watch_time" : watch_time
    }


@app.get("/api/leaderboard")
def read_item(id: int, db: Session = Depends(get_db)):
    name = db.execute((models.User).select(models.User.name).where(models.User.c.id == id)).fetchall()
    level = db.execute((models.User).select(models.User.level).where(models.User.c.id == id)).fetchall()
    return{
        "name" : name,
        "level" : level,
    }

@app.get("/api/search")
def search_item(name: str, db: Session = Depends(get_db)):
    id = db.execute((models.User).filter(models.User.id).where(models.User.c.name == name)).fetchall
    name = db.execute((models.User).select(models.User.name).where(models.User.c.id == id)).fetchall()
    level = db.execute((models.User).select(models.User.level).where(models.User.c.id == id)).fetchall()
    #render_template("/api/profile")
    return{
        "name" : name,
        "level" : level,
    }



@app.get("/api/star")
def star_details(star: bool, db: Session = Depends(get_db)):
    if not star:
        return {"message" : "Add friend"}
    return {"star": star}


@app.post("/api/register/", status_code=status.HTTP_201_CREATED)
def register(username: str, password: str, db: Session = Depends(get_db)):
    new_user = models.User(username=username)
    new_user.hash_password(password)
    new_user.create_access_token(data={'username': username})
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User registered successfully!"
    }

@app.post("/api/login", status_code=status.HTTP_200_OK)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.verify_password(password) == False:
        return {"message": "Invalid credentials", "status": 503}
    return {
        "message": "Login successfull!",
        "token": user.jwt_token
    }

@app.get("/")
def index():
    return {
        "message": "Hello, World!"
    }
>>>>>>> local
 