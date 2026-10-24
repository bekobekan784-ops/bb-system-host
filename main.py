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

# 3. /userinfo
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

# 4. /serverinfo
@client.tree.command(name="serverinfo", description="get stats about this server 📊")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        color=discord.Color.green()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=True)
    embed.add_field(name="Total Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="Created On", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=False)

    await interaction.response.send_message(embed=embed)

# 5. /help
@client.tree.command(name="help", description="view all available veritybot commands 📜")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 VerityBot Commands",
        description="here are the starter commands for veritybot:",
        color=discord.Color.gold()
    )
    embed.add_field(name="`/ping`", value="check bot status and latency 🏓", inline=False)
    embed.add_field(name="`/userinfo [user]`", value="view profile details 👤", inline=False)
    embed.add_field(name="`/serverinfo`", value="view server statistics 📊", inline=False)
    embed.add_field(name="`/help`", value="show this message 📜", inline=False)
    embed.set_footer(text="VerityBot | Python Edition")

    await interaction.response.send_message(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
