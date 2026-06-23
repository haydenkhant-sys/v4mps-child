import discord
from discord.ext import commands
import random
import os
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- DATA ----

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
    ("Why can't Elsa have a balloon?", "She'll let it go! ❄️"),
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
    "Cleopatra lived closer to the Moon landing than to the pyramids 🏛️",
    "The average person walks past 36 murderers in their lifetime 😨",
    "Crows can recognize and remember human faces 🐦",
    "Wombat poop is cube-shaped 🟫",
    "Butterflies taste with their feet 🦋",
    "A snail can sleep for 3 years 🐌",
]

quotes = [
    "\"Be yourself; everyone else is already taken.\" — Oscar Wilde ✨",
    "\"The only way to do great work is to love what you do.\" — Steve Jobs 💪",
    "\"In the middle of every difficulty lies opportunity.\" — Einstein 🧠",
    "\"Life is what happens when you're busy making other plans.\" — John Lennon 🎵",
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
    "Friday energy vs Monday energy 📊 (Friday wins 1000%)",
    "When someone says 'just a quick question' and it's not quick 😐",
    "Nobody: ... Me at 2am: let me reorganize my entire life 🌙",
]

rizz_lines = [
    "Your smile could crash Discord servers 😍",
    "Are you a magician? Because whenever I look at you, everyone else disappears ✨",
    "Do you have a map? I keep getting lost in your eyes 🗺️",
    "Are you WiFi? Because I'm feeling a connection 📶",
    "You must be a keyboard, because you're just my type 💻",
    "Is your name Google? Because you have everything I've been searching for 🔍",
    "Are you a camera? Every time I see you, I smile 📸",
    "You're so sweet, you'd put Willy Wonka out of business 🍫",
]

vibes = [
    "Chaotic but make it cute 💅",
    "Main character energy today 🌟",
    "Unhinged but in a fun way 😈",
    "Cozy and unbothered 🧸",
    "That 'I woke up like this' energy ✨",
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
    "You're not stupid, you just have bad luck thinking. 🧠",
]

