#uvicorn main:app --reload
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.put("/profile")
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