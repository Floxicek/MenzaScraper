import menza_scraper
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os

fav = ["lasagn", "pizza", "burger", "paprice", "tortil"]

menzy = ["studenstký dům","technická","karlovo nám"]
load_dotenv()

def send_favorite_food():
    print(f"Fetching food items at {datetime.now()}")
    food = menza_scraper.get_daily_menu([2,3,8])
    
    webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"))
    
    embed = DiscordEmbed(title=f"{datetime.now().strftime("%c")}", color="AAFF00")
    embed.set_timestamp()
    is_empty = True
    for i, place in enumerate(food):
        for menu in place:
            for f in menu:
                # print(f)
                for fa in fav:
                    if fa in f:
                        embed.add_embed_field(menzy[i], value=f)
                        is_empty = False
                        break
    if not is_empty:
        webhook.add_embed(embed)
        response = webhook.execute()

send_favorite_food()