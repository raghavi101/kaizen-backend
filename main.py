from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_200_OK

import models
from database import SessionLocal, engine

app = FastAPI()

# Creates database tables
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

def get_db():
    try:
        db =  SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/api/register/", status_code=status.HTTP_201_CREATED)
def register(username: str, password: str, email: str, 
            profile_pic_url: str = "", db: Session = Depends(get_db)):
    new_user = models.User(username=username, email=email, profile_pic_url=profile_pic_url)
    new_user.hash_password(password)
    new_user.create_access_token(data={'username': username})
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User registered successfully!"
    }

@app.post("/api/login", status_code=status.HTTP_200_OK)
def login(username: str, password: str, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.verify_password(password) == False:
        return {"message": "Invalid credentials", "status": 503}
    return {
        "message": "Login successfull!",
        "token": user.jwt_token
    }

@app.get("/api/profile", 
    status_code=status.HTTP_200_OK)
def profile(username:str, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return {"message": "User credentials not found"}
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'profile_pic_url': user.profile_pic_url,
        'level': user.level,
        'token': user.jwt_token,
    }

@app.post("/api/add_friend", status_code=status.HTTP_201_CREATED)
def add_friend(id:int, fid: int, db: Session=Depends(get_db)):
    friend = models.Friend(pk=id, fk=fid)
    db.add(friend)
    db.commit()
    db.refresh(friend)
    return {
        'message': 'friend added successfully!'
    }

@app.post("/api/remove_friend", status_code=status.HTTP_201_CREATED)
def remove_friend(id:int, fid: int, db: Session=Depends(get_db)):
    friend = db.query(models.Friend).filter(models.Friend.pk==id, models.Friend.fk == fid).first()
    db.delete(friend)
    db.commit()
    db.refresh(friend)
    return {
        'message': 'friend removed successfully!'
    }


@app.get("/api/leaderboard", status_code=status.HTTP_200_OK)
def leaderboard(id:int, db: Session=Depends(get_db)):
    friends = db.query(models.Friend).filter(models.Friend.pk == id)
    leaderboard = {}
    for friend in friends:
        user = db.query(models.User).filter(models.User.id == friend.fk).first()
        leaderboard[user.username] = {
            'level': user.level,
            'time_watched': user.time_watched,
        }
    main_user = db.query(models.User).filter(models.User.id == id).first()
    leaderboard[main_user.username] = {
        'level': main_user.level,
        'time_watched': main_user.time_watched,
    }
    data = jsonable_encoder([leaderboard])
    return data

@app.get("/api/users", status_code=status.HTTP_200_OK)
def search(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    peeps = {}
    idx = 0
    for user in users:
        peeps[idx] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_pic_url': user.profile_pic_url,
            'level': user.level,
        }
        idx = idx + 1
    data = jsonable_encoder([peeps])
    return data

@app.get("/")
def index():
    return {
        "message": "Hello, World!"
    }