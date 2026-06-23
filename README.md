# v4mp's child 🤖

A Discord bot made for v4mp's server!

## Features
- Replies to "who's your dad" → says **v4mp**!
- Auto-greets when you say hi/hello/hey
- `!joke` — tells random jokes
- `!dad` — who is your dad?
- `!8ball <question>` — magic 8ball
- `!flip` — coin flip
- `!roast [@user]` — friendly roasts
- `!hug [@user]` — give hugs
- `!about` — bot info
- `!commands` — show all commands

---

## Setup Guide

### Step 1 — Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it `v4mp's child`
3. Go to **Bot** tab → Click **Add Bot**
4. Copy the **Token** (keep it secret!)
5. Under **Privileged Gateway Intents**, enable:
   - ✅ Message Content Intent
6. Go to **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Read Messages/View Channels`, `Embed Links`
7. Copy the generated URL and invite the bot to your server

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "v4mp's child bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/v4mps-child.git
git push -u origin main
```

### Step 3 — Deploy on Railway
1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repo
4. Go to **Variables** tab → Add:
   ```
   DISCORD_TOKEN = your_bot_token_here
   ```
5. Railway will auto-deploy! ✅

Your bot is now online 24/7! 🎉
