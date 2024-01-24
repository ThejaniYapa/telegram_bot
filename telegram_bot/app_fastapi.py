# Import everything needed
import re
from fastapi import FastAPI, Request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.ai import generate_smart_reply

# Initialize the bot
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# Start the FastAPI app
app = FastAPI()

@app.post('/{token}')
async def respond(token: str, request: Request):
    if token != TOKEN:
        return {"error": "Invalid token"}

    # Retrieve the message in JSON and then transform it to Telegram object
    update_data = await request.json()
    update = telegram.Update.de_json(update_data, bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # For debugging purposes only
    print("got text message :", text)
    # here call your smart reply message
    reply = generate_smart_reply(text)
    bot.sendMessage(chat_id=chat_id, text=reply, reply_to_message_id=msg_id)
    """# The first time you chat with the bot AKA the welcoming message
    if text == "/start":
        bot_welcome = "Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name."
        # Send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
    else:
        try:
            # Clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # Create the api link for the avatar based on http://avatars.adorable.io/
            url = f"https://api.adorable.io/avatars/285/{text.strip()}.png"
            # Reply with a photo to the name the user sent
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # If things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    """
    return {"message": "ok"}

@app.get('/setwebhook')
async def set_webhook():
    # Link the bot to our app
    s = await bot.setWebhook(f'{URL}{TOKEN}')
    # Something to let us know things work
    if s:
        return {"message": "webhook setup ok"}
    else:
        return {"message": "webhook setup failed"}

@app.get('/')
async def index():
    return {"message": "."}

# No need to specify 'if __name__ == "__main__"', as we run the app with Uvicorn
# uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
# web: uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --workers 4

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app_fastapi:app
# web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app_fastapi:app