from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatapp import app as chatapp


app = FastAPI(title = 'Wulab Openai 服務平台',description = '透過 api 快速調用 openai 服務')            # 以app作為FastAPI實例
api_router = APIRouter()   # 以api_router作為APIRouter實例，本次重點!

api_router.include_router(chatapp) 

app.include_router(api_router)            # app實例將api_router的路由結合進去

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中，应指定允许的域名，例如["https://example.com"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有标头
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)