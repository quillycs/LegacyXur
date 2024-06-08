import os
import random
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("BUNGIE_API")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.command()
async def xur(ctx):
    url = "https://bungie.net/d1/Platform/Destiny/Advisors/Xur/"

    headers = {
        "X-API-Key": API_KEY
    }

    response = requests.get(url, headers = headers)

    quotes = [
        "So lonely here.",
        "I am only an Agent. The Nine rule beyond the Jovians.",
        "I cannot explain what the Nine are. They are... very large. I cannot explain. The fault is mine, not yours.",
        "I think it is very possible that I am here to help you.",
        "Each mote of dust tells a story of ancient Earth.",
        "I think the cells of this body are dying.",
        "I do not entirely control my movements.",
        "Some of the cells in this body began on this world, how strange to return.",
        "There are no birds where I came from. The things that fly... are like shadows.",
        "I understood my mission when the Nine put it in me, but now I cannot articulate it.",
        "This is but one end.",
        "These inner worlds are very strange.",
        "My movements are to a significant degree dependent on planetary alignments.",
        "I feel a great many consciousnesses impinging on mine, and all of them so small and lonely."
    ]

    items = {
        1665465325: "((GENESIS CHAIN~))",
        3563445476: "Abyss Defiant (Adept)",
        1344441638: "Anguish of Drystan (Adept)",
        2512322824: "Atheon's Epilogue (Adept)",
        2748609458: "Fabian Strategy",
        99462853: "Universal Remote",
        941890990: "Helm of Inmost Light",
        1458254033: "Don't Touch Me",
        1519376147: "Obsidian Mind"
    }

    random_quote = random.choice(quotes)

    if response.status_code == 200:
        data = response.json()

        item_names = []

        for category in data["Response"]["data"]["saleItemCategories"]:
            for sale_item in category["saleItems"]:
                item_hash = sale_item["item"]["itemHash"]
                if item_hash in items:
                    item_names.append(items[item_hash])

        item_list = "\n".join([f"• {item}" for item in item_names])

        second_item_list = "\n".join([f"• {item}" for item in ["Heavy Ammo Synthesis", "Three of Coins", "Glass Needles", "Emerald Coil", "Void Drive"]])

        message = (
            f"Xur is selling the following Exotic items:\n"
            f"{item_list}\n\n"
            f"He also has these for sale:\n"
            f"{second_item_list}\n\n"
            f"*{random_quote}* - Xur, Agent of the Nine"
        )
        
        await ctx.send(message)
    else:
        current_utc_time = datetime.now(timezone.utc)
        days_until_friday = (4 - current_utc_time.weekday() + 7) % 7
        nearest_friday = current_utc_time + timedelta(days=days_until_friday)
        nearest_friday_9am = nearest_friday.replace(hour=9, minute=0, second=0, microsecond=0)
        time_difference = nearest_friday_9am - current_utc_time

        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        await ctx.send(f"There are {days} days, {hours} hours, and {minutes} minutes left until Xur arrives.\n\n'*{random_quote}*' - Xur, Agent of the Nine")

bot.run(TOKEN)