import telethon.tl.types
import db
import re
import tg
import helpp
import template
from helpp import send
from assist import *
import httpp


async def index(bot, event, chat_id, sender_id, text):
    official = await db.official_one(sender_id)
    if official is None:
        return
    
    text = text.replace(" ", "")
    text = text.lower()
    if text.find("查公群") >= 0:
        num = text.replace("查公群", "")
        if is_number(num):
            group = await db.group_one_by_num(num)
            if group is None:
                await event.reply("不存在该编号 %s 的公群" % num)
                return
            
            group_tg_id = group["chat_id"]
            title = group["title"]
            
            log_danbao = await db.danbao_one(group_tg_id)
            
            qunlaoban = await db.qunlaoban_one(group_tg_id)
            yewuyuans = await db.yewuyuan_all(group_tg_id)
            jiaoyi = await db.jiaoyi_one(group_tg_id)
            
            text_show = title
            if log_danbao is not None:
                text_show += "开群日期：%s\n" % log_danbao["created_at"]
                
            if qunlaoban is None:
                text_show += "群老板：不存在\n"
            else:
                text_show += "群老板：@%s\n" % qunlaoban["username"]
            
            if len(yewuyuans) == 0:
                text_show += "业务员：不存在\n"
            else:
                text_show += "业务员："
                for yewuyuan in yewuyuans:
                    text_show += "@%s " % yewuyuan["username"]
                text_show += "\n"
            
            if jiaoyi is None:
                text_show += "交易员：不存在\n"
            else:
                text_show += "交易员：@%s\n" % jiaoyi["username"]
               
            if log_danbao is not None:
                text_jiufen = await httpp.getJiufen(num, str(log_danbao["created_at"]))
                text_show += text_jiufen
                
                text_show += "月费：%s\n" % log_danbao["yuefei"]
            
            if log_danbao is not None:
                flag, text_yue_no_arr, text_yue_have_arr, remark = helpp.has_yuefei(log_danbao)
                if flag:
                    text_show += "月费已收取\n"
                else:
                    text_yue_no = ""
                    for item in text_yue_no_arr:
                        text_yue_no += "%s，" % item
                        
                    text_show += "未收取：%s\n" % text_yue_no
                    
            if log_danbao is not None:
                fakuan_money, fakuan_num = await httpp.getFakuan(num, str(log_danbao["created_at"]))
                
                text_show += "罚款：%s次，总计：%s\n" % (fakuan_num, fakuan_money)
            
            await event.reply(text_show)
            
    else:
        text_temp = text.replace("查", "")
        if text_temp.find("t") == 0:
            if len(text_temp) < 20 or len(text_temp) > 40:
                await event.reply("不是合法的地址")
                return
            
            msgs = await db.log_msg_address_get(text_temp)
            if len(msgs) == 0:
                await event.reply("没有出现过")
                return
            
            text_show = text
            text_show += "\n"
            for msg in msgs:
                text_show += "%s %s %s, %s\n" % (msg["title"], msg["username"], msg["created_at"], msg["temp"])
                
            await event.reply(text_show)
            return
        
        elif is_number(text_temp):
            user = await db.user_one(text_temp)
            user_tg_id = text_temp
            
            if user is None:
                await event.reply("用户账号不存在")
                return

            text_show = "用户：@%s id：%s\n" % (user["username"], text_temp)
            if len(user["username"]) > 0:
                text_jiufen = await httpp.getJiufenByUsername(user["username"])
                text_show += text_jiufen
                
            jiaoyi_group_tg_ids = []
            jiaoyi_group_tg_ids_jz = await httpp.getJzJiaoyi(user_tg_id)
            jiaoyi_group_tg_ids_bb = await db.group_trade_report_get(user_tg_id)
            
            for item in jiaoyi_group_tg_ids_jz:
                jiaoyi_group_tg_ids.append(item)
            
            for item in jiaoyi_group_tg_ids_bb:
                jiaoyi_group_tg_ids.append(item)
                
            jiaoyi_group_tg_ids = list(set(jiaoyi_group_tg_ids))
                
            text_show += "\n"
                
            if len(jiaoyi_group_tg_ids) == 0:
                text_show += "交易过公群：无"
            else:
                text_show += "交易过公群："
                for jiaoyi_group_tg_id in jiaoyi_group_tg_ids:
                    group = await db.group_num_one(jiaoyi_group_tg_id)
                    if group is not None and int(group) > 0:
                        text_show += "公群%s" % group
                    else:
                        text_show += "" % jiaoyi_group_tg_id
                    
            await event.reply(text_show)
            
            
    