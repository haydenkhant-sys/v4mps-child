import discord
from discord.ext import commands
import random
import os
import asyncio
from datetime import datetime, timedelta

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- IN-MEMORY STORAGE ----
xp_data = {}       # {user_id: {"xp": 0, "level": 0, "name": ""}}
eco_data = {}      # {user_id: {"coins": 0, "last_daily": None, "last_work": None}}
last_xp_time = {}  # {user_id: datetime}
trivia_sessions = {}

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
    "Wombat poop is cube-shaped 🟫",
    "Butterflies taste with their feet 🦋",
    "A snail can sleep for 3 years 🐌",
]

quotes = [
    "\"Be yourself; everyone else is already taken.\" — Oscar Wilde ✨",
    "\"The only way to do great work is to love what you do.\" — Steve Jobs 💪",
    "\"You miss 100% of the shots you don't take.\" — Wayne Gretzky 🏒",
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
    "Friday energy vs Monday energy — Friday wins 1000% 📊",
    "When someone says 'just a quick question' and it's not quick 😐",
    "Nobody: ... Me at 2am: let me reorganize my entire life 🌙",
]

trivia_questions = [
    {"q": "What is the capital of Japan?", "a": "tokyo", "hint": "Starts with T 🇯🇵"},
    {"q": "How many sides does a hexagon have?", "a": "6", "hint": "Single digit number"},
    {"q": "What is the largest planet in our solar system?", "a": "jupiter", "hint": "Gas giant 🪐"},
    {"q": "How many legs does a spider have?", "a": "8", "hint": "More than 6 🕷️"},
    {"q": "What is the fastest land animal?", "a": "cheetah", "hint": "Has spots 🐆"},
    {"q": "What is 7 x 8?", "a": "56", "hint": "Between 50 and 60"},
    {"q": "Which planet is closest to the Sun?", "a": "mercury", "hint": "Also an element ☿"},
    {"q": "What is the largest ocean?", "a": "pacific", "hint": "Surrounds Hawaii 🌊"},
    {"q": "How many colors are in a rainbow?", "a": "7", "hint": "ROYGBIV 🌈"},
    {"q": "What is the chemical symbol for water?", "a": "h2o", "hint": "Two H's and one O 💧"},
]

