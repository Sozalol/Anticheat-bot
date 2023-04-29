import discord
from discord.ext import commands
import asyncio
from time import sleep
import uuid

intents = discord.Intents.all()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

yourrole = 'HQ'



@bot.command()
async def download(ctx):
    # Check if the user has the "Customer" role
    if discord.utils.get(ctx.author.roles, name="HQ"):
        embed = discord.Embed(title="**Link**", color=discord.Color.red())
        embed.add_field(name="Download", value="https://www.mediafire.com/file/de0eh7fq6ohhlrl/AntiCheat.rar/file")

        await ctx.author.send(embed=embed)
        await ctx.send("**Check your DMs for the download link!**")
    else:
        await ctx.send("Your not HQ dummy")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def clear(ctx, amount=5):
    if amount <= 0 or amount > 100:
        await ctx.send("You can only clear between 1 and 100 messages at once.")
    else:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Cleared {amount} messages.", delete_after=2.0)


@bot.command()
async def gen(ctx, amount):
    key_amt = range(int(amount))
    f = open("keys.txt", "a")
    show_key = ''
    for x in key_amt:
        key = str(uuid.uuid4())
        show_key += "\n" + key
        f.write(key)
        f.write("\n")

    if len(str(show_key)) == 37:
        show_key = show_key.replace('\n', '')
        await ctx.send(f"Key: {show_key}")
        return 0
    if len(str(show_key)) > 37:
        await ctx.send(f"Keys: {show_key}")
    else:
        await ctx.send("Somthings wrong")

@bot.command()
async def redeem(ctx, key):
    if len(key) == 36:
        with open("used keys.txt") as f:
            if key in f.read():
                em = discord.Embed(color=0xff0000)
                em.add_field(name="Invalid Key", value="Inputed key has already been used!")
                await ctx.send(embed=em)
                return 0
        with open("keys.txt") as f:
            if key in f.read():
                role = discord.utils.get(ctx.guild.roles, name=yourrole)
                await ctx.author.add_roles(role)
                em = discord.Embed(color=0xff0000)
                em.add_field(name="Key Redeemed", value="Key has now been redeemed")
                await ctx.send(embed=em)
                f = open("used keys.txt", "w")
                f.write(key)
                f.write('\n')
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="Invalid Key", value="Inputed key has already been used!")
                await ctx.send(embed=em)
    else:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="Invalid Key", value="Inputed key has already been used!")
        await ctx.send(embed=em)


bot.run('your-token')
