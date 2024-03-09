import telebot

from telebot import types

bot = telebot.TeleBot('7009147970:AAGa3BHfR1H5WztUh2UI1CMGo09pToFi7Fk')

channel = ''
text = 'a'
textBtn = ''
pathPhoto = ''

linkBtn = False
linksBtn = ''
@bot.message_handler(commands=['start','help'])
def Start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton(text="📝Создание поста"))
    markup.add(types.KeyboardButton(text='➕Добавление бота в канал'))
    markup.add(types.KeyboardButton(text='🗣️Тех.поддержка'))
    bot.send_message(message.chat.id,'''Привет 👋 
Этот бот разработан для выкладывания рекламы в твой телеграмм канал/чат этот бот являеться первым из серии ботов для "Каналов" которые я разрабатываю 
Удачи в использовании🫰''',reply_markup=markup)
    bot.register_next_step_handler(message,Handler)

@bot.message_handler(content_types=['photo','gif'])
def create1(message):
    global text,pathPhoto
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        pathPhoto = file_info.file_path
        with open(pathPhoto, 'wb') as new_file:
            new_file.write(downloaded_file)
            text = message.caption
        bot.send_message(message.chat.id,'Введи текст кнопки:')
        bot.register_next_step_handler(message,create2)
    except TypeError:
        bot.send_message(message.chat.id,'Пост должен содержать фотографию!')
        bot.register_next_step_handler(message,create1)

def create2(message):
    global textBtn
    textBtn = message.text
    bot.send_message(message.chat.id,'''Будет ли у кнопки какая либо ссылка? 🤔
Если ссылки не будет то тогда просто пиши "нет"😃''')
    bot.register_next_step_handler(message,create3)

def create3(message):
    global linksBtn

    linksBtn = message.text
    file = open(pathPhoto,'rb')

    markups = types.InlineKeyboardMarkup()
    if message.text == 'нет':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text=textBtn,callback_data='nofunc'))
        bot.send_photo(message.chat.id,file,caption=text,reply_markup=markup)
        linkBtn = False
    else:
        linkBtn = True
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text=textBtn,url=linksBtn,callback_data='a'))
        bot.send_photo(message.chat.id,file,caption=text,reply_markup=markup)
    markups.add(types.InlineKeyboardButton(text='Отправить✅',callback_data='send'))
    markups.add(types.InlineKeyboardButton(text='Отмена❌',callback_data='stop'))
    bot.send_message(message.chat.id,'''Пост готов✅✅, Внимательно проверь всё ли верно проверь ссылку ,текст и если всё готово выкладывай🥱''',reply_markup=markups)

def Handler(message):
    if message.text == '🗣️Тех.поддержка':
        bot.send_message(message.chat.id,'Случилась какая-то проблема? есть пожелание?хочешь себе своего бота?\nМожешь написать мне в личку там и решим все вопросы\n@nissangtiturbosprolus')
        bot.register_next_step_handler(message,Handler)
    elif message.text == '➕Добавление бота в канал':
        bot.send_message(message.chat.id,'''Что-бы добавить бота в канал нужно для начала его добавить в список админов и дать права на отправление сообщений🪪
Если пункт сверху выполнен то тогда отправляй ссылку на своего бота в формате @[Название бота] (бот отправит тестовое сообщение советуем приготовиться)🏃‍♀️''')
        bot.register_next_step_handler(message,add)
    elif message.text == 'Обратно в меню':
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(types.KeyboardButton(text="📝Создание поста"))
        markup.add(types.KeyboardButton(text='➕Добавление бота в канал'))
        markup.add(types.KeyboardButton(text='🗣️Тех.поддержка'))
        bot.send_message(message.chat.id,'Вы вернулись обратно в меню',reply_markup=markup)
        bot.register_next_step_handler(message,Handler)
    elif message.text == '📝Создание поста':
        bot.send_message(message.chat.id,'''🤔Введи текст сообщения 
‼️‼️Можешь отправить только 1 кратинку/gif‼️‼️''')
        bot.register_next_step_handler(message,create1)
    else:
        bot.send_message(message.chat.id,'Упс! видимо вы ошиблись попробуйте ввести другую команду❌')
        bot.register_next_step_handler(message,Handler)

def add(message):
    global channel
    try:
        channel = message.text
        print(channel)
        bot.send_message(chat_id = channel,text ='a')
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id,'''Ссылка не действительна❗ проверьте правильность написания, добавили ли вы бота и дали ли вы ему все права\nВведите проверенную ссылку или же обратитесь к тех.поддержке🧠
''')
        bot.register_next_step_handler(message,add)
    else:
        bot.send_message(message.chat.id,'Бот добавлен в канал теперь можно работать✅')
        bot.register_next_step_handler(message,Handler)

@bot.callback_query_handler(func = lambda call:True)
def han(call):
    global linkBtn,text,channel,textBtn,linksBtn
    file = open(pathPhoto,'rb')
    if call.data == 'send':
        markup = types.InlineKeyboardMarkup()
        if linkBtn == True:
            print('link '+linksBtn)
            markup.add(types.InlineKeyboardButton(text=textBtn,url=linksBtn,callback_data='nofunc'))
            bot.send_photo(chat_id = channel,caption=text,photo = file,reply_markup=markup)
            stop()
            bot.register_next_step_handler(call.message,Handler)
        else:
            markup.add(types.InlineKeyboardButton(text=textBtn,callback_data='nofunc'))
            bot.send_photo(chat_id = channel,caption=text,photo = file,reply_markup=markup)
            stop()
            bot.register_next_step_handler(call.message,Handler)
    if call.data == 'stop':
        bot.send_message(call.message.chat.id,'Вы отменили отправку поста❌')
        stop()
        bot.register_next_step_handler(call.message,Handler)

def stop():
    channel = ''
    text = 'a'
    textBtn = ''
    pathPhoto = ''
    linkBtn = False
    linksBtn = ''
bot.infinity_polling()