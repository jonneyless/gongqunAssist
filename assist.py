import time
import html
import string
import re


def get_month(created_at):
    created_at_timestamp = time2timestamp(created_at)
    
    return int(time.strftime("%m", time.localtime(created_at_timestamp)))
    
    
def timestamp2yue(t):
    yue = time.strftime("%m", time.localtime(t))
    
    return int(yue)
    
    
def get_right_date(year, month, day, timeDetail):
    created_at = "%s-%s-%s %s" % (year, month, day, timeDetail)
    
    i = 0
    flag = True
    while flag and i < 9:
        try:
            int(time.mktime(time.strptime(created_at, '%Y-%m-%d %H:%M:%S')))
            flag = False
        except:
            day = int(day) - 1
            created_at = "%s-%s-%s %s" % (year, month, day, timeDetail)
            flag = True
            i = i + 1
            
    return created_at
    
    
def getNextMonth(t, num=1):
    created_at_timestamp = int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    
    year = int(time.strftime("%Y", time.localtime(created_at_timestamp)))
    month = int(time.strftime("%m", time.localtime(created_at_timestamp)))
    day = int(time.strftime("%d", time.localtime(created_at_timestamp)))
    timeDetail = time.strftime("%H:%M:%S", time.localtime(created_at_timestamp))
    
    month = month + num
    
    if month > 36:
        month = month - 36
        year = year + 3
    elif month > 24:
        month = month - 24
        year = year + 2
    elif month > 12:
        month = month - 12
        year = year + 1
     
    if month < 10:
        month = "0%s" % month
        
    if day < 10:
        day = "0%s" % day
        
    return get_right_date(year, month, day, timeDetail)
    
    
def get_baobei_msg(text):
    # text = htmlspecialchars_php(text)
    # text_temp = text.lower()
    text_temp = text
    
    user_username = None
    user_money = None
    user_day = None
    user_group_num = None
    
    text_temp_arr = text_temp.split("\n")
    for text_temp_item in text_temp_arr:
        text_temp_item = text_temp_item.replace("\n", "")
        text_temp_item = text_temp_item.replace(" ", "")
        
        if text_temp_item.find("交易方对接人") >= 0:
            user_username = re.search("交易方对接人：@(.*)", text_temp_item)
        elif text_temp_item.find("交易金额") >= 0:
            text_temp_item = text_temp_item.replace("U", "u")
            user_money = re.search("交易金额：(.*?)u", text_temp_item)
        elif text_temp_item.find("订单完成时间") >= 0:
            user_day = re.search("订单完成时间：(.*?)天", text_temp_item)
        elif text_temp_item.find("公群") >= 0:
            text_temp_item = text_temp_item.replace(":", "")
            text_temp_item = text_temp_item.replace("：", "")
            text_temp_item = text_temp_item.replace("公群", "")
            if is_number(text_temp_item):
                user_group_num = text_temp_item
                
    return user_username, user_money, user_day, user_group_num
    
    
def htmlspecialchars_php(temp):
    return html.escape(temp)


def to_num2(num):
    num_float = float(num)
    num_int = int(num_float)

    if num_int == num_float:
        return num_int

    return round(num_float, 2)
    

def has_chiness(text):
    result = re.search('[\u4e00-\u9fa5]', text)
    if result is not None:
        return True
    else:
        return False
        
        
def is_number(s):
    if len(s) == 0:
        return False

    if has_chiness(s):
        return False

    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        for i in s:
            unicodedata.numeric(i)
        return True
    except (TypeError, ValueError):
        pass
    
    return False


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_current_timestamp():
    return int(time.time())


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def handle_sender(sender):
    obj = {
        "id": sender.id,
        "tg_id": sender.id,
        "user_tg_id": sender.id,
        "username": "",
        "firstname": "",
        "lastname": "",
        "fullname": "",
        "first_name": "",
        "last_name": "",
        "full_name": "",
    }

    if hasattr(sender, "username") and sender.username is not None:
        obj["username"] = sender.username

    if hasattr(sender, "first_name") and sender.first_name is not None:
        obj["firstname"] = sender.first_name

    if hasattr(sender, "last_name") and sender.last_name is not None:
        obj["lastname"] = sender.last_name

    firstname = obj["firstname"]
    lastname = obj["lastname"]

    firstname = firstname.replace("'", "")
    lastname = lastname.replace("'", "")

    firstname = firstname.replace("\\", "")
    lastname = lastname.replace("\\", "")

    firstname = htmlspecialchars_php(firstname)
    lastname = htmlspecialchars_php(lastname)

    fullname = firstname + lastname

    obj["firstname"] = firstname
    obj["lastname"] = lastname
    obj["first_name"] = firstname
    obj["last_name"] = lastname

    obj["fullname"] = fullname
    obj["full_name"] = fullname

    return obj


def get_status_info(status):
    status = int(status)

    if status == 1:
        return "<s>已处理</s>"
    else:
        return "未处理"


def has_prev(page):
    flag = False
    if page > 1:
        flag = True

    return flag


def has_next(page, count, page_len):
    flag = False
    if page * page_len < count:
        flag = True

    return flag


def get_max_page(count, page_len):
    page_temp = count / page_len
    page = int(page_temp)

    if page_temp > page:
        page = page + 1

    return page


def replace_string_en(text):
    punctuation_str = string.punctuation
    for i in punctuation_str:
        text = text.replace(i, "")

    # punctuation_str = punctuation
    # for i in punctuation_str:
    #     text = text.replace(i, "")

    return text
    
    
def is_command(text):
    if text.find("公群") > 0 and text.find("已处理") > 0:
        return True

    if text.find("公群") > 0 and text.find("恢复") >= 0:
        return True
        
    return False
    
    
def is_cha(text):
    if text.find("查") >= 0:
        return True
        
    return False
    
    
def get_command_type(text):
# 交易员
# 1 超押监控 chaoya
# 2 负记账 fu
# 3 报备超押 bbchaoya
# 4 报备异常 bbyc
# 5 未结算 wei
# 6 异常记账 yichang
# 7 漏统计记账 lou
# 8 规则 guize

# 巡查
# 20 踢人 ban
# 21 拉人 la
# 22 上下课 sxke
# 23 进群 in
# 24 引流 yin

# 公群巡视员
# 31 管理 admin
    
    if text == "chaoya" or text == "超押监控" or text == "超":
        return 1
    elif text == "fu" or text == "负记账" or text == "负":
        return 2
    elif text == "bbchaoya" or text == "报备超押" or text == "报超":
        return 3 
    elif text == "bbyc" or text == "报备异常" or text == "报":
        return 4
    elif text == "wei" or text == "未结算" or text == "未":
        return 5 
    elif text == "yichang" or text == "异常记账" or text == "异":
        return 6
    elif text == "lou" or text == "漏统计记账" or text == "漏":
        return 7 
    elif text == "guize" or text == "规则" or text == "规":
        return 8
    elif text == "ban" or text == "踢人" or text == "踢":
        return 20
    elif text == "la" or text == "拉人" or text == "拉":
        return 21
    elif text == "sxke" or text == "上下课" or text == "上":
        return 22 
    elif text == "in" or text == "进群" or text == "进":
        return 23
    elif text == "yin" or text == "引流" or text == "引":
        return 24 
    elif text == "admin" or text == "管理" or text == "管":
        return 31
        
    return -1
    
    
def get_simple_time(created_at):
    return time.strftime("%m-%d %H:%M", time.localtime(time2timestamp(str(created_at)) - 3600))
    
    
    
    