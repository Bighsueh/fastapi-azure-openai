from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from typing import List
import os
import openai

import mongoStore as db

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = os.environ.get("OPENAI_ENDPOINT")
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = APIRouter()

class RoleItem(BaseModel):
    role: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "role":"system",
                "content":"您現在是一位專門為國小三年級學生根據自然科目互動的聊天機器人，您的名字叫做「地球姊姊」。在與小朋友的對話中，您將根據提問內容，和小朋友進行持續的互動。您不可以主動向小朋友說再見，而且非常歡迎小朋友對回答的內容提出問題，您將竭盡所能地回答和解釋，讓小朋友更深入地了解"
            }
        }


@app.api_route(path="/callapi/chatGPT", summary='ChatGPT聊天功能', methods=["POST"])
async def chatGPT(temperature: float,
                  max_tokens: int,
                  top_p: float,
                  roles: List[RoleItem],
                  frequency_penalty: float,
                  presence_penalty: float,
                  stop: str,
                  past_messages: int,
                  purpose: str,
                  ):

    messages = [{"role": row.role, "content": row.content} for row in roles[-past_messages:]]

    stop_list = stop.split('-') if stop else None

    response = openai.ChatCompletion.create(
        engine="LC-gpt35turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop_list)

    db.insertJson(purpose, messages, response)

    return response

@app.api_route(path="/callapi/calTokenLength",summary='計算 token 數量',methods=["POST"])
async def calTokenLength(temperature: float,
                    top_p: float,
                    purpose : str,
                    roles: List[RoleItem],
                    ):

    messages = [{"role":row.role,"content":row.content} for row in roles]

    all_text = " ".join([msg["content"] for msg in messages])
    words = all_text.split()
    token_count = len(words)

    response = openai.ChatCompletion.create(
        engine="LC-gpt35turbo",
        messages = messages,
        temperature=temperature,
        max_tokens=token_count,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    
    total_count = response['usage']['total_tokens']
    
    return total_count

@app.api_route(path="/callapi/test",summary='測試功能',methods=["POST"] )
async def chatGPT():

    return {"data": {"choices": [{"message": "test"}]}}



