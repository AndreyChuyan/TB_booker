﻿import telebot
from telebot import types

from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI
import socks
import socket

# Настройки прокси
# Настройки прокси
# telebot.apihelper.proxy = {'https': 'socks5://ifk:3f0gns1AZ@158.160.59.184:3128'}

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "socks5://ifk:3f0gns1AZ@158.160.59.184", 3128)
socket.socket = socks.socksocket

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN_TELEGRAM)


client = OpenAI(
    api_key=TOKEN_OPENAI
)



# bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode=None)


@bot.message_handler(commands=['start', 'help', 'asd'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def answer_all(message):
    print(message.from_user)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    result = completion.choices[0].message.content
    bot.reply_to(message, result)


if __name__ == "__main__":
    bot.polling()