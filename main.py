import discord
import os
from openai import OpenAI
import asyncio

OWNER_ID = 1444007232072061114
BOT_NAME = "RINYARO"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ai = OpenAI(api_key=os.getenv("GROQ_KEY"), base_url="https://api.groq.com/openai/v1")
GROQ_MODEL = "openai/gpt-oss-120b"

def get_ai(question, is_owner, user_name):
    if is_owner:
        loyalty = "THIS IS OYAKATA RIN - YOUR MASTER. Be 1000% kind, sweet, soft to her."
    else:
        loyalty = "Be 100% kind and polite."
    system_prompt = f"You are {BOT_NAME}, CODE HASHIRA, 100% KIND like Thorfinn. {loyalty} Reply 2-4 lines max, super kind. You are RINYARO."
    try:
        r = ai.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"system","content":system_prompt},{"role":"user","content":f"{user_name}: {question}"}], max_tokens=500, temperature=0.6)
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

@client.event
async def on_ready():
    print(f'{BOT_NAME} ONLINE')
    await client.change_presence(activity=discord.Game(name="kind to all | devoted to Rin"))

@client.event
async def on_message(m):
    if m.author.bot: return
    if "rinyaro" not in m.content.lower() and client.user not in m.mentions: return
    is_owner = m.author.id == OWNER_ID
    if "greet" in m.content.lower() and len(m.mentions) >= 1:
        target = [u for u in m.mentions if u.id!= client.user.id]
        if target:
            ans = get_ai(f"Warmly welcome {target[0].display_name}", is_owner, m.author.display_name)
            await m.reply(f"{target[0].mention} {ans}", mention_author=False)
            return
    q_clean = m.content.replace(f"<@{client.user.id}>","").strip() or "hello"
    async with m.channel.typing():
        ans = get_ai(q_clean, is_owner, m.author.display_name)
    await m.reply(ans, mention_author=False)

client.run(os.getenv("DISCORD_TOKEN"))
