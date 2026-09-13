from flask import Flask
from threading import Thread
import discord
import os
from openai import OpenAI

app = Flask('')
@app.route('/')
def home():
    return "Rinyaro is Online! 24/7"

def run():
  app.run(host='0.0.0.0',port=10000)

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()

OWNER_ID = 144460722072061114
BOT_NAME = "RINYARO"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ai = OpenAI(api_key=os.getenv("GROQ_KEY"), base_url="https://api.groq.com/openai/v1")

@client.event
async def on_ready():
    print(f'{BOT_NAME} ONLINE as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id == OWNER_ID or client.user.mentioned_in(message) or message.content.startswith("!"):
        try:
            async with message.channel.typing():
                resp = ai.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":message.content}]
                )
                await message.reply(resp.choices[0].message.content[:2000])
        except Exception as e:
            print(e)

client.run(os.getenv("DISCORD_TOKEN"))
