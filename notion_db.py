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

def update_food(page_id, food: Food):
    try:
        page = notion.pages.retrieve(page_id)
        properties = page.get("properties", {})

        multi_select_property = properties.get("Place", {}).get("multi_select", [])
        old_counter = properties.get("Counter", {}).get("number", {})
        current_values = [item['name'] for item in multi_select_property]
        
        if food.place in current_values:
            notion.pages.update(
            page_id=page_id,
            properties={
                "LastSeen":{
                    "date":{
                        "start":str(datetime.now().date())
                        }
                },
                "Frequency":{
                    "number": old_counter+1
                }
            } 
            )
        else:
            notion.pages.update(
            page_id=page_id,
            properties={            "Place": {
                "multi_select": [{"name": value} for value in current_values + [food.place]]
            },
                "LastSeen":{
                    "date":{
                        "start":str(datetime.now().date())
                        }
                },
                "Frequency":{
                    "number":old_counter+1
                }
            } 
            )        
        print(f"'{food.key}' was updated.")
        
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def food_exists(food:Food):
    try:
        response = notion.databases.query(
            **{
                "database_id": menza_db,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": food.key
                    }
                }
            }
        )
        results = response.get("results", [])
        success = len(results) > 0
        page = results[0]
        return (success, page["id"])
    except Exception as e:
        return (False, -1)

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
    found, id = food_exists(food)
    if found and not(id == -1):
        print(f"'{food.key}' already exists in the database.")
        update_food(id, food)
    else:
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
                    # Added is being done by the notion
                    # "Added": {
                    # "date": {
                    #     "start": str(datetime.now().date())
                    # }
                    # }
                    "LastSeen":{
                        "date":{
                            "start":str(datetime.now().date())
                        }},
                    "Type": {
                        "select": {"name": food.type}
                    },
                    "Place":{
                        "multi_select":[{"name": food.place}]
                    }
                }
                }
            )
            print(f"Added '{food.key}' to the database.")
        except Exception as e:
            print(f"An error occurred: {e}")


# print(read_db())