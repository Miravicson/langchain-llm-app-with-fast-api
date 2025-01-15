""" Getting started with langchain """

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Union, cast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()


def dumb_translate():
    """Translate hardcoded text"""
    model = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage("Translate the following from English to Italian"),
        HumanMessage("Good morning"),
    ]

    response = model.invoke(messages)
    print(response.content)
    return response


def translate(language: str, text_to_translate: str):
    """Allows user to specify both the text and the language for translation"""
    model = ChatOpenAI(model="gpt-4o-mini")

    system_template = "Translate the following from English into {language}"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    prompt = prompt_template.invoke({"language": language, "text": text_to_translate})

    print(prompt.to_messages())
    response = model.invoke(prompt)
    print(response.content)

    return cast(str, response.content)


class Input(BaseModel):
    text: str
    language: str


class Output(BaseModel):
    output: str


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q, "message": "Hey there"}


@app.post("/conversation")
async def input(input: Input):
    output = Output(output=translate(language=input.language, text_to_translate=input.text))
    return output


origins = ["<http://localhost>", "<http://localhost:5173>"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