jobs = [
    ("pizza delivery 🍕", 50, 150),
    ("streamer 🎮", 20, 300),
    ("dog walker 🐕", 30, 100),
    ("meme maker 😂", 10, 200),
    ("ninja 🥷", 100, 500),
    ("professional napper 😴", 5, 50),
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

weapons = ["🥄 spoon", "🍞 bread", "🧦 sock", "🐟 fish", "🌮 taco", "👡 high heel", "🧅 onion", "🍌 banana"]
battle_moves = ["slapped", "yeeted", "bonked", "obliterated", "destroyed", "defeated", "annihilated"]

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
    "{user} just unlocked: Being Awesome 🏆",
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

# ---- XP HELPERS ----
XP_PER_MSG = 10
XP_COOLDOWN = 60

def get_level(xp):
    return int((xp / 100) ** 0.5)

def xp_for_next_level(level):
    return (level + 1) ** 2 * 100

def get_xp(user_id, name=""):
    uid = str(user_id)
    if uid not in xp_data:
        xp_data[uid] = {"xp": 0, "level": 0, "name": name}
    return xp_data[uid]

def add_xp(user_id, amount, name=""):
    d = get_xp(user_id, name)
    old_level = d["level"]
    d["xp"] += amount
    d["level"] = get_level(d["xp"])
    if name:
        d["name"] = name
    return old_level, d["level"]

# ---- ECO HELPERS ----
def get_eco(user_id):
    uid = str(user_id)
    if uid not in eco_data:
        eco_data[uid] = {"coins": 0, "last_daily": None, "last_work": None}
    return eco_data[uid]

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
            old_lvl, new_lvl = add_xp(message.author.id, XP_PER_MSG, message.author.display_name)
            if new_lvl > old_lvl:
                await message.channel.send(
                    f"🎉 {message.author.mention} leveled up to **Level {new_lvl}**! Keep chatting! 🔥"
                )

    # Trivia answer check
    if message.channel.id in trivia_sessions:
        session = trivia_sessions[message.channel.id]
        if content == session["answer"]:
            del trivia_sessions[message.channel.id]
            add_xp(message.author.id, 50, message.author.display_name)
            eco = get_eco(message.author.id)
            eco["coins"] += 100
            await message.channel.send(
                f"🎉 {message.author.mention} got it right! Answer: **{session['answer']}**!\n+50 XP & +100 coins! 💰"
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
        ]
        await message.channel.send(random.choice(greetings))
        return

    if "good night" in content or content in ["gn", "gn!", "goodnight"]:
        nights = [
            f"Good night {message.author.mention}! Don't let the bed bugs bite 🌙",
            f"Night night {message.author.mention}! Sweet dreams 💤",
            f"Sleep well {message.author.mention}! See you tomorrow ⭐",
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
        await message.channel.send(random.choice(["WAY 😤", "Yes way! 💀", "Believe it! 🔥"]))
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
    embed.set_footer(text="Type your answer! | !hint for a clue | Correct = +50 XP +100 coins!")
    await ctx.send(embed=embed)
    await asyncio.sleep(30)
    if ctx.channel.id in trivia_sessions:
        del trivia_sessions[ctx.channel.id]
        await ctx.send(f"⏰ Time's up! The answer was **{q['a']}**!")

@bot.command(name="hint")
async def hint(ctx):
    if ctx.channel.id in trivia_sessions:
        await ctx.send(f"💡 Hint: {trivia_sessions[ctx.channel.id]['hint']}")
    else:
        await ctx.send("No active trivia! Use `!trivia` to start one.")

# ---- SOCIAL COMMANDS ----
@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!hug @user`")
        return
    await ctx.send(random.choice(hug_messages).format(author=ctx.author.mention, target=member.mention))

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!kiss @user`")
        return
    await ctx.send(random.choice(kiss_messages).format(author=ctx.author.mention, target=member.mention))

@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!slap @user`")
        return
    await ctx.send(random.choice(slap_messages).format(author=ctx.author.mention, target=member.mention))

@bot.command(name="cuddle")
async def cuddle(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!cuddle @user`")
        return
    await ctx.send(random.choice(cuddle_messages).format(author=ctx.author.mention, target=member.mention))

@bot.command(name="highfive")
async def highfive(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!highfive @user`")
        return
    await ctx.send(random.choice(highfive_messages).format(author=ctx.author.mention, target=member.mention))

@bot.command(name="roast")
async def roast(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!roast @user`")
        return
    await ctx.send(f"{member.mention} {random.choice(roasts)}")

# ---- MINI GAMES ----
@bot.command(name="coinflip")
async def coinflip(ctx):
    await ctx.send(f"🪙 Flipping... **{random.choice(['Heads 🪙', 'Tails 🪙'])}**!")

@bot.command(name="dice")
async def dice(ctx):
    result = random.randint(1, 6)
    faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
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
    elif (player=="rock" and bot_choice=="scissors") or \
         (player=="paper" and bot_choice=="rock") or \
         (player=="scissors" and bot_choice=="paper"):
        result = "You win! 🎉"
    else:
        result = "I win! 😈"
    await ctx.send(f"You: {emojis[player]} vs Me: {emojis[bot_choice]}\n**{result}**")

@bot.command(name="battle")
async def battle(ctx, member: discord.Member = None):
    if not member or member == ctx.author:
        await ctx.send("❌ Tag someone else! Example: `!battle @user`")
        return
    winner = random.choice([ctx.author, member])
    loser = member if winner == ctx.author else ctx.author
    await ctx.send(f"⚔️ **BATTLE!**\n{ctx.author.mention} vs {member.mention}\n\n🏆 **{winner.mention}** {random.choice(battle_moves)} {loser.mention} with a {random.choice(weapons)}!")

# ---- XP COMMANDS ----
@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    target = member or ctx.author
    d = get_xp(target.id, target.display_name)
    next_xp = xp_for_next_level(d["level"])
    embed = discord.Embed(title=f"⭐ {target.display_name}'s Level", color=discord.Color.gold())
    embed.add_field(name="Level", value=f"**{d['level']}**", inline=True)
    embed.add_field(name="XP", value=f"**{d['xp']}** / {next_xp}", inline=True)
    embed.set_thumbnail(url=target.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="leaderboard")
async def leaderboard(ctx):
    if not xp_data:
        await ctx.send("No XP data yet! Start chatting! 💬")
        return
    sorted_data = sorted(xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
    embed = discord.Embed(title="🏆 XP Leaderboard", color=discord.Color.gold())
    medals = ["🥇","🥈","🥉"]
    desc = ""
    for i, (uid, d) in enumerate(sorted_data):
        medal = medals[i] if i < 3 else f"**#{i+1}**"
        desc += f"{medal} {d.get('name', 'Unknown')} — Level {d['level']} ({d['xp']} XP)\n"
    embed.description = desc
    await ctx.send(embed=embed)

# ---- ECONOMY ----
@bot.command(name="balance")
async def balance(ctx, member: discord.Member = None):
    target = member or ctx.author
    eco = get_eco(target.id)
    embed = discord.Embed(title=f"💰 {target.display_name}'s Balance", color=discord.Color.green())
    embed.add_field(name="Coins", value=f"**{eco['coins']} 🪙**", inline=True)
    embed.set_thumbnail(url=target.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="daily")
async def daily(ctx):
    eco = get_eco(ctx.author.id)
    now = datetime.now()
    last = eco.get("last_daily")
    if last:
        diff = now - last
        if diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - diff
            hours = int(remaining.seconds / 3600)
            mins = int((remaining.seconds % 3600) / 60)
            await ctx.send(f"⏰ Already claimed! Come back in **{hours}h {mins}m**!")
            return
    coins = random.randint(100, 500)
    eco["coins"] += coins
    eco["last_daily"] = now
    await ctx.send(f"✅ {ctx.author.mention} claimed daily reward! **+{coins} coins** 🪙\nBalance: **{eco['coins']} coins**!")

@bot.command(name="work")
async def work(ctx):
    eco = get_eco(ctx.author.id)
    now = datetime.now()
    last = eco.get("last_work")
    if last:
        diff = now - last
        if diff < timedelta(hours=1):
            mins = int((timedelta(hours=1) - diff).seconds / 60)
            await ctx.send(f"⏰ You're tired! Rest **{mins} more minutes**!")
            return
    job, min_pay, max_pay = random.choice(jobs)
    earned = random.randint(min_pay, max_pay)
    eco["coins"] += earned
    eco["last_work"] = now
    await ctx.send(f"💼 {ctx.author.mention} worked as **{job}** and earned **{earned} coins** 🪙!")

# ---- OTHER ----
@bot.command(name="vibe")
async def vibe(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"✨ {target.mention}'s vibe today: **{random.choice(vibes)}**")

@bot.command(name="rate")
async def rate(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("❌ Tag someone! Example: `!rate @user`")
        return
    score = round(random.uniform(1, 10), 1)
    label = "LEGENDARY! 👑" if score>=9 else "Pretty awesome! 🔥" if score>=7 else "Not bad! 👍" if score>=4 else "Needs improvement 😬"
    await ctx.send(f"⭐ I rate {member.mention} **{score}/10** — {label}")

@bot.command(name="dad")
async def dad(ctx):
    await ctx.send(random.choice(dad_responses))

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! I'm **v4mp's child** 🤖✨")

@bot.command(name="about")
async def about(ctx):
    embed = discord.Embed(title="About Me 🤖", description="I am **v4mp's child** — made by the legendary **v4mp**!", color=discord.Color.purple())
    embed.add_field(name="👨 Dad", value="v4mp", inline=True)
    embed.add_field(name="🎂 Purpose", value="To make this server fun!", inline=True)
    embed.set_footer(text="Made with ❤️ by v4mp")
    await ctx.send(embed=embed)

@bot.command(name="commands")
async def commands_list(ctx):
    embed = discord.Embed(title="📋 v4mp's child — All Commands", color=discord.Color.purple())
    embed.add_field(name="🎉 Fun", value="`!joke` `!fact` `!quote` `!meme` `!8ball <question>`", inline=False)
    embed.add_field(name="🧠 Trivia", value="`!trivia` `!hint`", inline=False)
    embed.add_field(name="💖 Social", value="`!hug @` `!kiss @` `!slap @` `!cuddle @` `!highfive @` `!roast @`", inline=False)
    embed.add_field(name="🎮 Games", value="`!coinflip` `!dice` `!rps` `!battle @`", inline=False)
    embed.add_field(name="⭐ XP", value="`!level` `!leaderboard`", inline=False)
    embed.add_field(name="💰 Economy", value="`!balance` `!daily` `!work`", inline=False)
    embed.add_field(name="😄 Other", value="`!vibe` `!rate @` `!dad` `!about`", inline=False)
    embed.add_field(name="💬 Auto-Reply", value="gm • gn • f • gg • lol • brb • same • no way • i'm bored • who's your dad • hi/hello/hey", inline=False)
    embed.set_footer(text="Chat to earn XP! ⭐ | Random events every 30-90 mins! 🎲")
    await ctx.send(embed=embed)

# ---- RUN ----
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(token)
