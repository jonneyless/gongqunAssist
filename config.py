from environs import Env

env = Env()
env.read_env()

mysqlInfo = {
    "host": env.str("DB_HOST", "3.1.50.237"),
    "db": env.str("DB_DATABASE", "welcome"),
    "user": env.str("DB_USER", "sync"),
    "passwd": env.str("DB_PASS", "pcKyxHZzHcz35D33"),
    "port": env.int("DB_PORT", 3306),
}

redisInfo = {
    "host": env.str("REDIS_HOST", "127.0.0.1"),
    "port": env.int("REDIS_PORT", 6379),
}

bot_token = env.str('BOT_TOKEN', "5995027011:AAFbO4lMOnv-AYbDYT2NTtLFJ79FkcON5jE")
bot_id = env.int('BOT_ID', 5995027011)

app_id = 22330058
app_hash = "c8c2f318a089aff99b7949d1092bfec2"


bot_url = "https://api.telegram.org/bot"+env.str("QG_BOT_TOKEN", "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")+"/"
bot_qunguan_url = "https://api.telegram.org/bot"+env.str("QG_BACK_BOT_TOKEN", "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")+"/"

chat_photo_path = env.str("CHAT_PHOTO_PATH", "chat_photo.jpg")