import discord
from discord.ext import commands
import datetime
import re
import os

# setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 🚀 pass help_command=None here so it never conflicts!
bot = commands.Bot(command_prefix="!h", intents=intents, help_command=None)

def parse_time(time_str: str) -> int:
    """Parses time inputs like 10, 10m, 1h, 1d into minutes."""
    time_str = time_str.replace("<", "").replace(">", "").strip()
    match = re.match(r"^(\d+)([mhd])?$", time_str.lower())
    if not match:
        raise ValueError("Invalid format")
    amount, unit = match.groups()
    amount = int(amount)
    if unit == "h":
        return amount * 60
    elif unit == "d":
        return amount * 1440
    return amount

@bot.event
async def on_ready():
    print(f'🔥 hamno is online and ready as {bot.user}! 🚀')
    await bot.change_presence(activity=discord.Game(name="moderating with !h 🛡️"))
    
    # 🧹 WIPE OLD SLASH COMMANDS FROM DISCORD CACHE
    try:
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print("✨ successfully cleared and unsynced old slash commands!")
    except Exception as e:
        print(f"❌ error wiping slash commands: {e}")

# 🔨 BAN COMMAND: !hban @user [reason]
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "no reason provided"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"💥 **{member.name}** was banned by {ctx.author.mention}! 🚪 reason: {reason} 🚫")
    except discord.Forbidden:
        await ctx.send("❌ i don't have permission to ban this user! ⚙️")

# 🔓 UNBAN COMMAND: !hunban Username#0000 or UserID
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_input: str):
    banned_users = [entry async for entry in ctx.guild.bans()]
    user_input = user_input.strip()
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if str(user) == user_input or str(user.id) == user_input or user.name == user_input:
            await ctx.guild.unban(user)
            await ctx.send(f"✅ **{user.name}** was unbanned by {ctx.author.mention}! welcome back 😇")
            return
            
    await ctx.send("❌ couldn't find that user in the ban list fr 🤷‍♂️")

# 👢 KICK COMMAND: !hkick @user [reason]
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "no reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member.name}** got kicked by {ctx.author.mention}! reason: {reason} 👋")
    except discord.Forbidden:
        await ctx.send("❌ i don't have permission to kick this user! ⚙️")

# ⏰ TIMEOUT COMMAND: !htimeout @user <time> [reason]
@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration_str: str, *, reason: str = "no reason provided"):
    try:
        minutes = parse_time(duration_str)
    except ValueError:
        await ctx.send("❌ invalid duration! use numbers like `10`, `10m`, `1h`, or `1d` ⏰")
        return

    duration = datetime.timedelta(minutes=minutes)
    try:
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🤫 **{member.name}** was timed out for {minutes} minute(s)! reason: {reason} 🤐")
    except discord.Forbidden:
        await ctx.send("❌ i don't have permission to timeout this user! ⚙️")

# 🔊 UNTIMEOUT COMMAND: !huntimeout @user / !hunmute @user
@bot.command(name="untimeout", aliases=["unmute"])
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member, *, reason: str = "no reason provided"):
    try:
        await member.timeout(None, reason=reason)
        await ctx.send(f"🔊 **{member.name}** was removed from timeout by {ctx.author.mention}! 🗣️✨")
    except discord.Forbidden:
        await ctx.send("❌ i don't have permission to remove timeout from this user! ⚙️")

# 🧹 PURGE COMMAND: !hpurge <amount>
@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 cleared {len(deleted) - 1} messages real quick! ✨", delete_after=3)

# 📜 HELP COMMAND: !hhelp
@bot.command(name="help")
async def hamno_help(ctx):
    embed = discord.Embed(
        title="🤖 HAMNO BOT COMMANDS 🛡️",
        description="dyno who?? hamno in the house 🔥\nUse `!h` prefix for all commands!",
        color=discord.Color.blue()
    )
    embed.add_field(name="!hban @user [reason]", value="bans a rule breaker 💥", inline=False)
    embed.add_field(name="!hunban user_id / username", value="lifts a ban 🔓", inline=False)
    embed.add_field(name="!hkick @user [reason]", value="kicks a user out 👢", inline=False)
    embed.add_field(name="!htimeout @user <time> [reason]", value="timeouts user (e.g. 10m, 1h) ⏰", inline=False)
    embed.add_field(name="!huntimeout @user", value="removes timeout / unmutes 🔊", inline=False)
    embed.add_field(name="!hpurge <amount>", value="clears chat messages 🧹", inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))
