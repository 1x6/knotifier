import nextcord
from nextcord.ext import commands
from database import knotifier
from config import token
import bato
import actions
import threading
import time
import re

intents = nextcord.Intents.default()
intents.message_content = True

knotifier.initiate()

# Define the function that runs the thread
def run_thread():
    while True:
        # Call your function
        actions.check_for_new()
        # Sleep for an hour
        time.sleep(10)

# Create and start the thread
thread = threading.Thread(target=run_thread)
thread.start()

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

@bot.slash_command(name="track", description="Tracks series chapters")
async def addtrack(ctx, link: str):
    email = knotifier.db.get_email(ctx.user.id)
    telegram_chat_id = knotifier.db.get_telegram_chat_id(ctx.user.id)

    if email is None and telegram_chat_id is None:
        await ctx.send("Please set your email or Telegram channel ID first to receive notifications.")
        return

    seriesId = None
    if '/series/' in link:  # v2
        seriesId = link.split("/series/")[1].split("/")[0]
    elif '/title/' in link:  # v3
        seriesId = link.split("/title/")[1].split("/")[0].split("-")[0]
    elif link.isdigit():
        seriesId = int(link)
    if seriesId is None:
        await ctx.send("Invalid series link.")
        return

    # Check if the series is already tracked for the user
    tracked_series = knotifier.db.get_tracked_series(ctx.user.id)
    if any(series[0] == seriesId for series in tracked_series):
        await ctx.send("This series is already being tracked.")
        return

    title = bato.get_metadata(seriesId)
    if len(title) > 0 and type(title) == str:
        knotifier.db.track(ctx.user.id, seriesId, bato.get_chapters(seriesId), title)
        await ctx.send(f"Now tracking {title}")
    else:
        await ctx.send("Invalid series link")

@bot.slash_command(name="email", description="Sets your email to recieve notifications")
async def setemail(ctx, email: str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        if knotifier.db.save_email(ctx.user.id, email):
            await ctx.send(f"Email set to {email}")
            #TODO maybe verify'''
    else:
        await ctx.send("Invalid email")

@bot.slash_command(name="list", description="Lists your tracked series")
async def list(ctx,):
    s = knotifier.db.get_tracked_series(ctx.user.id)
    if s == [] or s is None:
       await ctx.send("You are not tracking any series")
       return
    if s is not None:
        msg = "\n"
        for series_id, friendly_name in s:
            print(f"Series ID: {series_id}, Friendly Name: {friendly_name}")
            msg += f"`{friendly_name}` - <https://bato.to/series/{series_id}>\n"
        msg += "\n"
        await ctx.send(f"Tracking series: {msg}")

@bot.slash_command(name="telegram", description="Sets your Telegram channel ID")
async def settelegram(ctx, channel_id: str):
    if channel_id.isdigit():
        channel_id = int(channel_id)
        if knotifier.db.save_telegram_chat_id(ctx.user.id, channel_id):
            await ctx.send(f"Telegram channel ID set to {channel_id}")
        else:
            await ctx.send("Failed to set Telegram channel ID")
    else:
        await ctx.send("Please provide a valid Telegram channel ID.\nTo retrieve your Telegram channel ID, please use the Username to ID Bot\n<https://t.me/username_to_id_bot>")

bot.run(token())
