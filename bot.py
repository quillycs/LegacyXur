import os
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

    formatted_message = f"There are {days} days, {hours} hours, and {minutes} minutes left until Xur arrives."

    await ctx.send(formatted_message)

bot.run(TOKEN)