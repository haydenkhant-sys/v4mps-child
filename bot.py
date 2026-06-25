import discord
from discord.ext import commands
import random
import os
import asyncio
import json
from datetime import datetime, timedelta

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- DATA FILES ----
XP_FILE = "xp_data.json"
ECO_FILE = "eco_data.json"

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---- STATIC DATA ----
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
    ("Why do cows wear bells?", "Because their horns don't work! 🐄"),
    ("What do you call a sleeping dinosaur?", "A dino-snore! 🦕"),
    ("Why did the computer go to the doctor?", "Because it had a virus! 💻"),
    ("What do you call a bear with no teeth?", "A gummy bear! 🐻"),
]

facts = [
    "A group of flamingos is called a 'flamboyance' 🦩",
    "Honey never expires — 3000-year-old honey was found in Egyptian tombs 🍯",
    "Octopuses have three hearts 🐙",
    "Bananas are berries, but strawberries are not 🍌",
    "Cats can't taste sweetness 🐱",
    "A group of owls is called a parliament 🦉",
    "Sharks are older than trees 🦈",
    "A day on Venus is longer than a year on Venus 🪐",
    "Wombat poop is cube-shaped 🟫",
    "Butterflies taste with their feet 🦋",
    "A snail can sleep for 3 years 🐌",
    "Crows can recognize and remember human faces 🐦",
]

quotes = [
    "\"Be yourself; everyone else is already taken.\" — Oscar Wilde ✨",
    "\"The only way to do great work is to love what you do.\" — Steve Jobs 💪",
    "\"You miss 100% of the shots you don't take.\" — Wayne Gretzky 🏒",
    "\"Why be moody when you can shake yo booty? 💃\" — Unknown Philosopher",
    "\"I am not lazy, I am on energy saving mode. 🔋\" — Wise Person",
    "\"I need a six month holiday, twice a year. 😴\" — Everyone",
    "\"My bed is a magical place where I suddenly remember everything. 🛏️\" — Me",
    "\"I'm not arguing, I'm just explaining why I'm right. 😤\" — Also Me",
]

memes = [
    "When you finally fix the bug but don't know how 💀",
    "Me: I'll sleep early tonight. Also me at 3am: 🦉",
    "Brain at 3am: remember that embarrassing thing from 10 years ago 😭",
    "My wallet: empty. My snack game: strong 🍕",
    "POV: You said 'I'm almost ready' 45 minutes ago 😅",
    "That feeling when the WiFi drops for 1 second 📶💀",
    "Me explaining my problems to my dog 🐶 (he understands)",
    "Friday energy vs Monday energy — Friday wins 1000% 📊",
    "When someone says 'just a quick question' and it's not quick 😐",
    "Nobody: ... Me at 2am: let me reorganize my entire life 🌙",
]

trivia_questions = [
    {"q": "What is the capital of Japan?", "a": "tokyo", "hint": "It starts with T 🇯🇵"},
    {"q": "How many sides does a hexagon have?", "a": "6", "hint": "It's a single digit number"},
    {"q": "What is the largest planet in our solar system?", "a": "jupiter", "hint": "It's a gas giant 🪐"},
    {"q": "What color is the sky on a clear day?", "a": "blue", "hint": "Look up! ☀️"},
    {"q": "How many legs does a spider have?", "a": "8", "hint": "More than 6 🕷️"},
    {"q": "What is the fastest land animal?", "a": "cheetah", "hint": "It has spots 🐆"},
    {"q": "What is 7 x 8?", "a": "56", "hint": "Between 50 and 60"},
    {"q": "Which planet is closest to the Sun?", "a": "mercury", "hint": "Also a element ☿"},
    {"q": "What is the largest ocean?", "a": "pacific", "hint": "It surrounds Hawaii 🌊"},
    {"q": "How many colors are in a rainbow?", "a": "7", "hint": "ROYGBIV 🌈"},
    {"q": "What animal is known as man's best friend?", "a": "dog", "hint": "Woof woof 🐶"},
    {"q": "What is the chemical symbol for water?", "a": "h2o", "hint": "Two H's and one O 💧"},
]

jobs = [
    ("pizza delivery 🍕", 50, 150),
    ("streamer 🎮", 20, 300),
    ("dog walker 🐕", 30, 100),
    ("meme maker 😂", 10, 200),
    ("ninja 🥷", 100, 500),
    ("professional napper 😴", 5, 50),
    ("Discord mod 🔨", 1, 30),
    ("YouTuber 📹", 50, 1000),
    ("chef 👨‍🍳", 80, 250),
    ("wizard 🧙", 200, 800),
]

