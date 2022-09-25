from fastapi import FastAPI
from app.database import (
    Base, 
    create_mysql_database_if_not_exists, 
    engine)

from app.router import user_router
from app.auth import authentication
import logging
logger = logging.getLogger('uvicorn')


app = FastAPI(debug = True)

app.include_router(user_router.router)
app.include_router(authentication.router)

@app.on_event("startup")
def init_project():

    logger.info("Starting Project")
    create_mysql_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    logger.info("Starting Project Success.")

@app.get("/")
async def root():
    return {"message": "success"}