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
            "status": {
                "equals": "Done"
            }
        }
    }
).get("results")

now = datetime.datetime.now(datetime.timezone.utc)

if not results:
    print("There are no results to update.")
else:
    for result in results:
        page_id = result["id"]
        last_edited_time = datetime.datetime.fromisoformat(result["last_edited_time"][:-1] + '+00:00')
        delta = now - last_edited_time

        if delta.days >= 3:
            updated_props = {
                "status": {
                    "name": "Archive"
                }
            }
            notion.pages.update(page_id=page_id, properties=updated_props)
            print(f"Page {page_id} has been updated.")
