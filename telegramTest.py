# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="8013412356:AAFHOWSwpWURns-riiMgFDRDQW0z5-_Ja4g")
chat_id = "7743827290"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="파이썬 텔레그램 테스트2!"))