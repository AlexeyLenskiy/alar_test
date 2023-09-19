from fastapi import FastAPI
import uvicorn
import os

from src.db.settings import init_db 

app = FastAPI()
host = os.getenv("APP_HOST")
port = int(os.getenv("APP_PORT"))



@app.get("/")
async def check_root():
    return {"sucess": True}

@app.on_event("startup")
async def on_startup():
   await init_db()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=host, port=port, log_level='info')
