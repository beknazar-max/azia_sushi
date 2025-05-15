import telebot
from telebot import types

bot = telebot.TeleBot('7247659364:AAHF08I3xiLJBwPjGeuIZ08WRVHYPzxWr54')

photo = ['Мини Сет.jpg', 'Сет"Мари".jpg', 'Сет"Айлин".jpg', 'Сет"золото".jpg', 'Сет"Чисай".jpeg', 'Пицца"Маргарита".jpg']
drinks = ['Coca-Cola 1L.jpeg', 'компот.jpg', 'Coca-Cola 0.25L.jpeg', 'натуральный сок 1L.jpg']

photo_index = {}
drinks_index = {}
user_cart = {}

def remove_duplicates(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]

photo = remove_duplicates(photo)
drinks = remove_duplicates(drinks)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    photo_index[chat_id] = 0
    drinks_index[chat_id] = 0
    user_cart[chat_id] = []

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Перейти на сайт 😊')
    btn2 = types.KeyboardButton('Показать блюда🍜')
    btn3 = types.KeyboardButton('Показать напитки🧃')
    btn4 = types.KeyboardButton('Моя корзина')
    btn5 = types.KeyboardButton('Заказать')
    btn6 = types.KeyboardButton('Назад 🔙')
    markup.add(btn1, btn2,btn3)
    markup.add(btn4, btn5, btn6)

    bot.send_message(chat_id, 'Здравствуйте! Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if message.text == 'Перейти на сайт 😊':
        bot.send_message(chat_id, 'Нажмите чтобы перейти на сайт: https://www.asiasushi.kg/#suhi')

    elif message.text == 'Показать блюда🍜':
        send_photo(chat_id, 'photo')

    elif message.text == 'Показать напитки🧃':
        send_photo(chat_id, 'drinks')

    elif message.text == 'Моя корзина':
        cart_items = user_cart.get(chat_id, [])
        if cart_items:
            bot.send_message(chat_id, 'Ваши товары в корзине:\n' + '\n'.join(cart_items))
        else:
            bot.send_message(chat_id, 'Ваша корзина пуста.')

    elif message.text == 'Заказать':
        cart_items = user_cart.get(chat_id, [])
        if cart_items:
            bot.send_message(chat_id, 'Ваш заказ принят! Товары:\n' + '\n'.join(cart_items))
            user_cart[chat_id] = []
        else:
            bot.send_message(chat_id, 'Ваша корзина пуста. Добавьте товары, чтобы сделать заказ.')

    elif message.text == 'Назад 🔙':
        clear_messages(chat_id)
        start(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    chat_id = call.message.chat.id

    if call.data.startswith('add_'):
        _, category, index = call.data.split('_')
        index = int(index)
        if category == 'photo' and 0 <= index < len(photo):
            item = photo[index]
            user_cart[chat_id].append(item)
            bot.send_message(chat_id, f'Добавлено в корзину: {item}')
        elif category == 'drinks' and 0 <= index < len(drinks):
            item = drinks[index]
            user_cart[chat_id].append(item)
            bot.send_message(chat_id, f'Добавлено в корзину: {item}')

def send_photo(chat_id, category):
    if category == 'photo':
        index = photo_index.get(chat_id, 0)
        if index >= len(photo):
            photo_index[chat_id] = 0
            bot.send_message(chat_id, 'Блюд больше нет')
            return
        try:
            with open(photo[index], 'rb') as file:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Добавить в корзину', callback_data=f'add_photo_{index}')
                markup.add(btn1)
                bot.send_photo(chat_id, file, reply_markup=markup)
            photo_index[chat_id] += 1
        except FileNotFoundError:
                bot.send_message(chat_id, f'Файл {photo[index]} не найден.')
    elif category == 'drinks':
        index = drinks_index.get(chat_id, 0)
        if index >= len(drinks):
            drinks_index[chat_id] = 0
            bot.send_message(chat_id, 'Напитков больше нет')
            return
        try:
            with open(drinks[index], 'rb') as file:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Добавить в корзину', callback_data=f'add_drinks_{index}')
                markup.add(btn1)
                bot.send_photo(chat_id, file, reply_markup=markup)
            drinks_index[chat_id] += 1
        except FileNotFoundError:
            bot.send_message(chat_id, f'Файл {drinks[index]} не найден.')

def clear_messages(chat_id):

    bot.send_message(chat_id, "Возвращаемся к началу")

bot.polling(none_stop=True)