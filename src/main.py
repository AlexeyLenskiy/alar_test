from fastapi import FastAPI, Depends
import uvicorn
import os
from sqlalchemy.orm import Session

from src.db import data, settings, models

app = FastAPI()
host = os.getenv("APP_HOST")
port = int(os.getenv("APP_PORT"))



@app.get("/")
async def check_root():
    return {"sucess": True}

@app.on_event("startup")
async def on_startup():
   await data.init_db()

@app.get("/data", response_model=list[models.Data])
async def get_data(db: Session = Depends(settings.get_db)):
   return await data.get_sorted_data(
       db, 
       models=[
           models.Data1Model, 
           models.Data2Model, 
           models.Data3Model,
         ]
      )

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=host, port=port, log_level='info')
