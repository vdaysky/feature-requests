import datetime


def property_date(start_date, end_date):
    return {
        "type": "date",
        "date": {
            "start": start_date,
            "end": end_date,
            "time_zone": None
        }
    }


def property_multiselect(options):
    return {
        "type": "multi_select",
        "multi_select": [
            {"id": option}
            for option in options
        ]
    }


def property_people(people):
    return {
        "type": "people",
        "people": [
            {"id": person, "object": "user"}
            for person in people
        ]
    }


def property_text(text):
    return {
        "id": "title",
        "type": "title",
        "title": [
            {
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                },
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default"
                },
                "plain_text": text,
                "href": None
            }
        ]
    }


def property_select(option):
    return {
        "type": "select",
        "select": {
            "id": option
        }
    }


def db_properties(title, requested_by, priority, tags):
    return {
        "Due Date": property_date(datetime.date.today().isoformat(), None),
        "Tags": property_multiselect(tags),
        "Participants": property_people([requested_by]),
        "Requested By": property_people([requested_by]),
        "Name": property_text(title),
        "Priority": property_select(priority),
    }


def heading(text, size, toggle=False, children=None):
    return {
            "object": "block",
            "type": f"heading_{size}",
            f"heading_{size}": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": text,
                        "href": None
                    }
                ],
                "is_toggleable": toggle,
                "color": "default",
                **({"children": children} if children else {})
            }
        }


def heading1(text, toggle=False, children=None):
    return heading(text, 1, toggle=toggle, children=children)


def heading2(text, toggle=False, children=None):
    return heading(text, 2, toggle=toggle, children=children)


def heading3(text, toggle=False, children=None):
    return heading(text, 3, toggle=toggle, children=children)


def callout(text):
    return {
        "type": "callout",
        "callout": {
            "icon": {
                "type": "emoji",
                "emoji": "\ud83d\udca1"
            },
            "color": "gray_background",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": text,
                    "href": None
                }
            ]
        }
    }


def paragraph(text):
    return {
        "type": "paragraph",
        "paragraph": {
            "color": "default",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": text,
                    "href": None
                }
            ]
        }
    }
