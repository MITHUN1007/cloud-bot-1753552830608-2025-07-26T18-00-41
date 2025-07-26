import os
from telethon import TelegramClient, events
from groq import Groq

# API ID and Hash from Telegram
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize Telegram client
client = TelegramClient('session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

@client.on(events.NewMessage)
async def echo(event):
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": event.message.message}],
            model="mixtral-8x7b-32768",
        )
        await event.reply(response.choices[0].message.content)
    except Exception as e:
        print(f"Error processing message: {e}")
        await event.reply("Sorry, I encountered an error processing your request.")

if __name__ == '__main__':
    print("Bot is running...")
    client.run_until_disconnected()