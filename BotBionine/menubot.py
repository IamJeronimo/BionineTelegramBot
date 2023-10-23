"""
Autor: Lucas Jeronimo da Silva
E-mail: l.jeronimo@outlook.com.br
Manutenção: Lucas Jeronimo da Silva - 2023-10-22

#################################### OBJETIVO ###########################################################
- Chatbot Telegram para iniciar um atendimento e encaminhar o contato ao atendente para finalizar.

#################################### DOCs ###########################################################
PyTelegramBotAPI:
- https://pytba.readthedocs.io/en/latest/index.html
- https://pypi.org/project/pyTelegramBotAPI/

"""
#!/usr/bin/env python3

import os
import telebot
from dotenv import load_dotenv

load_dotenv()

apiKey = os.environ.get("API_KEY")
atendenteChatid = os.environ.get("ATD_CHAT_ID")
chatBot = telebot.TeleBot(apiKey)

@chatBot.message_handler(commands=['start'])
def sendBemvindoFunc(message):
    chatBot.reply_to(message, "Olá " + message.from_user.first_name + "," +
 """ seja bem-vindo(a). Sou o Bionine Bot e irei lhe auxiliar, agende consultas e exames médicos com rapidez e facilidade.
                     
Clique em alguma opção para começarmos:
    /reclamacao  - Faça uma reclamação;
    /agendamento - Faça um agendamento de exames.""" )

@chatBot.message_handler(commands=['reclamacao'])
def reclamacaoFunc(message):
    chatBot.reply_to(message, message.from_user.first_name + ", para uma reclamação nos envie um e-mail para sacbionine@gmail.com e dentro de 3 dias úteis o(a) responderemos. Nós sentimos muito por isso.")

user_states = {}

@chatBot.message_handler(commands=['agendamento'])
def agendamentoFunc(message):
    chat_id = message.chat.id
    user_states[chat_id] = "aguardando_foto"
    chatBot.reply_to(message, "Para agendar um exame, envie uma foto frente e verso do seu RG ou documento oficial com foto (original):")

@chatBot.message_handler(content_types=['photo'])
def receivedphotoFunc(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == "aguardando_foto":
        user_states[chat_id] = "aguardando_confirmacao"
        chatBot.send_message(chat_id, "Conseguiu enviar a foto do documento? Responda com /sim ou /nao.")
    chatBot.forward_message(atendenteChatid, chat_id, message.message_id)

@chatBot.message_handler(commands=['sim', 'nao'])
def receivedconfirmationFunc(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == "aguardando_confirmacao":
        user_states[chat_id] = "aguardando_contato"
        if message.text == '/sim':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button = telebot.types.KeyboardButton("Compartilhar meu contato", request_contact=True)
            markup.add(button)
            chatBot.send_message(chat_id, "Clique no botão abaixo para compartilhar seu contato com o atendente:", reply_markup=markup)
        chatBot.forward_message(atendenteChatid, chat_id, message.message_id)

@chatBot.message_handler(content_types=['contact'])
def receivedcontactFunc(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == "aguardando_contato":
        chatBot.reply_to(message, "Contato compartilhado! Em breve o atendente entrará em contato.")
        chatBot.forward_message(atendenteChatid, chat_id, message.message_id)
    user_states.pop(chat_id, None) 
chatBot.polling()