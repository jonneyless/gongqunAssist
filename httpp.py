import requests
import json

headers_tg = {
    "Content-Type": "application/json",
}


async def getFakuan(num, created_at_jinbian):
    bot_url = "http://dbyy.admin.com:8680/api/fakuan"
    
    headers = headers_tg
    
    data = {
        "key": "yy99",
        "num": num,
        "created_at_jinbian": created_at_jinbian,
    }
    
    money = 0
    num = 0
    
    response = requests.post(bot_url, json=data, headers=headers, timeout=10)
    if response is not None:
        response_text = json.loads(response.text)
        
        if "message" in response_text and response_text["message"] == "success":
            money = response_text["data"]["money"]
            num = response_text["data"]["num"]
            
    return money, num
    

def handle_jiufen(response):
    num = 0
    num_in = 0
    # 1 => '受理中',
    # 2 => '公审中',
    # 3 => '处理中',
    # 4 => '已结案',
    
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num9 = 0
    # 1 => '和解',
    # 2 => '公审',
    # 3 => '仲裁',
    # 4 => '赔付',
    # 9 => '待定',
    
    if response is not None:
        response_text = json.loads(response.text)
        
        if "message" in response_text and response_text["message"] == "success":
            data = response_text["data"]["data"]
            
            num = len(data)
            for item in data:
                status = int(item["status"])
                status_result = int(item["status_result"])
                
                if status != 4:
                    num_in = num_in + 1
                else:
                    if status_result == 1:
                        num1 = num1 + 1
                    elif status_result == 2:
                        num2 = num2 + 1
                    elif status_result == 3:
                        num3 = num3 + 1
                    elif status_result == 4:
                        num4 = num4 + 1
                    elif status_result == 9:
                        num9 = num9 + 1
    
    text = "纠纷 %s 次，处理中 %s 次\n" % (num, num_in)
    text += " 和解 %s 次\n" % num1
    text += " 公审 %s 次\n" % num2
    text += " 仲裁 %s 次\n" % num3
    text += " 赔付 %s 次\n" % num4
    # text += " 待定 %s 次\n" % num9
    
    return text
    

async def getJiufen(num, created_at_jinbian):
    bot_url = "http://assist.admin.com:8681/api/jiufen"
    
    headers = headers_tg
    
    data = {
        "key": "jf99",
        "num": num,
        "created_at_jinbian": created_at_jinbian,
    }
    
    response = requests.post(bot_url, json=data, headers=headers, timeout=10)

    return handle_jiufen(response)      

    
async def getJiufenByUsername(username):
    bot_url = "http://assist.admin.com:8681/api/jiufenByUsername"
    
    headers = headers_tg
    
    data = {
        "key": "jf99",
        "username": username,
    }
    
    response = requests.post(bot_url, json=data, headers=headers, timeout=10)
    
    return handle_jiufen(response)   
    
    
async def getJzJiaoyi(user_tg_id):
    bot_url = "http://jz.admin.com:8680/api/getJiaoyi"
    
    headers = headers_tg
    
    data = {
        "key": "huionedb",
        "user_tg_id": user_tg_id,
    }
    
    data1 = []
    response = requests.post(bot_url, json=data, headers=headers, timeout=10)
    if response is not None:
        response_text = json.loads(response.text)
        
        if "message" in response_text and response_text["message"] == "success":
            data1 = response_text["data"]
            
    return data1
    