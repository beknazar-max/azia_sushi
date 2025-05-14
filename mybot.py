import  telebot
import  webbrowser
from  telebot import types
import sqlite3

bot = telebot.TeleBot('7921062562:AAHKSNitjKxaRdcGv5EDAHEzLCCOdZB_R_g')

name = None

@bot.message_handler(commands=['start'])
def start(massage):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('прейти на сайт  😊')
    markup.row(btn1)
    btn2 = types.KeyboardButton('удалить фото')
    btn3 = types.KeyboardButton('изменить')
    markup.row(btn2, btn3)
    file = open('./photo.jpg', 'rb')
    bot.send_photo(massage.chat.id, file, reply_markup=markup)
    # bot.send_message(massage.chat.id, 'привет', reply_markup=markup)
    bot.register_next_step_handler(massage, on_click)


def on_click(massage):
    if massage.text == 'прейти на сайт':
        bot.send_message(massage.chat.id, 'website is open')
    elif massage.text == 'удалить фото':
        bot.send_message(massage.chat.id, 'delate')


@bot.message_handler(content_types=['photo'])
def get_photo(massage):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('прейти на сайт 😊', url='https://www.asiasushi.kg/#suhi')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('удалить фото', callback_data='delate')
    btn3 = types.InlineKeyboardButton('изменить', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(massage, 'какое красивое фото', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_massage(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['site', 'website'])
def site(massage):
    webbrowser.open('https://www.asiasushi.kg/#suhi')



@bot.message_handler(commands=['hello', 'main'])
def main(massage):
    bot.send_message(massage.chat.id, f'привет {massage.from_user.first_name}')

@bot.message_handler()
def info(massage):
    if massage.text.lower() == 'привет':
        bot.send_message(massage.chat.id, f'привет {massage.from_user.first_name}')
    elif massage.text.lower() == 'id':
        bot.reply_to(massage, f'ID: {massage.from_user.id}')

@bot.message_handler(commands=['help'])
def main(massage):
    bot.send_message(massage.chat.id, '<b>что</b> <em><u>увас случилось</u></em>', parse_mode='html')
#
# @bot.message_handler(commands=['start'])
# def start(massage):
#     conn = sqlite3.connect('itproger.sql')
#     cur = conn.cursor()
#
#     cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(8))')
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     bot.send_message(massage.chat.id, 'Приветб сейчас тебя зарегистрируем! Введите ваше имя')
#     bot.register_next_step_handler(massage, user_name)
#
# def user_name(massage):
#     global name
#     name = massage.text.strip()
#     bot.send_message(massage.chat.id, 'Введите пароль')
#     bot.register_next_step_handler(massage, user_pass)

# def user_pass(message):
#     password = message.text.strip()
#     conn = sqlite3.connect('itproger.sql')
#     cur = conn.cursor()
#
#     cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton('сприсок пользователей', callback_data='users'))
#     bot.send_message(message.chat.id, 'Ползеватель зарегистрирован', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('itproger.sql')
#     cur = conn.cursor()
#
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     info = ''
#     for el in users:
#         info += f'Имя: {el[1]}, пароль: {el[2]}\n'
#
#     cur.close()
#     conn.close()
#
#     bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)