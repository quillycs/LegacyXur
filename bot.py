import os
import random
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("BUNGIE_API")

# Set up Discord bot intents and commands
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Xur quotes and items
QUOTES = [
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

ITEMS = {
    2055601060: "Hard Light",
    2055601062: "Monte Carlo",
    2055601061: "SUROS Regime",
    255654879: "Zhalo Supercell",
    3078564839: "Plan C",
    346443850: "Pocket Infinity",
    3012398148: "Telesto",
    2447423792: "Hawkoom",
    2447423793: "The Last Word",
    3851373522: "Nemesis Star",
    57660786: "Super Good Advice",
    57660787: "Thunderlord",
    1177550374: "Bad Juju",
    1177550375: "Red Death",
    2808364179: "Dragon's Breath",
    2808364178: "Truth",
    1346849289: "MIDA Multi-Tool",
    3688594190: "The Jade Rabbit",
    99462852: "Invective",
    99462854: "The 4th Horseman",
    99462853: "Universal Remote",
    3938709034: "Trespasser",
    3227022823: "Hereafter",
    3835813881: "No Land Beyond",
    3835813880: "Patience and Time",
}

CURIOS = [
    "3 Heavy Ammo Synthesis - 1 Strange Coin",
    "10 Heavy Ammo Synthesis - 3 Strange Coins",
    "Three of Coins - 7 Strange Coins",
    "Glass Needles - 3 Strange Coins, 3 Motes of Light & 1 Exotic Shard",
    "Emerald Coil - 23 Strange Coins",
    "Void Drive - 23 Strange Coins",
    "Exotic Shard - 7 Strange Coins",
    "Mote of Light - 2 Strange Coins"
]

# Function to fetch Xur's inventory
def fetch_xur_inventory():
    url = "https://bungie.net/d1/Platform/Destiny/Advisors/Xur/"
    headers = {"X-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to calculate time until next Friday 9 AM UTC
def time_until_friday_9am():
    current_utc_time = datetime.now(timezone.utc)
    days_until_friday = (4 - current_utc_time.weekday() + 7) % 7
    nearest_friday = current_utc_time + timedelta(days=days_until_friday)
    nearest_friday_9am = nearest_friday.replace(hour=9, minute=0, second=0, microsecond=0)
    return nearest_friday_9am - current_utc_time

# Command to get Xur's status and inventory
@bot.command()
async def xur(ctx):
    data = fetch_xur_inventory()

    if data.get("ErrorCode") == 1627:
        time_difference = time_until_friday_9am()
        days, remainder = divmod(time_difference.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60

        await ctx.send(
            f"There are {int(days)} days, {int(hours)} hours, and {int(minutes)} minutes left until Xur arrives.\n\n"
            f"'{random.choice(QUOTES)}' - Xur, Agent of the Nine"
        )
    else:
        item_names = [ITEMS[item["item"]["itemHash"]] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"] if item["item"]["itemHash"] in ITEMS]

        item_list = "\n".join([f"• {item}" for item in item_names])
        extra_item_list = "\n".join([f"• {item}" for item in CURIOS])

        message = (
            f"Xur is selling the following Exotic items:\n{item_list}\n\n"
            f"He also has these for sale:\n{extra_item_list}\n\n"
            f"'{random.choice(QUOTES)}' - Xur, Agent of the Nine"
        )
        
        await ctx.send(message)

# Run the bot
bot.run(TOKEN)