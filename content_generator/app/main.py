from fastapi import FastAPI , Request , Depends
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session

import models, crud, database, utility, schemas

from database import engine, SessionLocal

from starlette.concurrency import run_in_threadpool


models.base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")