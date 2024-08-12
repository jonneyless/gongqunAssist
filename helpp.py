import db
from config import bot_url
import db_redis
from assist import get_current_timestamp, get_current_time, time2timestamp, timestamp2time, get_month, timestamp2yue, getNextMonth
import math


async def send(bot, event, user_tg_id, msg, buttons=None, flag=False, key_short=""):
    m = None
    
    if buttons is None:
        m = await event.respond(message=msg, parse_mode="html", link_preview=False)
    else:
        m = await event.respond(message=msg, buttons=buttons, parse_mode="html", link_preview=False)
    
    if flag:
        last_m_id = await db_redis.last_message_id_get(user_tg_id, key_short)
        if last_m_id is not None:
            last_m_id = int(last_m_id)
            try:
                await bot.delete_messages(user_tg_id, last_m_id)
            except Exception:
                pass
    
        if m is not None:
            if hasattr(m, "id"):
                await db_redis.last_message_id_set(user_tg_id, m.id, key_short)


async def edit(bot, event, chat_id, msg_id, msg, buttons=None):
    m = None
    
    if buttons is None:
        m = await bot.edit_message(entity=chat_id, message=msg_id, text=msg, parse_mode="html", link_preview=False)
    else:
        m = await bot.edit_message(entity=chat_id, message=msg_id, text=msg, buttons=buttons, parse_mode="html", link_preview=False)
        
        
async def send_text(event, msg):
    return await event.respond(message=msg, buttons=Button.clear(), parse_mode="html", link_preview=False)
    
    
def get_bot_url(group_tg_id, typee):
    bot_url = get_bot_url_default()
    
    bot = db.bot_one(group_tg_id, typee)
    if bot is None:
        print("%s %s no bot" % (group_tg_id, typee))
        return bot_url
    
    print("%s %s %s" % (group_tg_id, typee, bot["username"]))
    
    token = bot["token"]
    bot_url = "https://api.telegram.org/bot%s/" % token

    return bot_url
    

def get_bot_url_default():
    return bot_url
    
    
async def get_num_no(flag = True):
    # flag 默认返回字符串
    
    num_objs = await db.group_nums()
    nums = []
    for num_obj in num_objs:
        nums.append(int(num_obj["group_num"]))
        
    nums.sort()
    nums.append(2)
    nums.append(2)
    nums.append(2)
    nums = set(nums)
    nums = list(nums)
    
    num_first = nums[0]
    num_last = nums[len(nums) - 1]
    
    print(num_first)
    print(num_last)
    
    nums_all = []
    for item in range(num_first, num_last +1):
        item_str = str(item)
        if item_str.find("4") == -1:
            nums_all.append(item)
    
    nums_no = []
    nums_no_str = ""
    for item in nums_all:
        if item not in nums:
            nums_no.append(item)
            nums_no_str += "%s," % item
    
    if flag:
        return nums_no_str
    else:
        return nums_no
        
        
async def get_group_num(group_tg_id):
    num = await db_redis.group_num_get(group_tg_id)
    if num is not None:
        return num
    else:
        num = await db.group_num_one(group_tg_id)
        
        await db_redis.group_num_set(group_tg_id, num)
        
        return num
        
        
async def get_group(group_tg_id):
    obj = await db_redis.group_obj_get(group_tg_id)
    if obj is not None:
        return obj
    else:
        obj = await db.group_num_obj_one(group_tg_id)
        
        await db_redis.group_obj_set(group_tg_id, obj)
        
        return obj
        

def has_yuefei(log_danbao):
    data_id = log_danbao["id"]
    group_tg_id = log_danbao["group_tg_id"]
    created_at = str(log_danbao['created_at'])
    yuefei_day = int(log_danbao['yuefei_day'])
    business_detail_type = int(log_danbao["business_detail_type"])
    group_num = log_danbao["num"]
    now = get_current_time()

    created_at_timestamp = time2timestamp(created_at)
    now_timestamp = get_current_timestamp()
    month_num = math.ceil((now_timestamp - created_at_timestamp) / (86400 * 31))
    
    text_yue_no_arr = []
    text_yue_have_arr = []
    remark = -1
    flag = True # 月费已全部结清
    
    for i in range(month_num + 1):
        start_at = getNextMonth(created_at, 0 + i)
        end_at = getNextMonth(created_at, 1 + i)
        
        print("%s, start_at %s, end_at %s, %s" % (created_at, start_at, end_at, i))
        
        start_timestamp = time2timestamp(start_at)
        end_timestamp = time2timestamp(end_at)
        
        if i == 0:
            if business_detail_type == 300:
                pass
            else:
                # 非卡商中介第一个月不收月费
                continue
        
        if business_detail_type == 300:
            if end_timestamp > now_timestamp:
                break
        else:
            if start_timestamp > now_timestamp:
                break
        
        log_yuefei = db.danbao_yuefei_one(data_id, group_num, get_month(start_at), log_danbao["created_at"])
        
        if log_yuefei is None:
            text_yue_no_arr.append(get_month(start_at))
            
            flag = False
        else:
            text_yue_have_arr.append(get_month(start_at))


    return flag, text_yue_no_arr, text_yue_have_arr, remark
      
      