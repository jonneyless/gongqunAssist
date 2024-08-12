from telethon import Button

import helpp
import db
from assist import has_prev, has_next, get_simple_time, get_status_info
import math
import json


def get_text_weidu(zl_user, text, typee):
    if db.zl_notice_has(zl_user, zl_user["user_tg_id"], typee):
        text += "🔴"
    
    return text
    

def get_btns(typee, zl_user):
    # 1交易员 2巡查 3巡视员 10主管 20责任经理 30总经办
    buttons = None
    typee = int(typee)
    
    # if typee == 1:
    #     text = "超押监控"
    # elif typee == 2:
    #     text = "负记账"
    # elif typee == 3:
    #     text = "报备超押"
    # elif typee == 4:
    #     text = "报备异常"
    # elif typee == 5:
    #     text = "未结算"
    # elif typee == 6:
    #     text = "异常记账"
    # elif typee == 7:
    #     text = "漏统计记账"
    # elif typee == 8:
    #     text = "规则"
    # elif typee == 20:
    #     text = "踢人"
    # elif typee == 21:
    #     text = "拉人(开启了拉人权限)"
    # elif typee == 22:
    #     text = "上下课"
    # elif typee == 23:
    #     text = "进群(用户10分钟至少申请3次进群)"
    # elif typee == 24:
    #     text = "引流(非官方管理简介中包含：@或链接)"
    # elif typee == 31:
    #     text = "管理(已退押群，20分钟还有非官方管理)"
    
    text1 = "超押监控"
    text2 = "负记账"
    text6 = "异常记账"
    text7 = "漏统计记账"
    text3 = "报备超押"
    text4 = "报备异常"
    text8 = "规则"
    text20 = "踢人"
    text21 = "拉人"
    text22 = "上下课"
    text23 = "进群"
    text24 = "引流"
    text31 = "管理"
    
    text1 = get_text_weidu(zl_user, text1, 1)
    text2 = get_text_weidu(zl_user, text2, 2)
    text6 = get_text_weidu(zl_user, text6, 6)
    text7 = get_text_weidu(zl_user, text7, 7)
    text3 = get_text_weidu(zl_user, text3, 3)
    text4 = get_text_weidu(zl_user, text4, 4)
    text8 = get_text_weidu(zl_user, text8, 8)
    text20 = get_text_weidu(zl_user, text20, 20)
    text21 = get_text_weidu(zl_user, text21, 21)
    text22 = get_text_weidu(zl_user, text22, 22)
    text23 = get_text_weidu(zl_user, text23, 23)
    text24 = get_text_weidu(zl_user, text24, 24)
    text31 = get_text_weidu(zl_user, text31, 31)
    
    buttons1 = [
        [
            Button.inline(text=text1, data="chaoya"),
            Button.inline(text=text2, data="fu"),
            # Button.inline(text="未结算", data="wei"),
            Button.inline(text=text6, data="yichang"),
            Button.inline(text=text7, data="lou"),
        ],
        [
            Button.inline(text=text3, data="bbchaoya"),
            Button.inline(text=text4, data="bbyc"),
            Button.inline(text=text8, data="guize"),
        ],
    ]
    
    buttons2 = [
        [
            Button.inline(text=text20, data="ban"),
            Button.inline(text=text21, data="la"),
            Button.inline(text=text22, data="sxke"),
        ],
        [
            Button.inline(text=text23, data="in"),
            Button.inline(text=text24, data="yin"),
        ]
    ]
    
    buttons3 = [
        [
            # Button.inline(text=text31, data="admin"),
        ],
    ]
    
    if typee == 1:
        buttons = buttons1
    elif typee == 2:
        buttons = buttons2
    elif typee == 3:
        # buttons = buttons3
        pass
    
    if typee > 3:
        buttons = []
        buttons.append(buttons1[0])
        buttons.append(buttons1[1])
        
        buttons.append(buttons2[0])
        buttons.append(buttons2[1])
        
        # buttons.append(buttons3[0])

    return buttons
    

