import telethon.tl.types
import db
import re
import tg
import helpp
from assist import *


async def get_group_by_re(result):
    try:
        num = result.group(1)
        
        if num is None:
            return None, None
        
        if not is_number(num):
            return None, None
        if isinstance(num, int):
            return None, None
        
        return await db.group_one_by_num(num), num
    except:
        pass
    
    return None, None
    
    
async def index(bot, event, chat_id, sender_id, text, message):
# 1、123群审核链接 （永久审核链接）
# 2、123群单个链接（一天1个人链接） 
# 3、123群导航链接（7天前公开链接，7天后自动改审核链接）
# 4、123群广告链接（7天后失效）
# 5、123群月广告链接（30天后失效）
# 6、123注销链接（注销导航链接）

# 7、123群广告审核链接（审核链接7天后失效）
# 8、123群月广告审核链接（审核链接30天后失效）

    re1 = "(.*?)群审核链接"
    re2 = "(.*?)群单个链接"
    re3 = "(.*?)群导航链接"
    re4 = "(.*?)群广告链接"
    re5 = "(.*?)群月广告链接"
    re6 = "(.*?)群注销链接"
    
    re7 = "(.*?)群广告审核链接"
    re8 = "(.*?)群月广告审核链接"
    
    re9 = "群老板链接"
    re10 = "vip群链接"
    re11 = "高级群链接"

    text = text.replace(" ", "")
    
    result1 = re.search(re1, text)
    result2 = re.search(re2, text)
    result3 = re.search(re3, text)
    result4 = re.search(re4, text)
    result5 = re.search(re5, text)
    result6 = re.search(re6, text)
    result7 = re.search(re7, text)
    result8 = re.search(re8, text)
    
    if text == "/start":
        await event.reply("start...")
        return
    
    if result1 is None and result2 is None and result3 is None and result4 is None and result5 is None and result6 is None and result7 is None and result8 is None and text != re9 and text != re10 and text != re11 and text != "未启用群编号":
        return
    
    official = await db.official_one(sender_id)
    if official is None:
        await event.reply("error...")
        return
    
    if text == "未启用群编号":
        info = await helpp.get_num_no()
        info_len = len(info)
        info_len_2 = int(info_len/2)
        
        await event.reply(info[0:info_len_2])
        await event.reply(info[info_len_2:])
        return
    
    if result1 is not None:
        group, num = await get_group_by_re(result1)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 1)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 1, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "永久审核链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
    
    if result2 is not None:
        group, num = await get_group_by_re(result2)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 2)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 2, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "单个用户(24小时有效)链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
        
    if result3 is not None:
        group, num = await get_group_by_re(result3)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        # link_daohang = await db.group_link_one(chat_id, 3, 1)
        # if link_daohang is not None:
        #     await event.reply("该编号的公群已存在导航链接")
        #     return
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 3)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 3, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "导航链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return

    if result4 is not None:
        group, num = await get_group_by_re(result4)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 4)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 4, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "广告链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
    
    if result5 is not None:
        group, num = await get_group_by_re(result5)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 5)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 5, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "月广告链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
        
    if result6 is not None:
        group, num = await get_group_by_re(result6)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]

        link_daohang = await db.group_link_one(chat_id, 3, 1)
        if link_daohang is None:
            await event.reply("该编号的公群不存在导航链接")
            return
        
        # if int(sender_id) != int(link_daohang["user_tg_id"]):
        #     await event.reply("该编号的公群的导航链接不是当前账号创建，无法操作")
        #     return
        
        flag = await tg.revokeChatInviteLink(chat_id, link_daohang["link"])
        if not flag:
            await event.reply("注销导航链接失败，请重试")
            return
        
        await db.group_link_update(link_daohang["id"], 3, 2)
        
        await event.reply("该编号的公群的导航链接 %s 已注销" % link_daohang["link"])
        
        return
    
    if result7 is not None:
        group, num = await get_group_by_re(result7)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 7)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 7, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "群广告审核链接(7天后失效)\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
    
    if result8 is not None:
        group, num = await get_group_by_re(result8)

        if group is None:
            await event.reply("不存在该编号的真公群")
            return
        chat_id = group["chat_id"]
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 8)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 8, sender_id, group["title"], creator_tg_id, creator_fullname)
        
        msg = "%s\n" % group["title"]
        msg += "群月广告审核链接(30天后失效)\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
    
    # re9 = "群老板链接"
    # re10 = "vip群链接"
    # re11 = "svip群链接"
    
    if text == re9:
        chat_id = "-1001620186906"
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 2)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 2, sender_id, "", creator_tg_id, creator_fullname)
        
        msg = "群老板单个用户(24小时有效)链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
    
    if text == re10:
        chat_id = "-1001753191368"
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 2)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 2, sender_id, "", creator_tg_id, creator_fullname)
        
        msg = "vip群单个用户(24小时有效)链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return

    if text == re11:
        chat_id = "-1001601629727"
        
        link, creator_tg_id, creator_fullname = await tg.createBotApproveLink(chat_id, 2)
        if link is None:
            await event.reply("创建链接失败，请重试")
            return
        
        await db.group_link_save(chat_id, link, 2, sender_id, "", creator_tg_id, creator_fullname)
        
        msg = "高级群单个用户(24小时有效)链接\n"
        msg += link
        
        await event.reply(msg, link_preview=False)
        
        return
        
