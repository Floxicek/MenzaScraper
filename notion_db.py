from dotenv import load_dotenv
import os
from notion_client import Client
from datetime import datetime
from menza_scraper import Food

load_dotenv()
token = os.getenv("NOTION_TOKEN")
notion = Client(auth=token)

def get_database_id(database_name="Menza"):
    try:
        response = notion.search(filter={"property": "object", "value": "database"})
        results = response.get("results", [])
        for result in results:
            if result.get("title", [{}])[0].get("text", {}).get("content", "Untitled") == database_name:
                return result.get("id")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")

menza_db = get_database_id()

def update_last_seen(page_id):
    try:
        notion.pages.update(
        **{
            "page_id": page_id,
            "properties": {
            "LastSeen": {
                "date": {
                "start": str(datetime.now().date())
                }
            }
            }
        }
    )
    except Exception as e:
        print(f"An error occurred: {e}")

def food_exists(food_name):
    try:
        response = notion.databases.query(
            **{
                "database_id": menza_db,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": food_name
                    }
                }
            }
        )
        results = response.get("results", [])
        success = len(results) > 0
        # page_id = results[0]
        # print(page_id)
        # if success:
        #     update_last_seen(page_id)
        
        return success
    except Exception as e:
        print(f"An error occurred: {e}")
        return False   

def read_db():
    try:
        response = notion.databases.query(
            **{
                "database_id": menza_db,
            }
        )
        results = response.get("results", [])
        for result in results:
            print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

def add_food(food: Food):
    if food_exists(food.key):
        print(f"'{food.key}' already exists in the database.")
        # update_last_seen(food.name)
        return
    try:
        print(f"adding {food.key}")
        response = notion.pages.create(
            **{
            "parent": {"database_id": menza_db},
            "properties": {
                "Name": {
                "title": [
                    {
                    "text": {"content": food.key}
                    }
                ]
                },
                "Added": {
                "date": {
                    "start": str(datetime.now().date())
                }
                },
                "LastSeen":{
                    "date":{
                        "start":str(datetime.now().date())
                    }},
                "Type": {
                    "select": {"name": food.type}
                },
                "Place":{
                    "select":{"name": food.place}
                }
            }
            }
        )
        print(f"Added '{food.key}' to the database.")
    except Exception as e:
        print(f"An error occurred: {e}")


# print(read_db())