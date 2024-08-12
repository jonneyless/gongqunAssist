import telethon.tl.types
import db
import re
import tg
import helpp
import template
from helpp import send
from assist import *


async def index(bot, event, chat_id, sender_id, text, message):
    if text == "/start":
        zl_user = await db.zl_user_one(sender_id)
        if zl_user is None:
            return
        
        typee = int(zl_user["type"])
        # # 1交易员 2巡查 3巡视员 10主管 20责任经理 30总经办
        # 🔴
        await send(bot, event, sender_id, "...", template.get_btns(typee, zl_user), True, text)
            
        