async def msg_notice20_get(notices, user_tg_id, typee, count, page=1, page_len=10):
    typee = int(typee)
    text = ""
    
    if typee == 1:
        text = "超押监控"
    elif typee == 2:
        text = "负记账"
    elif typee == 3:
        text = "报备超押"
    elif typee == 4:
        text = "报备异常"
    elif typee == 5:
        text = "未结算"
    elif typee == 6:
        text = "异常记账"
    elif typee == 7:
        text = "漏统计记账"
    elif typee == 8:
        text = "规则"
    elif typee == 20:
        text = "踢人"
    elif typee == 21:
        text = "拉人(开启了拉人权限)"
    elif typee == 22:
        text = "上下课"
    elif typee == 23:
        text = "进群(用户10分钟至少申请3次进群)"
    elif typee == 24:
        text = "引流(非官方管理简介中包含：@或链接)"
    elif typee == 31:
        text = "管理(已退押群，20分钟还有非官方管理)"
    
    text += "\n\n"

    page_temp = count / page_len
    page_max = math.ceil(page_temp)

    for notice in notices:
        group_tg_id = notice["group_tg_id"]
        status = notice["status"]
        remark = notice["remark"]
        created_at = notice["created_at"]
        
        group = await helpp.get_group(group_tg_id)
        num = -1
        link = ""
        if group is not None:
            num = group["group_num"]
            link = group["url"]
            
        if int(num) == -1:
            await db.zl_notice_over_by_id(notice["id"])
            status = 1
        
        text_gongqun = "<a href='%s'>公群%s</a>" % (link, num)

        text += text_gongqun
        
        if typee == 1:
            text += " %s %s\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 2:
            text += " %s %s\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 3:
            if int(remark) == 1:
                text += " (即将超押)%s %s\n" % (get_status_info(status), get_simple_time(created_at))
            else:
                text += " (已超押)%s %s\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 4:
            text += "\n"
            
            text_arr = remark.split("。")
            text_temp = ""
            num = 0
            for item in text_arr:
                num = num + 1
                item_arr = item.split("，")
                text_temp1 = ""
                for val in item_arr:
                    if val.find("公群") < 0:
                        text_temp1 += "%s" % val
                
                text_temp1 = text_temp1.replace("\n", "")
                text_temp1 = text_temp1.replace("<br/>", "")
                
                text_temp += text_temp1
                if num < len(text_arr):
                    text_temp += "\n"
                    
            text += text_temp
            text += "%s %s\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 5:
            text = "未结算"
        elif typee == 6:
            text += "\n"
            text += "%s\n" % remark
            text += "%s %s\n" % (get_status_info(status), get_simple_time(created_at))
            text += "\n"
        elif typee == 7:
            ups = []
            downs = []
            ups_sum = 0
            downs_sum = 0
            
            try:
                remark = json.loads(remark)
                ups = remark["ups"]
                downs = remark["downs"]
            except:
                print(remark)
            
            for up in ups:
                ups_sum += float(up)
            for down in downs:
                downs_sum += float(down)
            
            text += "\n"
            # text += "上押 %s 笔，金额 %s\n" % (len(ups), ups_sum)
            # text += "下押 %s 笔，金额 %s\n" % (len(downs), downs_sum)
            text += "上押 %s 笔，下押 %s 笔\n" % (len(ups), len(downs))
            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 8:
            remark_arr = remark.split(",")
            
            text += "\n违禁词: %s\n" % remark_arr[len(remark_arr) - 1]
            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 20:
            remark_arr = remark.split("，")
            
            text += "\n%s\n" % remark_arr[len(remark_arr) - 1]
            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 21:
            text += "\n%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 22:
            remark_arr = remark.split("异常")
            
            text += "%s\n" % remark_arr[len(remark_arr) - 1]
            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 23:
            remark_arr = remark.split("进群")
            
            # text += "%s\n" % remark_arr[len(remark_arr) - 1]
            # text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
            text += "%s %s\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 24:
            # remark = "6825910105,汇旺6168https://t.me/+2P-nuvKyL2NhYzc1"
            
            text_user = ""
            try:
                remark_arr = remark.split(",")
                
                user = await db.user_one(remark_arr[0])
                if user is not None:
                    text_user = "@%s" % user["username"]
                else:
                    print("%s %s" % (remark_arr[0], user))
            except:
                pass
            
            text += "\n%s %s\n" % (text_user, remark)

            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        elif typee == 31:
            text += "\n"
            
            remark_arr = remark.split(".")
            remark_temp = ""
            num = 0
            for item in remark_arr:
                num = num + 1
                item = item.replace("\n", "")
                remark_temp += "%s" % item
                if num < len(remark_arr):
                    remark_temp += "\n"
            
            text += "%s" % remark_temp
            text += "%s %s\n\n" % (get_status_info(status), get_simple_time(created_at))
        
    text += "\n%s/%s" % (page, page_max)
    
    return text
    
    
def button_page_get(info, typee, count, page=1, page_len=10, status=-1):
    status = int(status)
    
    buttons = []
    page = int(page)

    page_prve = 1
    if page > 1:
        page_prve = page - 1
        
    page_temp = count / page_len
    page_max = math.ceil(page_temp)
    page_next = page_max
    if page < page_max:
        page_next = page + 1
        
    buttons_row = []
    if has_prev(page):
        buttons_row.append(Button.inline(text="上一页", data="%s?page=%s&status=%s" % (info, page_prve, status)))
    if has_next(page, count, page_len):
        buttons_row.append(Button.inline(text="下一页", data="%s?page=%s&status=%s" % (info, page_next, status)))
    
    buttons_row1 = []
    # 🟢
    if status == -1:
        buttons_row1.append(Button.inline(text="所有🟢", data="%s?page=%s&status=-1" % (info, page_prve)))
    else:
        buttons_row1.append(Button.inline(text="所有", data="%s?page=%s&status=-1" % (info, page_prve)))
    if status == 1:
        buttons_row1.append(Button.inline(text="已处理🟢", data="%s?page=%s&status=1" % (info, page_prve)))
    else:
        buttons_row1.append(Button.inline(text="已处理", data="%s?page=%s&status=1" % (info, page_prve)))
    if status == 2:
        buttons_row1.append(Button.inline(text="未处理🟢", data="%s?page=%s&status=2" % (info, page_prve)))
    else:
        buttons_row1.append(Button.inline(text="未处理", data="%s?page=%s&status=2" % (info, page_prve)))
    
    buttons_back = []
    buttons_back.append(Button.inline(text="返回", data="back"))
    
    if len(buttons_row) > 0:
        buttons.append(buttons_row)
        buttons.append(buttons_row1)
        buttons.append(buttons_back)
    
    if len(buttons) > 0:
        return buttons
    else:
        return None
    
    