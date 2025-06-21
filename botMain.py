import telebot
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

import botUtils

telegram_bot_token = ''
bot = telebot.TeleBot(telegram_bot_token)

def create_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = KeyboardButton('🐷Хрю')
    item2 = KeyboardButton('Помощь')
    markup.add(item1, item2)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я отправляю глупые фото со свиньями и придумываю для них подпись.",
                     reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == 'хрю')
def send_photo(message):
    try:
        rand_txt = botUtils.get_random_wisdom( )
        rand_img = botUtils.get_random_image( )
        bot.send_photo(message.chat.id, botUtils.add_text_to_img(rand_txt, rand_img))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при отправке фото: {str(e)}", reply_markup=create_menu())

@bot.message_handler(func=lambda message: message.text.lower() == 'помощь')
def send_help(message):
    bot.send_message(message.chat.id,
                    "Доступные команды:\n"
                    "Отправь фото свиньи",
                    reply_markup=create_menu())

@bot.message_handler(content_types=["text"])
def echo(message):
    if bot.get_me().username.lower() in message.text.lower():
        bot.reply_to(message, "Хрю! Привет!", reply_markup=create_menu())
    else:
        bot.send_message(message.chat.id, message.text, reply_markup=create_menu())

if __name__ == '__main__':
    bot.polling(none_stop=True)