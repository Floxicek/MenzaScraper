import menza_scraper
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os, json

load_dotenv()

with open('config.json') as f:
    config = json.load(f)


def send_favorite_food():
    print(f"Fetching food items at {datetime.now()}")
    canteens_ids = []
    for c in config["canteens"]:
        canteens_ids.append(c["id"])
    food = menza_scraper.get_daily_menu(canteens_ids)
    
    webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"))
    
    embed = DiscordEmbed(title=f"{datetime.now().strftime("%c")}", color="AAFF00")
    embed.set_timestamp()
    is_empty = True
    for i, place in enumerate(food):
        for menu in place:
            for f in menu:
                # print(f)
                for fa in config['food']:
                    if fa in f:
                        embed.add_embed_field(name=config["canteens"][i]["name"], value=f)
                        is_empty = False
                        break
    if not is_empty:
        webhook.add_embed(embed)
        response = webhook.execute()

send_favorite_food()