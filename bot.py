import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def xur(ctx):
    current_utc_time = datetime.now(timezone.utc)
    days_until_friday = (4 - current_utc_time.weekday() + 7) % 7
    nearest_friday = current_utc_time + timedelta(days=days_until_friday)
    nearest_friday_9am = nearest_friday.replace(hour=9, minute=0, second=0, microsecond=0)
    time_difference = nearest_friday_9am - current_utc_time

    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

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

    formatted_message = f'There are {days} days, {hours} hours, and {minutes} minutes left until Xur arrives.\n\n"*{random_quote}*" - Xur, Agent of the Nine'

    await ctx.send(formatted_message)

bot.run(TOKEN)