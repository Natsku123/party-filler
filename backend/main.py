import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from modules import crud, models, schemas


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}
