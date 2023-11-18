import logging
import json
import os

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from retriever import fetch_projects
from chat import get_agent_executor
from prompt_io import parse_response

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:3000",  # React front-end URL
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str
    chat_uuid: str 
  

chats = dict()


@app.post("/chat")
async def chat(query: Query = Body(...)):
    if query.chat_uuid in chats:
        logging.info(f"Fetching saved chat with ID: {query.chat_uuid}")
        agent_executor = chats[query.chat_uuid]
    else:
        logging.info(f"Creating new chat with ID: {query.chat_uuid}")
        agent_executor = get_agent_executor()
        chats[query.chat_uuid] = agent_executor
    
    response = agent_executor.invoke({"input": query.text})
    logging.info("Agent response", response)
    response = parse_response(response["output"])

    projects = fetch_projects(response["projectUUIDs"].split(","))
    server_response = {"answer": response["answer"], "projects": projects}
    logging.info("Final server response", server_response)
    return server_response


@app.get("/health")
async def health():
    return {"status": "🤙"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
