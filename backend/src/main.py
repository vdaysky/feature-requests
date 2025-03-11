import json
import os

import requests

from const import db_properties, heading1, heading2, paragraph, callout, heading3

from dotenv import load_dotenv

from settings import settings

load_dotenv()
SECRET = settings.notion_secret


def notion_request(method, url, data):
    r = getattr(requests, method)(f"https://api.notion.com/v1/{url}", headers={
        "Authorization": f"Bearer {SECRET}",
        "Notion-Version": "2022-02-22"
    }, json=data
    )
    res = r.json()
    print(f"{url}:", json.dumps(res, indent=4))
    if "message" in res:
        print(res["message"])
        raise Exception(res["message"])
    return r.json()


def notion_post(url, data):
    return notion_request("post", url, data)


def notion_get(url):
    return notion_request("get", url, {})


def notion_patch(url, data):
    return notion_request("patch", url, data)


def get_database(id):
    return notion_get(f"databases/{id}")


def query_database(id):
    return notion_post(f"databases/{id}/query", {})


def get_users():
    return notion_get("users")


def append_children(block_id, children):
    return notion_patch(f"blocks/{block_id}/children", {
        "children": children
    })


def create_database_page(database_id, title, requested_by, priority, tags, summary, description, user_story):

    page = notion_post(f"pages", {
        "parent": {
            "database_id": database_id
        },
        "properties": db_properties(title, requested_by, priority, tags),
        "children": [
            heading1("Feature Request", toggle=True, children=[
                heading2("Feature Description", toggle=True, children=[
                    heading3("Summary"),
                    callout("Brief description of the feature"),
                    paragraph(summary),
                    heading3("Detailed Description"),
                    callout("Include more details, in  particular about specific functionalities and requirements"),
                    paragraph(description),
                    heading3("User Story/Use Case"),
                    callout("Describe how the end-user will interact with this feature"),
                    paragraph(user_story),
                ]),
            ]),
            heading1("Feature Interview", toggle=True, children=[
                heading2("Technical Specifications", toggle=True, children=[
                    heading3("Technical Requirements"),
                    callout("Detail any specific technical needs, including platforms, languages, frameworks"),
                    paragraph("..."),
                    heading3("Integration Points"),
                    callout("Describe how this feature integrates with other parts of the product"),
                    paragraph("..."),
                    heading3("Data Requirements"),
                    callout("Specify any data storage, processing, or security needs"),
                    paragraph("..."),
                    heading3("Performance Criteria"),
                    callout("Define acceptable performance levels, response times"),
                    paragraph("..."),
                ]),
                heading2("Design Specifications", toggle=True, children=[
                    heading3("User Interface Requirements"),
                    callout("If applicable, describe the visual and interactive aspects"),
                    paragraph("..."),
                    heading3("User Experience Considerations"),
                    callout("Detail any UX principles or standards to adhere to"),
                    paragraph("..."),
                    heading3("Mockups or Diagrams"),
                    callout("Attach any preliminary designs or sketches"),
                    paragraph("..."),
                ])
            ]),
            heading1("Additional Comments or Notes:"),
            paragraph("...")
        ],
    })
    return page["url"]


def create_page_database(page_id, title, tags_options=None, priority_options=None):
    """
    Create a new database on a Notion page with predefined properties

    Args:
        page_id: ID of the parent page
        title: Database title
        tags_options: List of tag options with name and color
        priority_options: List of priority options with name and color
    """
    database = notion_post("databases", {
        "parent": {
            "type": "page_id",
            "page_id": str(page_id)
        },
        "icon": {
            "type": "emoji",
            "emoji": "📋"
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": title,
                    "link": None
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Created / Due": {
                "date": {}
            },
            "Tags": {
                "type": "multi_select",
                "multi_select": {
                    "options": tags_options or []
                }
            },
            "Participants": {
                "people": {}
            },
            "Requested By": {
                "people": {}
            },
            "Priority": {
                "select": {
                    "options": priority_options or [
                        {"name": "High", "color": "red"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "green"}
                    ]
                }
            }
        }
    })
    return database


def get_page(id):
    return notion_get(f"pages/{id}")


def get_block(id):
    return notion_get(f"blocks/{id}")


def get_block_children(id):
    return notion_get(f"blocks/{id}/children")


def get_database_options(database):
    data = get_database(database)
    res = {}
    for field, value in data['properties'].items():

        if "multi_select" in value:
            res[field] = value["multi_select"]["options"]

        if "select" in value:
            res[field] = value["select"]["options"]

    return res
