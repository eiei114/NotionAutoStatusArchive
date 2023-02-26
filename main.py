from notion_client import Client
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
database_id = os.getenv('DATABASE_ID')

results = notion.databases.query(
    **{
        "database_id": database_id,
        "filter": {
            "property": "Status",
            "select": {
                "equals": "Done"
            }
        }
    }
).get("results")

now = datetime.datetime.now(datetime.timezone.utc)

for result in results:
    page_id = result["id"]
    last_edited_time = datetime.datetime.fromisoformat(result["last_edited_time"][:-1] + '+00:00')
    delta = now - last_edited_time

    if delta.days >= 3:
        notion.pages.update(page_id=page_id, properties={"Status": {"name": "Archive"}})
