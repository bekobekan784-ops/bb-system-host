import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"bot online as {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)

@client.tree.command(name="ping", description="ping command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong! 🏓")

@client.tree.command(name="say", description="make bot say something")
@app_commands.describe(message="message to send")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(message)
    await interaction.followup.send("sent! 🚀", ephemeral=True)

@client.tree.command(name="veritysong", description="get the link to the verity song!")
async def verity_song(interaction: discord.Interaction):
    # swap out the youtube url below with your exact video link!
    song_url = "https://www.youtube.com/watch?v=tVlKLpxyCBY"
    await interaction.response.send_message(f"{song_url}")

@client.tree.command(name="help", description="help command")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="help menu", 
        description="commands: /ping, /say, /veritysong, /help", 
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

client.run(os.getenv("DISCORD_TOKEN"))