vibes = [
    "Chaotic but make it cute 💅",
    "Main character energy today 🌟",
    "Unhinged but in a fun way 😈",
    "Cozy and unbothered 🧸",
    "Villain arc loading... 💀",
    "NPC behavior detected 🤖",
    "Certified sigma grindset mode 💪",
    "Touch grass energy 🌿",
    "Delulu but make it slay 👑",
]

weapons = ["🥄 spoon", "🍞 bread", "🧦 sock", "🪣 bucket", "🐟 fish", "🌮 taco", "👡 high heel", "🪠 plunger", "🧅 onion", "🍌 banana"]
battle_moves = ["slapped", "yeeted", "bonked", "obliterated", "destroyed", "defeated", "annihilated", "roasted"]

dad_responses = [
    "My dad is **v4mp**! The coolest person ever! 😎",
    "That's easy — it's **v4mp**! My creator and dad! 👑",
    "**v4mp** is my dad! He made me from pure awesomeness! 🔥",
    "My dad? That's **v4mp** of course! Best dad ever! 💪",
]

v4mp_compliments = [
    "v4mp mentioned?! That's literally the coolest person in this server! 👑🔥",
    "Did someone say v4mp?! The GOAT has been summoned! 🐐✨",
    "v4mp is the reason I exist! Show some respect! 😤👑",
    "v4mp?! The legend, the myth, the absolute unit! 💪😎",
]

roasts = [
    "I'd roast you, but my mom said I'm not allowed to burn trash. 🔥",
    "Your brain is like a browser with 100 tabs open and none of them work. 💀",
    "If you were any more basic, you'd be a WiFi password. 😏",
    "You're the human equivalent of a participation trophy. 🏆",
    "I've seen better comebacks in a boomerang. 🪃",
]

random_events = [
    "{user} just tripped over nothing 😂",
    "Server energy +10 🔥 thanks to {user}!",
    "Breaking news: {user} is built different 💪",
    "Sudden plot twist: {user} was the impostor all along 📮",
    "{user} has entered their villain era 😈",
    "Scientists confirm: {user} is the funniest person here 🧪",
    "{user} just unlocked a new achievement: Being Awesome 🏆",
]

hug_messages = [
    "🤗 {author} gives {target} the warmest hug ever! ❤️",
    "🤗 {author} squeezes {target} so tight! 💕",
    "🤗 {author} runs and hugs {target}! Awww! 🥺",
]
kiss_messages = [
    "😘 {author} blows {target} a kiss! 💋",
    "😚 {author} gives {target} a little peck! How cute! 💕",
    "💋 {author} → {target} 😳 ooooh!",
]
slap_messages = [
    "👋 {author} slaps {target} with a 🐟 fish!",
    "💥 {author} slaps {target} into next week!",
    "😤 {author} gives {target} the ultimate slap! SMACK! 👋",
]
cuddle_messages = [
    "🥰 {author} cuddles up with {target}! So wholesome! ☁️",
    "💕 {author} and {target} are cuddling! Don't disturb them! 🤫",
    "🛋️ {author} wraps {target} in a cozy blanket cuddle! 🥺",
]
highfive_messages = [
    "✋ {author} and {target} high five! SLAP! Nice! 🎉",
    "🙌 {author} gives {target} the most epic high five!",
    "✋💥✋ {author} and {target} — that high five echoed! 😂",
]

# Active trivia sessions
trivia_sessions = {}

# ---- XP HELPERS ----
XP_PER_MSG = 10
XP_COOLDOWN = 60  # seconds
last_xp_time = {}

def get_level(xp):
    return int((xp / 100) ** 0.5)

def xp_for_level(level):
    return (level ** 2) * 100

def add_xp(user_id, amount):
    data = load_json(XP_FILE)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 0}
    old_level = data[uid]["level"]
    data[uid]["xp"] += amount
    new_level = get_level(data[uid]["xp"])
    data[uid]["level"] = new_level
    save_json(XP_FILE, data)
    return old_level, new_level

# ---- ECO HELPERS ----
def get_balance(user_id):
    data = load_json(ECO_FILE)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"coins": 0, "last_daily": None, "last_work": None}
        save_json(ECO_FILE, data)
    return data[uid]

def update_eco(user_id, update):
    data = load_json(ECO_FILE)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"coins": 0, "last_daily": None, "last_work": None}
    data[uid].update(update)
    save_json(ECO_FILE, data)

