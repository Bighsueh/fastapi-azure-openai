from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
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


@app.post(path="/callapi/roleplay",summary='ChatGPT角色扮演')
async def roleplay(temperature: float,
                    max_tokens: int,
                    top_p: float,
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
    
    db.insertJson(messages,response)
    
    return response




