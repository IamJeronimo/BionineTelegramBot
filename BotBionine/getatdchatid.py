"""
Autor: Lucas Jeronimo da Silva
E-mail: l.jeronimo@outlook.com.br
Manutenção: Lucas Jeronimo da Silva - 2023-10-22

#################################### OBJETIVO ###########################################################
- Capturar o chatid do atendente.

#################################### DOCs ###########################################################
PyTelegramBotAPI:
- https://pytba.readthedocs.io/en/latest/index.html
- https://pypi.org/project/pyTelegramBotAPI/

"""


import os
import telebot
from dotenv import load_dotenv

load_dotenv()
apiKey = os.environ.get("API_KEY")
chatBot = telebot.TeleBot(apiKey)

chat_ids = set() 

@chatBot.message_handler(commands=['getmychatidtoregister'])
def getchatId(message):
    chat_id = message.chat.id
    if chat_id not in chat_ids:
        chat_ids.add(chat_id)
        chatBot.reply_to(message, f"Seu ID de chat ({chat_id}) foi registrado.")
    else:
        chatBot.reply_to(message, "Seu ID de chat já está registrado.")

@chatBot.message_handler(commands=['removechatid'])
def removechatId(message):
    chat_id = message.chat.id
    if chat_id in chat_ids:
        chat_ids.remove(chat_id)
        chatBot.reply_to(message, f"Seu ID de chat ({chat_id}) foi removido.")
    else:
        chatBot.reply_to(message, "Seu ID de chat não estava registrado.")

chatBot.polling()