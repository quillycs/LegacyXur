import os
import random
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('BUNGIE_API')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def xur(ctx):
    url = "https://bungie.net/d1/Platform/Destiny/Advisors/Xur/"

    headers = {
        "X-API-Key": API_KEY,
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

    random_quote = random.choice(quotes)

    if response.status_code == 200:
        data = response.json()

        item_hashes = []

        for category in data["Response"]["data"]["saleItemCategories"]:
            for sale_item in category["saleItems"]:
                item_hash = sale_item["item"]["itemHash"]
                item_hashes.append(item_hash)

        await ctx.send(f"Item hashes: {item_hashes}\n\n'*{random_quote}*' - Xur, Agent of the Nine")
    else:
        # Calculate when Xur will next arrive
        await ctx.send(f"Xur has not arrived yet.\n\n'*{random_quote}*' - Xur, Agent of the Nine")

bot.run(TOKEN)