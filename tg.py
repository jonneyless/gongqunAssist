import time

import requests
from retrying import retry

from assist import get_current_timestamp
from config import bot_qunguan_url, chat_photo_path
import json
import helpp

headers_tg = {
    "Content-Type": "application/json",
}

description_arr = [
    "Forbidden: bot was blocked by the user",
    "Forbidden: bot was kicked from the group chat",
    "Forbidden: bot was kicked from the supergroup chat",
    "Bad Request: not enough rights to send text messages to the chat",
    "Bad Request: message to delete not found",
    "Bad Request: chat not found",
    "Bad Request: group chat was upgraded to a supergroup chat",

    "Bad Request: USER_ALREADY_PARTICIPANT"
]

declineChatJoinRequest_description_arr = [
    "Bad Request: HIDE_REQUESTER_MISSING",
    "Forbidden: user is deactivated",
    "Bad Request: USER_ID_INVALID",
    "Forbidden: bot was kicked from the supergroup chat",
    "Bad Request: chat not found"
]


async def revokeChatInviteLink(group_tg_id, link):
    bot_url = helpp.get_bot_url(group_tg_id, 3)
    
    tg_url = bot_url + "revokeChatInviteLink"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "invite_link": link,
    }
    
    current_timestamp = get_current_timestamp()
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=10)

    flag = False
    if response is not None:
        response_text = json.loads(response.text)
        
        print("revoke %s %s" % (group_tg_id, response_text))
        
        if ("result" in response_text) and response_text["result"]:
            flag = True
    
    if not flag:
        tg_url = bot_qunguan_url
        
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "chat_id": group_tg_id,
            "invite_link": link,
        }
        
        current_timestamp = get_current_timestamp()
        
        response = requests.post(tg_url, json=data, headers=headers, timeout=10)
    
        flag = False
        if response is not None:
            response_text = json.loads(response.text)
            
            print(response_text)
            
            if ("result" in response_text) and response_text["result"]:
                flag = True
                
    return flag


async def createBotApproveLink(group_tg_id, typee):
# 1、123群审核链接 （永久审核链接）
# 2、123群单个链接（一天1个人链接） 
# 3、123群导航链接（7天前公开链接，7天后自动改审核链接）
# 4、123群广告链接（7天后失效）
# 5、123群月广告链接（30天后失效）
# 6、123注销链接（注销导航链接）
# 7、123群广告审核链接（审核链接7天后失效）
# 8、123群月广告审核链接（审核链接30天后失效）
        
    bot_url = helpp.get_bot_url(group_tg_id, 3)    
    
    tg_url = bot_url + "createChatInviteLink"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
    }
    
    current_timestamp = get_current_timestamp()
    forever_date = current_timestamp + 86400 * 3650
    
    if typee == 1:
        data["name"] = "永久审核链接"
        data["creates_join_request"] = True
        data["expire_date"] = forever_date
    elif typee == 2:
        data["name"] = "单个链接"
        data["creates_join_request"] = False
        data["expire_date"] = current_timestamp + 86400
        data["member_limit"] = 1
    elif typee == 3:
        data["name"] = "导航链接"
        data["expire_date"] = forever_date
    elif typee == 4:
        data["name"] = "广告链接"
        data["expire_date"] = current_timestamp + 86400 * 7
    elif typee == 5:
        data["name"] = "月广告链接"
        data["expire_date"] = current_timestamp + 86400 * 30
    elif typee == 7:
        data["name"] = "群广告审核链接"
        data["creates_join_request"] = True
        data["expire_date"] = current_timestamp + 86400 * 7
    elif typee == 8:
        data["name"] = "群月广告审核链接"
        data["creates_join_request"] = True
        data["expire_date"] = current_timestamp + 86400 * 30
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=30)

    link = None
    creator_tg_id = ""
    creator_fullname = ""
    creator_firstname = ""
    creator_lastname = ""
    if response is not None:
        response_text = json.loads(response.text)
        
        print("create %s %s" % (group_tg_id, response_text))
        
        if ("result" in response_text) and response_text["result"]:
            link = response_text["result"]["invite_link"]
            
            if "creator" in response_text["result"]:
                creator = response_text["result"]["creator"]
                if "id" in creator:
                    creator_tg_id = creator["id"]
                if "first_name" in creator:
                    creator_firstname = creator["first_name"]
                if "last_name" in creator:
                    creator_lastname = creator["last_name"]
                
                creator_fullname = creator_firstname + creator_lastname
                
        
    return link, creator_tg_id, creator_fullname




def setChatTitle(bot_url, chat_id, title):
    tg_url = bot_url + "setChatTitle"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "title": title,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatTitle Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def setChatDescription(bot_url, chat_id, description):
    tg_url = bot_url + "setChatDescription"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "description": description,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatDescription Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def deleteChatPhoto(bot_url, chat_id):
    tg_url = bot_url + "deleteChatPhoto"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("deleteChatPhoto Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag

def setChatPhotoRequestRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("setChatPhotoRequestRetry: %s" % description)
        return True
    else:
        return False


@retry(stop_max_attempt_number=3, retry_on_result=setChatPhotoRequestRetry)
def setChatPhotoRequest(bot_url, chat_id):
    tg_url = bot_url + "setChatPhoto"

    data = {
        "chat_id": chat_id,
    }

    response = None
    try:
        response = requests.post(tg_url, data=data, files={"photo": open(chat_photo_path, 'rb')}, timeout=15)
    except Exception as e:
        print("setChatPhotoRequest Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 失败，不需要重试
    # flag = True 成功，不需要重试
    # flag = None 失败，需要重试：tg异常，tg限制

    if response is not None:
        print(response.text)
        response_text = json.loads(response.text)
        # print(response_text)
        print("setChatPhotoRequest %s %s" % (chat_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("setChatPhotoRequest sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


def sendMessage(bot_url, chat_id, text):
    tg_url = bot_url + "sendMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": True,
        "link_preview_options": {
            "is_disabled": True
        }
    }

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendMessageOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def pinChatMessage(bot_url, chat_id, message_id):
    tg_url = bot_url + "pinChatMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("pinChatMessage Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag

