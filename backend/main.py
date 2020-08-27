import os

from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{username}:{password}@{server}/{db}".format(
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    server="db",
    db=os.environ.get("DB_NAME")
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}
