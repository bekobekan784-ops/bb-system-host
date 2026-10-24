import os
import discord
from discord import app_commands
from discord.ext import commands

# Setup bot with intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"🤖 VerityBot online as {client.user}!")
    
    # Custom playing status
    await client.change_presence(activity=discord.Game(name="/help | Capuchin Redux VR"))
    
    try:
        synced = await client.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# 1. /ping
@client.tree.command(name="ping", description="check veritybot latency 🏓")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"bot latency is **{latency}ms**",
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed)

# 2. /say (ULTRA FAST FIX ⚡)
@client.tree.command(name="say", description="make veritybot say something 💬")
@app_commands.describe(message="the message for veritybot to say")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(message)
    await interaction.followup.send("sent! 🚀", ephemeral=True)

# 3. /embed 
@client.tree.command(name="embed", description="create and post a custom embed message 🎨")
@app_commands.describe(
    title="the title of your embed",
    description="the main message content inside the embed"
)
async def embed_command(interaction: discord.Interaction, title: str, description: str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Sent by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message("embed created! 🎨", ephemeral=True)
    await interaction.channel.send(embed=embed)

# 4. /userinfo
@client.tree.command(name="userinfo", description="get info about a member 👤")
@app_commands.describe(target="the user to get info for")
async def userinfo(interaction: discord.Interaction, target: discord.Member = None):
    target = target or interaction.user
    
    embed = discord.Embed(
        title=f"👤 {target.name}'s Info",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Tag", value=str(target), inline=True)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>", inline=False)
    embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=False)

    await interaction.response.send_message(embed=embed)

# 5. /serverinfo
@client.tree.command(name="serverinfo", description="get stats about this server 📊")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed
