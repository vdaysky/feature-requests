import os
from datetime import date
from typing import List

import fastapi
from fastapi import FastAPI, Query, Security, Header, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from main import get_users, get_database_options, create_database_page

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


def auth(header: str = Security(Header(name="Authorization"))):
    if header != os.getenv("API_KEY"):
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


@app.post("/create", dependencies=[fastapi.Depends(auth)])
def create_feature_request(data: CreateFeatureRequestData):
    try:
        create_database_page(DATABASE, data.title, data.requested_by, data.priority, data.tags,
                             data.summary, data.description, data.user_story)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
