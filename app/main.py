from fastapi import FastAPI
from app.api import endpoints
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://your_username:your_password@localhost/timetracker_db"






app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hola caracola"}