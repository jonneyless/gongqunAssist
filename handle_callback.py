import db
import db_redis
import helpp
import assist
import template


async def index(bot, event, chat_id, sender_id, msg_id, info, args):
    zl_user = await db.zl_user_one(sender_id)
    if zl_user is None:
        return
    
    if info == "back":
        typee = int(zl_user["type"])
        await helpp.edit(bot, event, sender_id, msg_id, "...", template.get_btns(typee, zl_user))
        return
        
    page = 1
    if "page" in args:
        page = args["page"]
        
    page_len = 10
        
    status = -1
    if "status" in args:
        status = int(args["status"])
    
    typee = assist.get_command_type(info)
    if int(typee) <= 0:
        return

    # print("%s %s %s %s" % (info, page, page_len, status))
    # print(args)

    notices = await db.zl_notice_groups_all(zl_user, sender_id, typee, page, page_len, status)
    notices_count = await db.zl_notice_groups_count(zl_user, sender_id, typee, status)
    
    await helpp.edit(bot, event, sender_id, msg_id, (await template.msg_notice20_get(notices, sender_id, typee, notices_count, page)), template.button_page_get(info, typee, notices_count, page, page_len, status))
    
    return

