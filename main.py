import discord
from discord.ext import commands
import datetime

# setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# bot prefix setup (!h command syntax)
bot = commands.Bot(command_prefix="!h", intents=intents)

@bot.event
async def on_ready():
    print(f'🔥 hamno is online and ready as {bot.user}! 🚀')
    await bot.change_presence(activity=discord.Game(name="moderating with !h 🛡️"))

# 🔨 BAN COMMAND: !hban @user [reason]
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "no reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"💥 **{member.name}** was banned by {ctx.author.mention}! 🚪 reason: {reason} 🚫")

# 🔓 UNBAN COMMAND: !hunban Username#0000 or UserID
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_input: str):
    banned_users = [entry async for entry in ctx.guild.bans()]
    for ban_entry in banned_users:
        user = ban_entry.user
        if str(user) == user_input or str(user.id) == user_input:
            await ctx.guild.unban(user)
            await ctx.send(f"✅ **{user.name}** was unbanned! Welcome back (maybe) 😇")
            return
    await ctx.send("❌ couldn't find that user in the ban list fr 🤷‍♂️")

# 👢 KICK COMMAND: !hkick @user [reason]
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "no reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member.name}** got kicked by {ctx.author.mention}! reason: {reason} 👋")

# ⏰ TIMEOUT / MUTE COMMAND: !htimeout @user <minutes> [reason]
@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason: str = "no reason provided"):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🤫 **{member.name}** was timed out for {minutes} minute(s)! reason: {reason} 🤐")

# 🧹 PURGE / CLEAR MESSAGES: !hpurge <amount>
@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 cleared {len(deleted) - 1} messages real quick! ✨", delete_after=3)

# 📜 HELP COMMAND: !hhelp
@bot.command(name="help")
async def hamno_help(ctx):
    embed = discord.Embed(
        title="🤖
