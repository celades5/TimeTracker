from fastapi import FastAPI
from app.api.endpoints import tasks
from app.models import models
from app.models.database import engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "postgresql://your_username:your_password@localhost/timetracker_db"



models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "hola caracola"}