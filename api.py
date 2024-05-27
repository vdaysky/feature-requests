from datetime import date
from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from main import get_users, get_database_options, create_database_page

app = FastAPI()

DATABASE = "d46b47a8-5a4f-4d35-adca-0f9a4b88d82a"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CACHE = {}


@app.get("/users")
def _get_users(force_refresh: bool = Query(False)):
    if "users" not in CACHE or force_refresh:
        CACHE["users"] = get_users()
    return CACHE["users"]


@app.get("/options")
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


@app.post("/create")
def create_feature_request(data: CreateFeatureRequestData):
    try:
        create_database_page(DATABASE, data.title, data.requested_by, data.priority, data.tags,
                             data.summary, data.description, data.user_story)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
