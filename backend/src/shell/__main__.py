from uuid import UUID

import typer

from main import create_page_database

app = typer.Typer()


@app.command("create-db")
def create_db(page: UUID, title: str):
    db = create_page_database(page, title)
    print(f"Database ID is {db['id']}")


@app.command("dummy")
def dummy():
    ...


if __name__ == "__main__":
    app()