random_events = [
    "{user} just tripped over nothing 😂",
    "Server energy +10 🔥 thanks to {user}!",
    "Breaking news: {user} is built different 💪",
    "{user} just said something and the whole server felt it 👀",
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
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower().strip()

    # Who's your dad
    if any(x in content for x in ["who's your dad", "whos your dad", "who is your dad", "who is ur dad"]):
        await message.channel.send(random.choice(dad_responses))
        return

    # Greetings
    if content in ["hello", "hi", "hey", "hello!", "hi!", "hey!"]:
        await message.channel.send(f"Hey {message.author.mention}! I'm **v4mp's child** 👋 Type `!commands` to see what I can do!")
        return

    # Good morning
    if "good morning" in content or content == "gm":
        greetings = [
            f"Good morning {message.author.mention}! Rise and grind! ☀️",
            f"Morning {message.author.mention}! Don't forget to touch grass today 🌿",
            f"Good morning {message.author.mention}! Today is gonna be your day! 🌟",
            f"Wakey wakey {message.author.mention}! ☀️ The world needs your energy!",
        ]
        await message.channel.send(random.choice(greetings))
        return

    # Good night
    if "good night" in content or content in ["gn", "gn!", "goodnight"]:
        nights = [
            f"Good night {message.author.mention}! Don't let the bed bugs bite 🌙",
            f"Night night {message.author.mention}! Sweet dreams 💤",
            f"Sleep well {message.author.mention}! See you tomorrow ⭐",
            f"Bye bye {message.author.mention}! Go touch your pillow 🛏️",
        ]
        await message.channel.send(random.choice(nights))
        return

    # F in chat
    if content == "f":
        await message.channel.send("F in the chat 🫡")
        return

    # GG
    if content in ["gg", "gg!", "ggs"]:
        await message.channel.send("GG EZ 🎮")
        return

    # LOL
    if content in ["lol", "lmao", "lmfao", "haha", "hahaha"]:
        replies = ["😂😂😂", "LMAOOO 💀", "bro really typed that 😭", "I'm dead 💀💀", "fr fr 😂"]
        await message.channel.send(random.choice(replies))
        return

    # BRB
    if content in ["brb", "brb!"]:
        await message.channel.send(f"See you soon {message.author.mention}! 👋")
        return

    # v4mp mentioned
    if "v4mp" in content and message.author.name.lower() != "v4mp":
        if random.random() < 0.5:
            await message.channel.send(random.choice(v4mp_compliments))
            return

    await bot.process_commands(message)

# ---- RANDOM EVENT TASK ----
async def random_event_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(random.randint(1800, 5400))  # every 30-90 mins
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
async def eightball(ctx, *, question: str):
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

# ---- SOCIAL COMMANDS ----
@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    target = member or ctx.author
    msg = random.choice(hug_messages).format(author=ctx.author.mention, target=target.mention)
    await ctx.send(msg)

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
    target = member or ctx.author
    msg = random.choice(kiss_messages).format(author=ctx.author.mention, target=target.mention)
    await ctx.send(msg)

@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
    target = member or ctx.author
    msg = random.choice(slap_messages).format(author=ctx.author.mention, target=target.mention)
    await ctx.send(msg)

@bot.command(name="cuddle")
async def cuddle(ctx, member: discord.Member = None):
    target = member or ctx.author
    msg = random.choice(cuddle_messages).format(author=ctx.author.mention, target=target.mention)
    await ctx.send(msg)

@bot.command(name="highfive")
async def highfive(ctx, member: discord.Member = None):
    target = member or ctx.author
    msg = random.choice(highfive_messages).format(author=ctx.author.mention, target=target.mention)
    await ctx.send(msg)

@bot.command(name="roast")
async def roast(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"{target.mention} {random.choice(roasts)}")

@bot.command(name="rizz")
async def rizz(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"💘 {ctx.author.mention} → {target.mention}: *{random.choice(rizz_lines)}*")

# ---- MINI GAMES ----
@bot.command(name="coinflip")
async def coinflip(ctx):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await ctx.send(f"🪙 Flipping coin... **{result}**!")

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
        result = "I win! 😈"
    await ctx.send(f"You: {emojis[player]} vs Me: {emojis[bot_choice]}\n**{result}**")

# ---- OTHER COMMANDS ----
@bot.command(name="vibe")
async def vibe(ctx, member: discord.Member = None):
    target = member or ctx.author
    await ctx.send(f"✨ {target.mention}'s vibe today: **{random.choice(vibes)}**")

@bot.command(name="rate")
async def rate(ctx, member: discord.Member = None):
    target = member or ctx.author
    score = round(random.uniform(1, 10), 1)
    if score >= 9:
        label = "LEGENDARY! 👑"
    elif score >= 7:
        label = "Pretty awesome! 🔥"
    elif score >= 4:
        label = "Not bad! 👍"
    else:
        label = "Needs improvement 😬"
    await ctx.send(f"⭐ I rate {target.mention} **{score}/10** — {label}")

@bot.command(name="ship")
async def ship(ctx, member1: discord.Member, member2: discord.Member = None):
    target2 = member2 or ctx.author
    score = random.randint(1, 100)
    if score >= 80:
        verdict = "Perfect match! Get married already! 💍"
    elif score >= 60:
        verdict = "Pretty good chemistry! 💕"
    elif score >= 40:
        verdict = "Could work with some effort 🤔"
    else:
        verdict = "Yikes... maybe just stay friends 😅"
    embed = discord.Embed(title="💘 Ship Calculator", color=discord.Color.pink())
    embed.add_field(name="Couple", value=f"{member1.mention} + {target2.mention}", inline=False)
    embed.add_field(name="Compatibility", value=f"**{score}%** — {verdict}", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="battle")
async def battle(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("You can't battle yourself... or can you? 🤔")
        return
    winner = random.choice([ctx.author, member])
    loser = member if winner == ctx.author else ctx.author
    weapon = random.choice(weapons)
    move = random.choice(battle_moves)
    await ctx.send(f"⚔️ **BATTLE!**\n{ctx.author.mention} vs {member.mention}\n\n🏆 **{winner.mention}** {move} {loser.mention} with a {weapon}!")

@bot.command(name="dad")
async def dad(ctx):
    await ctx.send(random.choice(dad_responses))

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! I'm **v4mp's child** 🤖✨")

@bot.command(name="about")
async def about(ctx):
    embed = discord.Embed(
        title="About Me 🤖",
        description="I am **v4mp's child** — made by the legendary **v4mp**!",
        color=discord.Color.purple()
    )
    embed.add_field(name="👨 Dad", value="v4mp", inline=True)
    embed.add_field(name="🎂 Purpose", value="To make this server fun!", inline=True)
    embed.set_footer(text="Made with ❤️ by v4mp")
    await ctx.send(embed=embed)

@bot.command(name="commands")
async def commands_list(ctx):
    embed = discord.Embed(title="📋 v4mp's child — All Commands", color=discord.Color.purple())
    embed.add_field(name="🎉 Fun", value="`!joke` `!fact` `!quote` `!meme` `!8ball <q>`", inline=False)
    embed.add_field(name="💖 Social", value="`!hug` `!kiss` `!slap` `!cuddle` `!highfive` `!roast` `!rizz`", inline=False)
    embed.add_field(name="🎮 Games", value="`!coinflip` `!dice` `!rps rock/paper/scissors`", inline=False)
    embed.add_field(name="⭐ Other", value="`!rate` `!ship` `!vibe` `!battle` `!dad` `!about`", inline=False)
    embed.add_field(name="💬 Auto-Reply", value="gm • gn • f • gg • lol • brb • who's your dad • hi/hello/hey", inline=False)
    embed.set_footer(text="Random events happen automatically every 30-90 mins! 🎲")
    await ctx.send(embed=embed)

# ---- RUN ----
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(token)
