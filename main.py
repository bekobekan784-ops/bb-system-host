import os
import discord
from discord import app_commands
from discord.ext import commands

# set up intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"[BB$SYSTEM] 💰 bot online as {client.user}")
    # custom activity status
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, 
            name="bbno$ - edamame 🎧"
        )
    )
    try:
        synced = await client.tree.sync()
        print(f"[BB$SYSTEM] synced {len(synced)} flex commands! 💎")
    except Exception as e:
        print(f"[BB$SYSTEM ERROR] {e}")

@client.tree.command(name="ping", description="check if bb$system is feeling groovy")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    embed = discord.Embed(
        title="💵 BB$SYSTEM CHECK",
        description=f"```bb$system speed: {latency}ms ⚡️\ntoo fast, bag secured 💼```",
        color=discord.Color.gold()
    )
    embed.set_footer(text="bb$system // wrist so icy ❄️")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="say", description="make bb$system drop a line")
@app_commands.describe(message="what should bb$system say?")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(f"🗣️ **bb$system says:** {message} 🗣️")
    await interaction.followup.send("```bar dropped successfully 🎤```", ephemeral=True)

@client.tree.command(name="flex", description="flex your clout in the server")
async def flex(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💰 BB$SYSTEM FLEX CORNER",
        description="```status: 100% certified fresh 🔥\nclout level: OVER 9000 📈\nbag: SECURED 💸```",
        color=discord.Color.green()
    )
    embed.set_footer(text="bb$system // money talks 🤑")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="veritysong", description="listen to the ultimate jam")
async def verity_song(interaction: discord.Interaction):
    song_url = "https://www.youtube.com/watch?v=tV1KLpxyCBY"
    embed = discord.Embed(
        title="🎶 BB$SYSTEM HIT SINGLE",
        description=f"**banger of the day:** verity song\n🔗 [stream it here!]({song_url}) 🎧",
        color=discord.Color.magenta()
    )
    embed.set_footer(text="bb$system // certified banger 🔥")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="help", description="bb$system command list")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎤 BB$SYSTEM MENU",
        description="check out the hit commands below 👇",
        color=discord.Color.gold()
    )
    embed.add_field(name="`/ping`", value="check connection speed ⚡️", inline=False)
    embed.add_field(name="`/say`", value="make the bot speak 🗣️", inline=False)
    embed.add_field(name="`/flex`", value="show off your clout 💰", inline=False)
    embed.add_field(name="`/veritysong`", value="get the track link 🎵", inline=False)
    embed.add_field(name="`/help`", value="open this menu 📜", inline=False)
    embed.set_footer(text="bb$system // no$ inside 💸")
    await interaction.response.send_message(embed=embed)

# run bot token from environment variables
client.run(os.getenv("TOKEN"))
