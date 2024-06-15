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
    1707223616: "Legacy Engram | Leg Armor Engram | 29 <:strange_coin:1249138524117274775>",
    2055601060: "Hard Light | Auto Rifle | 23 <:strange_coin:1249138524117274775>",
    2055601062: "Monte Carlo | Auto Rifle | 23 <:strange_coin:1249138524117274775>",
    2055601061: "SUROS Regime | Auto Rifle | 23 <:strange_coin:1249138524117274775>",
    255654879: "Zhalo Supercell | Auto Rifle | 23 <:strange_coin:1249138524117274775>",
    3078564839: "Plan C | Fusion Rifle | 23 <:strange_coin:1249138524117274775>",
    346443850: "Pocket Infinity | Fusion Rifle | 23 <:strange_coin:1249138524117274775>",
    3012398148: "Telesto | Fusion Rifle | 23 <:strange_coin:1249138524117274775>",
    2447423792: "Hawkmoon | Hand Cannon | 23 <:strange_coin:1249138524117274775>",
    2447423793: "The Last Word | Hand Cannon | 23 <:strange_coin:1249138524117274775>",
    3851373522: "Nemesis Star | Machine Gun | 23 <:strange_coin:1249138524117274775>",
    57660786: "Super Good Advice | Machine Gun | 23 <:strange_coin:1249138524117274775>",
    57660787: "Thunderlord | Machine Gun | 23 <:strange_coin:1249138524117274775>",
    1177550374: "Bad Juju | Pulse Rifle | 23 <:strange_coin:1249138524117274775>",
    1177550375: "Red Death | Pulse Rifle | 23 <:strange_coin:1249138524117274775>",
    2808364179: "Dragon's Breath | Rocket Launcher | 23 <:strange_coin:1249138524117274775>",
    2808364178: "Truth | Rocket Launcher | 23 <:strange_coin:1249138524117274775>",
    1346849289: "MIDA Multi-Tool | Scout Rifle | 23 <:strange_coin:1249138524117274775>",
    3688594190: "The Jade Rabbit | Scout Rifle | 23 <:strange_coin:1249138524117274775>",
    99462852: "Invective | Shotgun | 23 <:strange_coin:1249138524117274775>",
    99462854: "The 4th Horseman | Shotgun | 23 <:strange_coin:1249138524117274775>",
    99462853: "Universal Remote | Shotgun | 23 <:strange_coin:1249138524117274775>",
    3938709034: "Trespasser | Sidearm | 23 <:strange_coin:1249138524117274775>",
    3227022823: "Hereafter | Sniper Rifle | 23 <:strange_coin:1249138524117274775>",
    3835813881: "No Land Beyond | Sniper Rifle | 23 <:strange_coin:1249138524117274775>",
    3835813880: "Patience and Time | Sniper Rifle | 23 <:strange_coin:1249138524117274775>",
    1520434776: "Achlyophage Symbiote | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1520434778: "ATS/8 ARACHNID | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1520434781: "Celestial Nighthawk | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1054763959: "Graviton Forfeit | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1520434777: "Knucklehead Radar | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1520434779: "Mask of the Third Man | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1054763958: "Skyburners Annex | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1458254033: "Don't Touch Me | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1458254034: "Khepri's Sting | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    2217280774: "Shinobu's Vow | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1458254032: "Young Ahamkara's Spine | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    105485105: "ATS/8 Tarantella | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    2882684152: "Crest of Alpha Lupi (Hunter) | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    2882684153: "Lucky Raspberry | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    1775312683: "Bones of Eao | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    1394543945: "Fr0st-EE5 | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    1775312682: "Radiant Dance Machines | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    941890989: "An Insurmountable Skullfort | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    591060260: "Empyrean Bellicose | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    941890987: "Eternal Warrior | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    941890990: "Helm of Inmost Light | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    941890991: "Helm of Saint-14 | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    941890988: "The Glasshouse | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    591060261: "The Taikonaut | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    3055446324: "ACD/0 Feedback Fence | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    155374077: "Immolation Fists | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    3055446326: "No Backup Plans | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    3055446327: "Ruin Wings | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    155374076: "Thagomizers | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    2661471738: "Crest of Alpha Lupi (Titan) | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    2661471739: "The Armamentarium | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    3921595523: "Twilight Garrison | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    2479526175: "Dunemarchers | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    4267828624: "Mk. 44 Stand Asides | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    4267828625: "Peregrine Greaves | Leg Armor | 13 <:strange_coin:1249138524117274775>",
    1519376145: "Apotheosis Veil | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    2778128366: "Astrocyte Verse | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1519376146: "Light Beyond Nemesis | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1519376147: "Obsidian Mind | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1519376144: "Skull of Dire Ahamkara | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1519376148: "The Ram | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    2778128367: "THE STAG | Helmet Armor | 13 <:strange_coin:1249138524117274775>",
    1275480032: "Claws of Ahamkara | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1275480035: "Nothing Manacles | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1062853751: "Ophidian Aspect | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1275480033: "Sunbreakers | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    1062853750: "The Impossible Machines | Gauntlet Armor | 13 <:strange_coin:1249138524117274775>",
    2898542650: "Alchemist's Raiment | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    3574778423: "Heart of the Praxic Fire | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    3574778420: "Purifier Robes | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    3574778421: "Starfire Protocol | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    3574778422: "Voidfang Vestments | Chest Armor | 13 <:strange_coin:1249138524117274775>",
    2275132880: "Transversive Steps | Leg Armor | 13 <:strange_coin:1249138524117274775>",
}

