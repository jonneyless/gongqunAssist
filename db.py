from assist import get_current_time, get_current_timestamp, timestamp2time
from dbpool import OPMysql
import db_redis
import assist


# ======================================================================================================================

async def user_one(user_tg_id):
    obj = await db_redis.user_get(user_tg_id)
    if obj is None:
        opm = OPMysql()
    
        sql = "select * from users_new where tg_id = '%s'" % user_tg_id

        result = opm.op_select_one(sql)
    
        opm.dispose()
        
        if result is not None:
            if result["username"] is None:
                result["username"] = ""
            
            await db_redis.user_set(user_tg_id, {
                "username": result["username"]
            })
    
        return result
    else:
        return obj
    

async def official_one(user_tg_id):
    opm = OPMysql()

    sql = "select * from offical_user where tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def group_num_obj_one(chat_id):
    opm = OPMysql()

    sql = "select group_num, url from groups where (flag = 2 or flag = 4) and status_in = 1 and chat_id = '%s'" % chat_id
    
    result = opm.op_select_one(sql)

    opm.dispose()
    
    return result
        
    # if result is None:
    #     return "-1"
    # else:
    #     return result["group_num"]
        
        
async def group_num_one(chat_id):
    opm = OPMysql()

    sql = "select group_num from groups where (flag = 2 or flag = 4) and status_in = 1 and chat_id = '%s'" % chat_id
    
    result = opm.op_select_one(sql)

    opm.dispose()
    
    if result is None:
        return "-1"
    else:
        return result["group_num"]
        
        
async def group_nums():
    opm = OPMysql()

    sql = "select group_num from groups where (flag = 2 or flag = 4) and status_in = 1 and group_num > 0 and group_num < 10000 order by group_num asc"
    
    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
async def group_one_by_num(group_num):
    opm = OPMysql()

    sql = "select id, title, chat_id from groups where group_num = '%s' and flag = 2 and status_in = 1" % group_num
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    

async def group_link_one(group_tg_id, typee, status=1):
    opm = OPMysql()

    sql = "select * from group_link where group_tg_id = '%s' and type = %s and status = %s" % (group_tg_id, typee, status)
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    

