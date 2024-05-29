import os
from datetime import date
from typing import List

import fastapi
from fastapi import FastAPI, Query, Security, Header, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from main import get_users, get_database_options, create_database_page
import requests

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# my test db "d46b47a8-5a4f-4d35-adca-0f9a4b88d82a"

# conductive db
DATABASE = "39d0202f-5152-4a5e-b55f-8de15305f605"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CACHE = {}


def notify_on_slack(message: str):
    requests.post(os.getenv("SLACK_WEBHOOK"), json={
        "text": message
    })


def auth(header: str = Security(APIKeyHeader(name="Authorization"))):
    if header != os.getenv("API_SECRET"):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/users", dependencies=[fastapi.Depends(auth)])
def _get_users(force_refresh: bool = Query(False)):
    if "users" not in CACHE or force_refresh:
        CACHE["users"] = get_users()
    return CACHE["users"]


@app.get("/options", dependencies=[fastapi.Depends(auth)])
def get_property_options(force_refresh: bool = Query(False)):
    if "options" not in CACHE or force_refresh:
        CACHE["options"] = get_database_options(DATABASE)
    return CACHE["options"]


class CreateFeatureRequestData(BaseModel):
    requested_by: str
    priority: str
    tags: List[str]
    title: str
    summary: str
    description: str
    user_story: str
    send_notification: bool = False


def get_username_by_id(user_id: str):
    users = CACHE["users"]
    for user in users:
        if user["id"] == user_id:
            return user["name"]
    return "Unknown"


@app.post("/create", dependencies=[fastapi.Depends(auth)])
def create_feature_request(data: CreateFeatureRequestData):
    try:
        create_database_page(DATABASE, data.title, data.requested_by, data.priority, data.tags,
                             data.summary, data.description, data.user_story)

        if data.send_notification is True:
            notify_on_slack(f"*New feature request created:*\n{data.title}\nby {get_username_by_id(data.requested_by)}")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
