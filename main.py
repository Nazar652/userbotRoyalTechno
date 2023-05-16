import threading
from flask import Flask, render_template
from pyrogram import Client, filters

from database import *
from config import *

app = Flask(__name__)
client = Client("client",
                api_id=api_id,
                api_hash=api_hash)


@client.on_message(filters.group & ~filters.me & (filters.text | filters.caption))
async def message_handler(c, m):
    UserMessages.new_message(m)
    is_spam = UserMessages.check_spam(m)

    if is_spam:
        chats = Chat.select().execute()
        for c in chats:
            await client.ban_chat_member(c.id, m.from_user.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/clear', methods=['DELETE'])
async def clear_users():
    user_ids = UserMessages.get_inactive_users()

    chats = Chat.select().execute()
    for u_id in user_ids:
        for c in chats:
            await client.ban_chat_member(c.id, u_id)

    return {'amount': len(user_ids)}


if __name__ == "__main__":
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    client.run()
