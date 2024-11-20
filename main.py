import menza_scraper
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os, json
import notion_db 

load_dotenv()

with open('config.json') as f:
    config = json.load(f)

def is_open():
    day = datetime.now().strftime("%w")
    return not (day == 0 or day == 6)


def send_favorite_food():
    print(f"Fetching food items at {datetime.now()}")
    canteens_ids = []
    for c in config["canteens"]:
        canteens_ids.append(c["id"])
    
    webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"))
    
    embed = DiscordEmbed(title=f"{datetime.now().strftime("%c")}", color="AAFF00")
    embed.set_timestamp()
    is_empty = True
    
    for cantine in canteens_ids:
        menu = menza_scraper.get_daily_menu(cantine)
        for food in menu:            
            notion_db.add_food(f) # if food not in notion database, add it
            for fa in config['food']:
                if fa in f:
                    embed.add_embed_field(name=config["canteens"][i]["name"], value=f)
                    is_empty = False
                    break
    if not is_empty:
        webhook.add_embed(embed)
        response = webhook.execute()


if is_open():
    send_favorite_food()
    