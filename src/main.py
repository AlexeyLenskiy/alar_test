from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()
host = os.getenv("HOST", default="127.0.0.1")
port = int(os.getenv("PORT", default=8088))



@app.get("/")
def check_root():
    return {"sucess": True}

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=host, port=port, log_level='info')