HEAVY_AMMO_SYNTHESIS = [
    "Heavy Ammo Synthesis | 3x | 1 <:strange_coin:1249138524117274775>",
    "Heavy Ammo Synthesis | 10x | 3 <:strange_coin:1249138524117274775>",
]

CURIOS = {
    417308266: "Three of Coins | 7 <:strange_coin:1249138524117274775>",
    2633085824: "Glass Needles | 3 <:strange_coin:1249138524117274775>, 3 <:mote_of_light:1251536764049559623> and 1 <:exotic_shard:1251536923319861248>",
    1880070440: "'Emerald Coil' | 23 <:strange_coin:1249138524117274775>",
    1880070441: "Plasma Drive | 23 <:strange_coin:1249138524117274775>",
    1880070443: "Void Drive | 23 <:strange_coin:1249138524117274775>",
}

MATERIAL_EXCHANGE = {
    452597397: "Exotic Shard | 7 <:strange_coin:1249138524117274775>",
    937555249: "Mote of Light | 2 <:strange_coin:1249138524117274775>",
}

WEAPON_BUNDLES = {
    3912367297: "Monte Carlo and Royal Flush | 30 <:strange_coin:1249138524117274775>",
    2850106041: "Zhalo Supercell and Shock Hazard | 30 <:strange_coin:1249138524117274775>",
}

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
        # Print unmatched hashes so I can add them to dictionaries after
        all_hashes = [item["item"]["itemHash"] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"]]

        unmatched_hashes = [item_hash for item_hash in all_hashes 
                            if item_hash not in ITEMS and item_hash not in CURIOS and item_hash not in MATERIAL_EXCHANGE and item_hash not in WEAPON_BUNDLES]

        # Print unmatched hashes
        print("Unmatched hashes:")
        for hash in unmatched_hashes:
            print(hash)
        item_names = [ITEMS[item["item"]["itemHash"]] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"] if item["item"]["itemHash"] in ITEMS]

        curios_names = [CURIOS[item["item"]["itemHash"]] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"] if item["item"]["itemHash"] in CURIOS]
                    
        material_exchange_names = [MATERIAL_EXCHANGE[item["item"]["itemHash"]] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"] if item["item"]["itemHash"] in MATERIAL_EXCHANGE]

        weapon_bundles_names = [WEAPON_BUNDLES[item["item"]["itemHash"]] for category in data["Response"]["data"]["saleItemCategories"]
                      for item in category["saleItems"] if item["item"]["itemHash"] in WEAPON_BUNDLES]

        items_list = "\n".join([f"• {item}" for item in item_names])
        heavy_ammo_synthesis_list = "\n".join([f"• {item}" for item in HEAVY_AMMO_SYNTHESIS])
        curios_list = heavy_ammo_synthesis_list + "\n" + "\n".join([f"• {item}" for item in curios_names])
        material_exchange_list = "\n".join([f"• {item}" for item in material_exchange_names])
        weapon_bundles_list = "\n".join([f"• {item}" for item in weapon_bundles_names])

        message = (
            f"Exotic gear:\n{items_list}\n\n"
            f"Curios:\n{curios_list}\n\n"
            f"Material exchange:\n{material_exchange_list}\n\n"
            f"Weapon bundles:\n{weapon_bundles_list}\n\n"
            f"'{random.choice(QUOTES)}' - Xur, Agent of the Nine"
        )
        
        await ctx.send(message)

# Run the bot
bot.run(TOKEN)