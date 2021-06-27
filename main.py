from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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