import discord
from discord.ext import commands
import asyncio
from datetime import datetime

# Initialize bot
intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Token and sound file

TOKEN = os.getenv('DISCORD_TOKEN')
BELL_SOUND = "D:/MINI/BOT DISCORD/park-church-bell-tolling-01.wav"

# List of channel IDs
CHANNEL_IDS = [1270285785534300251, 861245642441490472, 897061629215264789, 903685923101900800, 897074575198785557]

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    bot.loop.create_task(schedule_voice_joins())

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and before.channel != after.channel:
        voice_channel = after.channel
        if voice_channel.id in CHANNEL_IDS:
            if voice_channel.guild.voice_client is None:  # Check if bot is not already connected
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(BELL_SOUND))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await vc.disconnect()

async def schedule_voice_joins():
    """Schedule bot to join channels at specific times."""
    while True:
        now = datetime.now().time()
        # Join channels at 13:00, 14:00, 23:00, and 00:00
        if (now.hour == 13 and now.minute == 0) or \
           (now.hour == 14 and now.minute == 0) or \
           (now.hour == 23 and now.minute == 0) or \
           (now.hour == 0 and now.minute == 0):
            await join_channels()
            await asyncio.sleep(60)  # Wait 1 minute to prevent duplicate joins within the same minute
        else:
            await asyncio.sleep(30)  # Check every 30 seconds

async def join_channels():
    """Bot joins each channel in CHANNEL_IDS and plays bell sound."""
    for guild in bot.guilds:
        for channel_id in CHANNEL_IDS:
            voice_channel = guild.get_channel(channel_id)
            if voice_channel is not None:
                if voice_channel.guild.voice_client is None:  # Ensure bot is not already connected
                    vc = await voice_channel.connect()
                    vc.play(discord.FFmpegPCMAudio(BELL_SOUND))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await vc.disconnect()

bot.run(TOKEN)
