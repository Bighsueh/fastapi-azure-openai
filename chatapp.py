from fastapi import FastAPI,APIRouter
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


@app.post(path="/callapi/chatGPT",summary='ChatGPT聊天功能')
async def chatGPT(temperature: float,
                    max_tokens: int,
                    top_p: float,
                    purpose : str,
                    roles: List[RoleItem],
                    ):

    messages = [{"role":row.role,"content":row.content} for row in roles]

    response = openai.ChatCompletion.create(
        engine="LC-gpt35turbo",
        messages = messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    
    db.insertJson(purpose,messages,response)
    
    return response




