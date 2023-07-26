from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from chatapp import app as chatapp


app = FastAPI(title = 'Wulab Openai 服務平台',description = '透過 api 快速調用 openai 服務')            # 以app作為FastAPI實例
api_router = APIRouter()   # 以api_router作為APIRouter實例，本次重點!

api_router.include_router(chatapp) 

app.include_router(api_router)            # app實例將api_router的路由結合進去

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)