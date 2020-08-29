from fastapi import FastAPI

from modules.endpoints.parties import router as party_router


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


app.include_router(party_router, prefix="/parties")
