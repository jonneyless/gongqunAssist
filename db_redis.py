import time

import redis
import json
from config import redisInfo

pool = redis.ConnectionPool(host=redisInfo['host'], port=redisInfo['port'], db=12)

prefix = "gongAssist_"


# ======================================================================================================================

def get_conn():
    return redis.Redis(connection_pool=pool)


# ======================================================================================================================

async def group_num_get(group_tg_id):
    key = prefix + "group_num" + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return str(val, encoding="utf-8")


async def group_num_set(group_tg_id, num):
    key = prefix + "group_num" + str(group_tg_id)
    
    conn = get_conn()
    
    conn.set(key, num, 1800)  # 1小时


async def group_obj_get(group_tg_id):
    key = prefix + "group_obj" + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_obj_set(group_tg_id, obj):
    key = prefix + "group_obj" + str(group_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(obj), 1800)  # 1小时
    
    
# ----------------------------------------------------------------------------------------------------------------------

async def last_message_id_get(group_tg_id, key_short="m"):
    key = prefix + key_short + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return int(conn.get(key))


async def last_message_id_set(group_tg_id, message_id, key_short="m"):
    key = prefix + key_short + str(group_tg_id)
    
    conn = get_conn()

    conn.set(key, message_id, 86400)  # 一天
    

# ----------------------------------------------------------------------------------------------------------------------

async def zl_user_set(user_tg_id, data):
    key = prefix + "zl_user" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(data), 300)


async def zl_user_get(user_tg_id):
    key = prefix + "zl_user" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)
        
    
async def user_set(user_tg_id, data):
    key = prefix + "admin_user_q2" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(data), 300)


async def user_get(user_tg_id):
    key = prefix + "admin_user_q2" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


async def group_restore_get(groupId):
    key = prefix + ":group:restore:" + str(groupId)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return val


async def group_restore_del(groupId):
    key = prefix + ":group:restore:" + str(groupId)

    conn = get_conn()

    val = conn.delete(key)


async def group_restore_set(groupId):
    key = prefix + ":group:restore:" + str(groupId)

    conn = get_conn()

    res = conn.set(key, int(time.time()), 1800)



async def group_restore_del(groupId):
    key = prefix + ":group:restore:" + str(groupId)

    conn = get_conn()

    res = conn.delete(key)
        