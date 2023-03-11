from notion_client import Client
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
database_id = os.getenv('DATABASE_ID')

db = notion.databases.query(
    **{
        'database_id': database_id,
        'filter': {
            'property': 'Select',
            'select': {
                'equals': 'Done'
            },
        },
    }
)

now = datetime.datetime.now(datetime.timezone.utc)

if not db:
    print("There are no results to update.")
else:
    db = db["results"]
    for result in db:
        page_id = result["id"]
        last_edited_time = datetime.datetime.fromisoformat(result["last_edited_time"][:-1] + '+00:00')
        delta = now - last_edited_time

        if delta.days > 3:
            notion.pages.update(
                **{
                    'page_id': page_id,
                    'properties': {
                        'Select': {
                            'select': {
                                'name': 'Archive'
                            },
                        },
                    }
                })

        print(f"Page {page_id} has been updated.")