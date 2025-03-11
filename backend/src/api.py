import os
from datetime import date
from typing import List

import fastapi
from fastapi import FastAPI, Query, Security, Header, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from main import get_users, get_database_options, create_database_page
import requests

from dotenv import load_dotenv

from settings import settings

load_dotenv()

app = FastAPI()

DATABASE = settings.notion_db

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CACHE = {}


def notify_on_slack(title: str, summary: str, author: str, tags: List[str], url: str, priority):
    tags_str = ", ".join([get_tag_by_id(x) for x in tags])
    priority = get_priority_by_id(priority)

    if not os.getenv("SLACK_WEBHOOK"):
        return

    requests.post(os.getenv("SLACK_WEBHOOK"), json={
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "New Feature Request Created"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\n\n{summary}\n\n*<{url}|View on Notion>*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Priority:*\n{priority}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Tags:*\n{tags_str}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Author: {author}",
                        "emoji": True
                    }
                ]
            }
        ]
    })


def auth(header: str = Security(APIKeyHeader(name="Authorization"))):
    if header != settings.api_secret:
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
    users = CACHE["users"]["results"]
    for user in users:
        if user["id"] == user_id:
            return user["name"]
    return "Unknown"


def get_tag_by_id(tag_id: str):
    tags = CACHE["options"]["Tags"]
    for tag in tags:
        if tag["id"] == tag_id:
            return tag["name"]
    return "?"


def get_priority_by_id(priority_id: str):
    priorities = CACHE["options"]["Priority"]
    for priority in priorities:
        if priority["id"] == priority_id:
            return priority["name"]
    return "Unknown"


@app.post("/create", dependencies=[fastapi.Depends(auth)])
def create_feature_request(data: CreateFeatureRequestData):
    try:
        url = create_database_page(DATABASE, data.title, data.requested_by, data.priority, data.tags,
                                   data.summary, data.description, data.user_story)

        if data.send_notification is True:
            notify_on_slack(
                title=data.title,
                author=get_username_by_id(data.requested_by),
                tags=data.tags,
                url=url,
                priority=data.priority,
                summary=data.summary
            )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


app.mount("/", StaticFiles(directory="../../notionFRs/dist"), name="static")
