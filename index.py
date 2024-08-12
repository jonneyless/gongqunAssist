from telethon import TelegramClient, events
import telethon.tl.types

from config import *
from assist import *
import handle_private_message
import handle_start
import handle_callback
import handle_command
import handle_cha
import db


bot = TelegramClient('gongqunAssist', app_id, app_hash).start(bot_token=bot_token)


def is_private(chat_id, sender_id):
    flag = False
    if chat_id == sender_id and sender_id > 0:
        flag = True

    return flag


@bot.on(events.NewMessage(incoming=True))
async def new_message(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    
    if sender_id is None:
        return

    chat_id = int(chat_id)
    sender_id = int(sender_id)
    
    message = event.message
    text = message.message

    if is_private(chat_id, sender_id):
        if text == "/start":
            await handle_start.index(bot, event, chat_id, sender_id, text, message)
        elif is_command(text):
            await handle_command.index(bot, event, chat_id, sender_id, text, message)
        elif is_cha(text):
            await handle_cha.index(bot, event, chat_id, sender_id, text)
        else:
            await handle_private_message.index(bot, event, chat_id, sender_id, text, message)
        # try:
        #     await handle_private_message.index(bot, event, chat_id, sender_id, text, message)
        # except:
        #     print("handle_private_message error...")
             
                
@bot.on(events.CallbackQuery())
async def callback(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    callback_data = event.query.data
    callback_data = callback_data.decode('utf-8')

    args = {}
    info = callback_data
    if callback_data.find("?") >= 0:
        arr = callback_data.split("?")
        if len(arr) == 2:
            info = arr[0]
            args_temp = arr[1]

            args_temp = args_temp.split("&")
            for item in args_temp:
                item = item.split("=")
                if len(item) == 2:
                    args[item[0]] = item[1]

    msg_id = int(event.query.msg_id)
        
    await handle_callback.index(bot, event, chat_id, sender_id, msg_id, info, args)
    
    
def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    print("init...")

    main()
