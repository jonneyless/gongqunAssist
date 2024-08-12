import telethon.tl.types
import db
import db_redis
import tg
import helpp
import template
from helpp import send
from assist import *
import assist
import re


async def index(bot, event, chat_id, sender_id, text, message):
    re1 = "(.*?)公群(.*?)已处理"
    result1 = re.search(re1, text)
    if result1 is not None:
        await processed(bot, event, chat_id, sender_id, text, result1)
        return

    patten = "恢复\\s*公群\\s*(\\d+)"
    result = re.search(patten, text)
    if result is not None:
        official = await db.official_one(sender_id)
        if official is None:
            return

        groupNum = result.group(1)
        checkTime = await db_redis.group_restore_get(groupNum)
        if checkTime is not None:
            await event.reply("公群" + str(groupNum) + ' 已有恢复操作')
            return

        await db_redis.group_restore_set(groupNum)

        groups = await db.getGroupByNum(groupNum)
        if len(groups) == 0:
            await db_redis.group_restore_del(groupNum)
            await event.reply("公群" + str(groupNum) + ' 不存在')
            return
        elif len(groups) > 1:
            await db_redis.group_restore_del(groupNum)
            await event.reply("后台有多个对应群，请删除其他无效群后重试")
            return

        group = groups[0]
        tmpGroup = await db.getTempGroupOne()
        print(tmpGroup['chat_id'])
        if tmpGroup is None:
            await db_redis.group_restore_del(groupNum)
            await event.reply("缺少可供恢复的临时群")
            return

        groupId = tmpGroup['chat_id']

        botUrl = helpp.get_bot_url(groupId, 2)

        noticeText = "开始处理...\n\n"
        notice = await event.reply("开始处理")

        tg.setChatTitle(botUrl, groupId, group['title'])
        noticeText += "已设置群名\n"
        await notice.edit(noticeText)

        if 'description' in group and group['description'] != "":
            tg.setChatDescription(botUrl, groupId, group['description'])
            noticeText += "已设置群简介\n"
            await notice.edit(noticeText)

        tg.deleteChatPhoto(botUrl, groupId)
        noticeText += "已清理群头像\n"
        await notice.edit(noticeText)

        ruleId = tg.sendMessage(botUrl, groupId, group['rules'])
        tg.pinChatMessage(botUrl, groupId, ruleId)
        noticeText += "已置顶群规则\n"
        await notice.edit(noticeText)

        admins = await db.getGroupAdminUsernames(group['chat_id'])
        noticeText = "恢复成功！\n\n"
        for admin in admins:
            if admin['custom_title'].find('老板'):
                noticeText += "老板： @" + admin['username'] + "\n"

        i = 0
        for admin in admins:
            if admin['custom_title'].find('业务员'):
                i = i + 1
                noticeText += "业务员" + str(i) + "： @" + admin['username'] + "\n"

        noticeText += "新群链接：" + tmpGroup['url']

        await notice.edit(noticeText)
        await db.restoreGroup(groupId, group)
        await db_redis.group_restore_del(groupNum)


async def processed(bot, event, chat_id, sender_id, text, result1):
    zl_user = await db.zl_user_one(sender_id)
    if zl_user is None:
        return

    text_type = result1.group(1)
    num = result1.group(2)

    group = await db.group_one_by_num(num)
    if group is None:
        await event.reply("公群 %s 不存在" % num)
        return
    group_tg_id = group["chat_id"]

    typee = assist.get_command_type(text_type)
    if int(typee) < 0:
        await event.reply("指令错误")
        return

    print("%s %s" % (text, typee))

    num = await db.zl_notice_over_count(zl_user, group_tg_id, sender_id, typee)

    await db.zl_notice_over(zl_user, group_tg_id, sender_id, typee)

    await event.reply("成功，处理%s条" % num)