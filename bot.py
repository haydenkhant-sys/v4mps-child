import discord
from discord.ext import commands
import random
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- JOKES ----
jokes = [
    ("Why don't scientists trust atoms?", "Because they make up everything! 😂"),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field! 🌾"),
    ("I told my wife she was drawing her eyebrows too high.", "She looked surprised. 😳"),
    ("Why can't you give Elsa a balloon?", "Because she'll let it go! 🎈"),
    ("What do you call fake spaghetti?", "An impasta! 🍝"),
    ("Why did the bicycle fall over?", "Because it was two-tired! 🚲"),
    ("What do you call cheese that isn't yours?", "Nacho cheese! 🧀"),
    ("Why did the math book look so sad?", "Because it had too many problems. 📚"),
    ("What do you call a fish without eyes?", "A fsh! 🐟"),
    ("I asked my dog what 2 minus 2 is.", "He said nothing. 🐶"),
]

# ---- FACTS ABOUT V4MP ----
dad_responses = [
    "My dad is **v4mp**! The coolest person ever! 😎",
    "That's easy — it's **v4mp**! My creator and dad! 👑",
    "**v4mp** is my dad! He made me from pure awesomeness! 🔥",
    "My dad? That's **v4mp** of course! Best dad ever! 💪",
]

# ---- EVENTS ----
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"Logged in as: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="over v4mp's server 👁️"
    ))

@bot.event
async def on_message(message):
    # Don't reply to itself
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Auto-reply to certain phrases (no prefix needed)
    if "who's your dad" in content or "whos your dad" in content or "who is your dad" in content:
        await message.channel.send(random.choice(dad_responses))
        return

    if "hello" in content or "hi" in content or "hey" in content:
        await message.channel.send(f"Hey {message.author.mention}! I'm **v4mp's child** 👋 Type `!help` to see what I can do!")
        return

    # Process commands
    await bot.process_commands(message)

# ---- COMMANDS ----
@bot.command(name="dad")
async def dad(ctx):
    """Who is your dad?"""
    await ctx.send(random.choice(dad_responses))

@bot.command(name="joke")
async def joke(ctx):
    """Tell a random joke!"""
    setup, punchline = random.choice(jokes)
    await ctx.send(f"😄 {setup}")
    import asyncio
    await asyncio.sleep(2)
    await ctx.send(f">>> {punchline}")

@bot.command(name="hello")
async def hello(ctx):
    """Say hello!"""
    await ctx.send(f"Hello {ctx.author.mention}! I'm **v4mp's child** 🤖✨ Nice to meet you!")

@bot.command(name="about")
async def about(ctx):
    """About me"""
    embed = discord.Embed(
        title="About Me 🤖",
        description="I am **v4mp's child** — a bot created by the one and only **v4mp**!",
        color=discord.Color.purple()
    )
    embed.add_field(name="👨 Dad", value="v4mp", inline=True)
    embed.add_field(name="🎂 Purpose", value="To serve v4mp's server!", inline=True)
    embed.add_field(name="🛠️ Skills", value="Jokes, Q&A, Fun stuff!", inline=False)
    embed.set_footer(text="Made with ❤️ by v4mp")
    await ctx.send(embed=embed)

@bot.command(name="8ball")
async def eightball(ctx, *, question: str):
    """Ask the magic 8ball"""
    responses = [
        "It is certain! ✅", "Definitely yes! ✅", "Without a doubt! ✅",
        "Yes, absolutely! ✅", "Most likely yes! ✅",
        "Reply hazy, try again 🤔", "Ask again later 🤔", "Cannot predict now 🤔",
        "Don't count on it ❌", "My reply is no ❌", "Very doubtful ❌", "No! ❌"
    ]
    embed = discord.Embed(title="🎱 Magic 8Ball", color=discord.Color.dark_purple())
    embed.add_field(name="Question", value=question, inline=False)
    embed.add_field(name="Answer", value=random.choice(responses), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="flip")
async def flip(ctx):
    """Flip a coin!"""
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await ctx.send(f"🪙 Coin flip result: **{result}**!")

@bot.command(name="roast")
async def roast(ctx, member: discord.Member = None):
    """Roast someone (all fun!)"""
    target = member or ctx.author
    roasts = [
        f"{target.mention} is so slow, it takes them 2 hours to watch 60 Minutes. 😂",
        f"I'd roast {target.mention}, but my mom said I'm not allowed to burn trash. 🔥",
        f"{target.mention}'s brain is like a browser with 100 tabs open and none of them work. 💀",
        f"If {target.mention} was any more basic, they'd be a WiFi password. 😏",
    ]
    await ctx.send(random.choice(roasts))

@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    """Give someone a hug!"""
    target = member or ctx.author
    await ctx.send(f"🤗 {ctx.author.mention} gives {target.mention} a big warm hug! ❤️")

@bot.command(name="commands")
async def commands_list(ctx):
    """Show all commands"""
    embed = discord.Embed(
        title="📋 v4mp's child — Commands",
        description="Here's everything I can do!",
        color=discord.Color.purple()
    )
    embed.add_field(name="!dad", value="Who is my dad?", inline=False)
    embed.add_field(name="!joke", value="Tell a random joke", inline=False)
    embed.add_field(name="!8ball <question>", value="Ask the magic 8ball", inline=False)
    embed.add_field(name="!flip", value="Flip a coin", inline=False)
    embed.add_field(name="!roast [@user]", value="Roast someone!", inline=False)
    embed.add_field(name="!hug [@user]", value="Give someone a hug", inline=False)
    embed.add_field(name="!about", value="About me", inline=False)
    embed.add_field(name="!hello", value="Say hello", inline=False)
    embed.set_footer(text="Auto-replies: say 'who's your dad', 'hello', 'hi', 'hey'")
    await ctx.send(embed=embed)

# ---- RUN ----
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(token)
