from queue import Empty
from telebot import types
import os
import telebot
# from dotenv import load_dotenv
from backButtonMarkup import backButtonMarkup


# load_dotenv()


token = os.environ['TOKEN']
channel_id = os.environ['CHANNEL_ID']
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    Markup = types.ReplyKeyboardMarkup(row_width=2)
    Markup.add(types.KeyboardButton('Прислать имена репрессированных'),
               types.KeyboardButton('Прислать фото и видео'))
    bot.send_message(
        message.chat.id, "Присылайте имена ваших родственников, пострадавших в годы репрессий, чтобы мы могли вместе помолиться о них. Также вы можете присылать фото и видео с чтения имён в вашем городе.", reply_markup=Markup)


# Обработчик выбора, который был сделан в start. Функция принимает либо текстовые сообщеие либо фото
@bot.message_handler(content_types=['text', 'photo'])
def main(message):
    if message.text == 'Прислать имена репрессированных':
        sendNames(message)

    if message.text == 'Прислать фото и видео':
        sendMedia(message)


def sendNames(message):
    mesg = bot.send_message(
        message.chat.id, 'Присылайте имена ваших родственников, пострадавших в годы репрессий, чтобы мы могли вместе помолиться о них', reply_markup=backButtonMarkup)

    def handler(message):
        if message.text == '🔙 Назад':
            message.text = None
            start(message)
        else:
            if message.text != None:
                postToChannel(message, "NAMES")
    bot.register_next_step_handler(mesg, handler)


def sendMedia(message):
    mesg = bot.send_message(
        message.chat.id, 'Загрузите фото и видео с чтения имён в вашем городе. Пожалуйста, отправляйте фото ПО ОДНОМУ', reply_markup=backButtonMarkup)

    def handler(message):
        if message.text == '🔙 Назад':
            message.text = None
            start(message)
        else:
            postToChannel(message, "MEDIA")
    bot.register_next_step_handler(mesg, handler)

def postToChannel(message, type):
    def handler(message):
        if message.text == 'Начать сначала' or message.text == '/start':
            message.text = None
            start(message)
        else:
            postToChannel(message, type)

    Markup = types.ReplyKeyboardMarkup(row_width=True)
    Markup.add(types.KeyboardButton('Начать сначала'))

    mesg = None

    bot.forward_message(channel_id, message.chat.id, message.message_id)

    if type == "NAMES":
        mesg = bot.send_message(
            message.chat.id, '✅ Спасибо! Ваша заявка принята.', reply_markup=Markup)
    elif type == "MEDIA":
        mesg = bot.send_message(
            message.chat.id, '✅ Спасибо! Лучшие фото мы публикуем на канале @molitvapamyaty и в социальных сетях акции.', reply_markup=Markup)

    bot.register_next_step_handler(mesg, handler)


if __name__ == '__main__':
    bot.polling()
