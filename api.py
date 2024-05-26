from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

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


@app.get("/users")
def _get_users():
    return get_users()


@app.get("/options")
def get_property_options():
    return get_database_options(DATABASE)


class CreateFeatureRequestData(BaseModel):
    requested_by: str
    priority: str
    tags: list[str]
    due_date: date
    title: str
    summary: str
    description: str
    user_story: str


@app.post("/create")
def create_feature_request(data: CreateFeatureRequestData):
    create_database_page(DATABASE, data.due_date, data.title, data.requested_by, data.priority, data.tags,
                         data.summary, data.description, data.user_story)

    return True