async def group_link_save(group_tg_id, link, typee, user_tg_id, title, creator_tg_id, creator_fullname):
    opm = OPMysql()

    sql = "insert into group_link(group_tg_id, link, type, created_at, user_tg_id, title, creator_tg_id, creator_fullname) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, link, typee, get_current_time(), user_tg_id, title, creator_tg_id, creator_fullname)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def group_link_update(data_id, typee, status=1):
    opm = OPMysql()

    sql = "update group_link set type = %s, status = %s, updated_at = '%s' where id = %s" % (typee, status, get_current_time(), data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
def bot_one(group_tg_id, typee):
    opm = OPMysql()

    sql = "select bots.* from bot_group join bots on bot_group.user_tg_id = bots.tg_id where bot_group.group_tg_id = '%s' and bots.type = %s" % (group_tg_id, typee)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def zl_user_one(user_tg_id):
    obj = await db_redis.zl_user_get(user_tg_id)
    if obj is not None and False:
        return obj
    else:
        opm = OPMysql()
    
        sql = "select * from zl_users where user_tg_id = '%s'" % user_tg_id
        
        result = opm.op_select_one(sql)
    
        opm.dispose()
        
        if result is not None:
            await db_redis.zl_user_set(user_tg_id, result)
            
        return result
    
    
def zl_notice_has(zl_user, user_tg_id, typee):
    opm = OPMysql()
    
    sql = "select * from zl_notice where type = '%s' and status = 2" % typee
    if int(zl_user["type"]) <= 3:
        sql = "select * from zl_notice where user_tg_id = '%s' and type = '%s' and status = 2" % (user_tg_id, typee)
    
    result = opm.op_select_one(sql)

    opm.dispose()

    if result is None:
        return False
    else:
        return True
    
    
async def zl_notice_groups_all(zl_user, user_tg_id, typee, page=1, page_len = 10, status=-1):
    offeset = (int(page) - 1) * int(page_len)
    # 2待处理 1已处理
    
    opm = OPMysql()
    
    sql = "select * from zl_notice where type = '%s' order by status desc, created_at desc limit %s,%s" % (typee, offeset, page_len)
    if int(status) != -1:
        sql = "select * from zl_notice where type = '%s' and status = %s order by status desc, created_at desc limit %s,%s" % (typee, status, offeset, page_len)

    if int(zl_user["type"]) <= 3:
        sql = "select * from zl_notice where user_tg_id = '%s' and type = '%s' order by status desc, created_at desc limit %s,%s" % (user_tg_id, typee, offeset, page_len)
        if int(status) != -1:
            sql = "select * from zl_notice where user_tg_id = '%s' and type = '%s' and status = %s order by status desc, created_at desc limit %s,%s" % (user_tg_id, typee, status, offeset, page_len)
        
    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
async def zl_notice_groups_count(zl_user, user_tg_id, typee, status=-1):
    opm = OPMysql()

    sql = "select count('id') as temp from zl_notice where type = '%s'" % (typee)
    if int(status) != -1:
        sql = "select count('id') as temp from zl_notice where type = '%s' and status = %s" % (typee, status)
    
    if int(zl_user["type"]) <= 3:
        sql = "select count('id') as temp from zl_notice where user_tg_id = '%s' and type = '%s' group by group_tg_id" % (user_tg_id, typee)
        if int(status) != -1:
            sql = "select count('id') as temp from zl_notice where user_tg_id = '%s' and type = '%s' and status = %s group by group_tg_id" % (user_tg_id, typee, status)
    
    result = opm.op_select_one(sql)
    
    opm.dispose()
    
    if result is None:
        return 0
    else:
        return result["temp"]
    
    
async def zl_notice_over_count(zl_user, group_tg_id, user_tg_id, typee):
    opm = OPMysql()

    sql = "select count(id) as temp from zl_notice where group_tg_id = '%s' and type = %s" % (group_tg_id, typee)
    if int(zl_user["type"]) <= 3:
        sql = "select count(id) as temp from zl_notice where group_tg_id = '%s' and user_tg_id = '%s' and type = %s" % (group_tg_id, user_tg_id, typee)
    
    result = opm.op_select_one(sql)

    opm.dispose()
    
    if result is None:
        return 0
    else:
        return result["temp"]
    
    
async def zl_notice_over(zl_user, group_tg_id, user_tg_id, typee):
    opm = OPMysql()

    sql = "update zl_notice set status = 1, updated_at = '%s' where group_tg_id = '%s' and type = %s" % (assist.get_current_time(), group_tg_id, typee)
    if int(zl_user["type"]) <= 3:
        sql = "update zl_notice set status = 1, updated_at = '%s' where group_tg_id = '%s' and user_tg_id = '%s' and type = %s" % (assist.get_current_time(), group_tg_id, user_tg_id, typee)
    
    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
async def zl_notice_over_by_id(data_id):
    opm = OPMysql()

    sql = "update zl_notice set status = 1, updated_at = '%s' where id = %s" % (assist.get_current_time(), data_id)
    
    result = opm.op_update(sql)

    opm.dispose()

    return result
    

# ======================================================================================================================

async def danbao_one(group_tg_id, status = 1):
    opm = OPMysql()

    sql = "select * from log_danbao where group_tg_id = '%s' and status = %s" % (group_tg_id, status)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
async def jiaoyi_one(group_tg_id):
    opm = OPMysql()

    selectSql = "select user_id, username, fullname from group_admin where chat_id = '%s' and fullname like '%%交易员%%'" % group_tg_id

    result = opm.op_select_one(selectSql)

    opm.dispose()

    return result
    
    
async def qunlaoban_one(group_tg_id):
    opm = OPMysql()

    selectSql = "select user_id, username, fullname from group_admin where chat_id = '%s' and custom_title like '%%群老板%%'" % group_tg_id

    result = opm.op_select_one(selectSql)

    opm.dispose()

    return result
    

async def yewuyuan_all(group_tg_id):
    opm = OPMysql()

    selectSql = "select user_id, username, fullname from group_admin where chat_id = '%s' and custom_title like '%%业务员%%'" % group_tg_id

    result = opm.op_select_all(selectSql)

    opm.dispose()

    return result
    
    
def danbao_yuefei_one(data_id, group_num, month, created_at):
    opm = OPMysql()

    sql = "select * from log_danbao_yuefei where title = '%s' and month = '%s' and status = 2 and created_at >= '%s'" % (group_num, month, created_at)
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result

    
# ======================================================================================================================

async def log_msg_address_get(address):
    opm = OPMysql()

    # sql = "select * from log_msg_address where info like '%%%s%%' order by id desc" % address
    sql = "SELECT title, group_tg_id, user_tg_id, username, fullname, created_at, count(id) as temp from log_msg_address where info like '%%%s%%' GROUP BY group_tg_id,user_tg_id ORDER BY created_at desc" % address
    
    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

async def group_trade_report_get(user_tg_id):
    # 10管理已完成 11客户已完成 12官方已完成
    opm = OPMysql()

    sql = "select distinct(group_tg_id) from group_trade_report where user_tg_id = '%s' and (status = 10 or status = 11 or status = 12)" % user_tg_id
    
    result = opm.op_select_all(sql)

    opm.dispose()
    
    data = []
    if result is not None:
        for item in result:
            data.append(item["group_tg_id"])

    return data


async def getGroupByNum(num):
    opm = OPMysql()

    sql = "select * from `groups` where group_num = %s" % int(num)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result

async def getTempGroupOne():
    opm = OPMysql()

    sql = "select * from `groups` where flag = 2 and title regexp '^汇旺[0-9]+' order by id asc limit 1"

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

async def getGroupAdminUsernames(groupId):
    opm = OPMysql()

    sql = "select * from `group_admin` where chat_id = %s" % groupId

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


async def restoreGroup(chatId, group):
    opm = OPMysql()

    description = None
    if 'description' in group:
        description = group['description']

    yajin_u = 0
    if group['yajin_u'] is not None:
        yajin_u = group['yajin_u']

    yajin_m = 0
    if group['yajin_m'] is not None:
        yajin_m = group['yajin_m']

    yajin = 0
    if group['yajin'] is not None:
        yajin = group['yajin']

    yajin_all_u = 0
    if group['yajin_all_u'] is not None:
        yajin_all_u = group['yajin_all_u']

    yajin_all_m = 0
    if group['yajin_all_m'] is not None:
        yajin_all_m = group['yajin_all_m']

    yajin_all = 0
    if group['yajin_all'] is not None:
        yajin_all = group['yajin_all']

    sql = "update `groups` set title = '%s', description = '%s', rules = '%s', yajin_u = %s, yajin_m = %s, yajin = %s, yajin_all_u = %s, yajin_all_m = %s, yajin_all = %s, search_sort = %s where chat_id = %s" %(
        group['title'], description, group['rules'], yajin_u, yajin_m, yajin, yajin_all_u, yajin_all_m, yajin_all, group['search_sort'], chatId
    )

    result = opm.op_update(sql)

    opm.dispose()

    return result
    