# ---- EVENTS ----
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="over v4mp's server 👁️"
    ))
    bot.loop.create_task(random_event_task())

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        welcome_ch = discord.utils.find(
            lambda c: c.name in ["welcome", "general", "chat"],
            guild.text_channels
        )
        if welcome_ch:
            embed = discord.Embed(
                title=f"🎉 Welcome to {guild.name}!",
                description=f"Hey {member.mention}! We're glad you're here! 🥳\nYou are member **#{guild.member_count}**!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="📋 Get started", value="Type `!commands` to see what I can do!", inline=False)
            embed.set_footer(text="v4mp's child bot 🤖")
            await welcome_ch.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower().strip()

    # XP System
    if not message.author.bot and not content.startswith("!"):
        uid = str(message.author.id)
        now = datetime.now()
        last = last_xp_time.get(uid)
        if not last or (now - last).seconds >= XP_COOLDOWN:
            last_xp_time[uid] = now
            old_lvl, new_lvl = add_xp(message.author.id, XP_PER_MSG)
            if new_lvl > old_lvl:
                await message.channel.send(
                    f"🎉 {message.author.mention} leveled up to **Level {new_lvl}**! Keep chatting! 🔥"
                )

    # Trivia answer check
    if message.channel.id in trivia_sessions:
        session = trivia_sessions[message.channel.id]
        if content == session["answer"]:
            del trivia_sessions[message.channel.id]
            add_xp(message.author.id, 50)
            eco = get_balance(message.author.id)
            update_eco(message.author.id, {"coins": eco["coins"] + 100})
            await message.channel.send(
                f"🎉 {message.author.mention} got it right! The answer was **{session['answer']}**!\n+50 XP & +100 coins! 💰"
            )
            return

    # Auto replies
    if any(x in content for x in ["who's your dad", "whos your dad", "who is your dad", "who is ur dad"]):
        await message.channel.send(random.choice(dad_responses))
        return

    if content in ["hello", "hi", "hey", "hello!", "hi!", "hey!"]:
        await message.channel.send(f"Hey {message.author.mention}! I'm **v4mp's child** 👋 Type `!commands` to see what I can do!")
        return

    if "good morning" in content or content == "gm":
        greetings = [
            f"Good morning {message.author.mention}! Rise and grind! ☀️",
            f"Morning {message.author.mention}! Don't forget to touch grass today 🌿",
            f"Good morning {message.author.mention}! Today is gonna be your day! 🌟",
            f"Wakey wakey {message.author.mention}! ☀️ The world needs your energy!",
        ]
        await message.channel.send(random.choice(greetings))
        return

    if "good night" in content or content in ["gn", "gn!", "goodnight"]:
        nights = [
            f"Good night {message.author.mention}! Don't let the bed bugs bite 🌙",
            f"Night night {message.author.mention}! Sweet dreams 💤",
            f"Sleep well {message.author.mention}! See you tomorrow ⭐",
            f"Bye bye {message.author.mention}! Go touch your pillow 🛏️",
        ]
        await message.channel.send(random.choice(nights))
        return

    if content == "f":
        await message.channel.send("F in the chat 🫡")
        return

    if content in ["gg", "gg!", "ggs"]:
        await message.channel.send("GG EZ 🎮")
        return

    if content in ["lol", "lmao", "lmfao", "haha", "hahaha"]:
        replies = ["😂😂😂", "LMAOOO 💀", "bro really typed that 😭", "I'm dead 💀💀", "fr fr 😂"]
        await message.channel.send(random.choice(replies))
        return

    if content in ["brb", "brb!"]:
        await message.channel.send(f"See you soon {message.author.mention}! 👋")
        return

    if content in ["same", "same.", "same lol"]:
        await message.channel.send("SAME BRO 😭")
        return

    if content in ["no way", "no way!", "no way!!"]:
        replies = ["WAY 😤", "Yes way! 💀", "Believe it! 🔥"]
        await message.channel.send(random.choice(replies))
        return

    if "i'm bored" in content or "im bored" in content:
        await message.channel.send(f"{message.author.mention} Try `!trivia` or `!rps` or `!joke`! 🎮")
        return

    if "v4mp" in content and message.author.name.lower() != "v4mp":
        if random.random() < 0.4:
            await message.channel.send(random.choice(v4mp_compliments))
            return

    await bot.process_commands(message)

# ---- RANDOM EVENTS ----
async def random_event_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(random.randint(1800, 5400))
        for guild in bot.guilds:
            general = discord.utils.find(
                lambda c: c.name in ["general", "chat", "lounge", "main"],
                guild.text_channels
            )
            if general:
                members = [m for m in guild.members if not m.bot]
                if members:
                    user = random.choice(members)
                    event = random.choice(random_events).format(user=user.mention)
                    await general.send(f"🎲 **Random Event!**\n{event}")

# ---- FUN COMMANDS ----
@bot.command(name="joke")
async def joke(ctx):
    setup, punchline = random.choice(jokes)
    await ctx.send(f"😄 {setup}")
    await asyncio.sleep(2)
    await ctx.send(f">>> {punchline}")

@bot.command(name="fact")
async def fact(ctx):
    await ctx.send(f"🧠 **Random Fact:** {random.choice(facts)}")

@bot.command(name="quote")
async def quote(ctx):
    await ctx.send(f"💬 {random.choice(quotes)}")

@bot.command(name="meme")
async def meme(ctx):
    await ctx.send(f"😂 **Meme of the moment:**\n> {random.choice(memes)}")

@bot.command(name="8ball")
async def eightball(ctx, *, question: str = None):
    if not question:
        await ctx.send("❌ Ask a question! Example: `!8ball Will I win today?`")
        return
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

# ---- TRIVIA ----
@bot.command(name="trivia")
async def trivia(ctx):
    if ctx.channel.id in trivia_sessions:
        await ctx.send("⚠️ There's already a trivia question active! Answer it first!")
        return
    q = random.choice(trivia_questions)
    trivia_sessions[ctx.channel.id] = {"answer": q["a"], "hint": q["hint"]}
    embed = discord.Embed(title="🧠 Trivia Time!", description=q["q"], color=discord.Color.gold())
    embed.set_footer(text="Type your answer! Hint available with !hint | Correct = +50 XP +100 coins!")
    await ctx.send(embed=embed)
    await asyncio.sleep(30)
    if ctx.channel.id in trivia_sessions:
        del trivia_sessions[ctx.channel.id]
        await ctx.send(f"⏰ Time's up! The answer was **{q['a']}**! Better luck next time!")

@bot.command(name="hint")
async def hint(ctx):
    if ctx.channel.id in trivia_sessions:
        await ctx.send(f"💡 Hint: {trivia_sessions[ctx.channel.id]['hint']}")
    else:
        await ctx.send("No active trivia question! Use `!trivia` to start one.")

# ---- SOCIAL COMMANDS ----
@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else to hug! Example: `!hug @user`")
        return
    msg = random.choice(hug_messages).format(author=ctx.author.mention, target=member.mention)
    await ctx.send(msg)

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else to kiss! Example: `!kiss @user`")
        return
    msg = random.choice(kiss_messages).format(author=ctx.author.mention, target=member.mention)
    await ctx.send(msg)

@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else to slap! Example: `!slap @user`")
        return
    msg = random.choice(slap_messages).format(author=ctx.author.mention, target=member.mention)
    await ctx.send(msg)

@bot.command(name="cuddle")
async def cuddle(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else to cuddle! Example: `!cuddle @user`")
        return
    msg = random.choice(cuddle_messages).format(author=ctx.author.mention, target=member.mention)
    await ctx.send(msg)

@bot.command(name="highfive")
async def highfive(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!highfive @user`")
        return
    msg = random.choice(highfive_messages).format(author=ctx.author.mention, target=member.mention)
    await ctx.send(msg)

@bot.command(name="roast")
async def roast(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else to roast! Example: `!roast @user`")
        return
    await ctx.send(f"{member.mention} {random.choice(roasts)}")

# ---- MINI GAMES ----
@bot.command(name="coinflip")
async def coinflip(ctx):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await ctx.send(f"🪙 Flipping... **{result}**!")

@bot.command(name="dice")
async def dice(ctx):
    result = random.randint(1, 6)
    faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    await ctx.send(f"🎲 You rolled: {faces[result-1]} **{result}**!")

@bot.command(name="rps")
async def rps(ctx, choice: str = None):
    options = ["rock", "paper", "scissors"]
    emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    if not choice or choice.lower() not in options:
        await ctx.send("❌ Choose: `!rps rock` / `!rps paper` / `!rps scissors`")
        return
    player = choice.lower()
    bot_choice = random.choice(options)
    if player == bot_choice:
        result = "It's a tie! 🤝"
    elif (player == "rock" and bot_choice == "scissors") or \
         (player == "paper" and bot_choice == "rock") or \
         (player == "scissors" and bot_choice == "paper"):
        result = "You win! 🎉"
    else:
        r
