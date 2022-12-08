import telebot
from telebot import types
import db_client, users_db
from keyboard import first_keyboard, delete_keyboard, select_dish, select_del_cat_dish, key_del_dish


telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot('')


@bot.middleware_handler()
def middleware_handler(bot_instance, package):
    if package.message != None:
        user_id = package.message.from_user.id
        message = package.message.text
        con = db_client.Connect()
        con.log(user_id=user_id, button=message)
    else:
        user_id = package.callback_query.from_user.id
        callback_data = package.callback_query.data
        match callback_data.split('*')[0]:
            case 'cat':
                try:
                    con = db_client.Connect()
                    cat_name = con.select_cat_name(button=int(package.callback_query.data.split('*')[1]))[0][0]
                    con.log(button=cat_name, user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод категории')
                    print(error)

            case 'item':
                try:
                    con =db_client.Connect()
                    info_name = con.select_info_name(button=int(package.callback_query.data.split('*')[1]))[0][0]
                    con.log(button=info_name, user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод информации о блюде')
                    print(error)

            case 'back':
                try:
                    con = db_client.Connect()
                    con.log(button=package.callback_query.data.split('*')[0], user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод информации о блюде')
                    print(error)

            case 'menu':
                try:
                    con = db_client.Connect()
                    con.log(button=package.callback_query.data, user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод информации о блюде')
                    print(error)

            case 's_del_dish':
                try:
                    con = db_client.Connect()
                    con.log(button=package.callback_query.data.split('*')[1], user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод информации о блюде')
                    print(error)

            case 'del_dish':
                try:
                    con = db_client.Connect()
                    con.log(button=package.callback_query.data.split('*')[1], user_id=user_id)
                except Exception as error:
                    bot.send_message(package.chat_id, text='Не верный ввод информации о блюде')
                    print(error)



#Команда START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.full_name}', reply_markup=first_keyboard())
    try:
        con = users_db.Users()
        user_id = message.from_user.id
        user_name = message.from_user.username
        add_user = con.user_register(user_id=user_id, user_name=user_name)
    except:
        pass


#Выбор категории
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='cat' else False)
def first_menu(call:types.CallbackQuery):
    user_id = call.from_user.id
    try:
        con = db_client.Connect()
        button_list = con.second_button(button=int(call.data.split('*')[1]), user_id=user_id)
        all_buttons = types.InlineKeyboardMarkup()
        for cat in button_list:
            all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'item*{cat[0]}'))
        all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
        bot.send_message(call.from_user.id, 'our menu:', reply_markup=all_buttons)
        bot.answer_callback_query(call.id)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Товар в выбранной категории
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='item' else False)
def second_menu(call:types.CallbackQuery):
    user_id = call.from_user.id
    print(call.data)
    try:
        con = db_client.Connect()
        item = con.info(item_id=int((call.data.split('*')[1])), user_id=user_id)
        print(item)
        print(call.data)
        all_buttons = types.InlineKeyboardMarkup()
        all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
        all_buttons.add(types.InlineKeyboardButton('back', callback_data=f'back*{item[0][3]}'))
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Блюдо: {item[0][0]} \nЦена: {item[0][2]} Byn \nВес: {item[0][1]} грамм',
            reply_markup=all_buttons
            )
        bot.answer_callback_query(call.id)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Кнопка BACK
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='back' else False)
def back(call:types.CallbackQuery):
    user_id = call.from_user.id
    try:
        con = db_client.Connect()
        button_list = con.second_button(button=int(call.data.split('*')[1]), user_id=user_id)
        all_buttons = types.InlineKeyboardMarkup()
        for cat in button_list:
            all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'item*{cat[0]}'))
        all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
        bot.send_message(call.from_user.id, 'our menu:', reply_markup=all_buttons)
        bot.answer_callback_query(call.id)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Кнопака MENU
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='menu' else False)
def home(call:types.CallbackQuery):
    try:
        bot.send_message(call.from_user.id, f'Привет {call.from_user.full_name}', reply_markup=first_keyboard())
        bot.answer_callback_query(call.id)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Добавление новой категории
@bot.message_handler(commands=['new_cat'])
def add_new_cat(message):
    try:
        bot.send_message(message.chat.id, 'Введите название новой категории блюд. Для отмени напишите back')
        bot.register_next_step_handler(message, add)
    except Exception as error:
        bot.send_message(message.chat.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Приём текста + добавления данных в БД
def add(message):
    try:
        if not message.text.lower() == 'back':
            cat = message.text
            con = db_client.Connect()
            add_cat = con.add_main_menu(new_cat=cat)
            bot.send_message(message.chat.id, f'Добавлена новая категория:  {message.text}', reply_markup=first_keyboard())
        else:
            bot.send_message(message.chat.id, f'Возврат в меню', reply_markup=first_keyboard())
    except Exception as error:
        bot.send_message(message.chat.id, f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Удаление категории
@bot.message_handler(commands=['delete_cat'])
def delete_cat(call):
    try:
        bot.send_message(call.from_user.id, 'Выберите категорию для удаления. Для отмены напишите back', reply_markup=delete_keyboard())
        bot.register_next_step_handler(call, next_delete)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Обработка нажания на кнопку удаления
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='del' else False)
def next_delete(call:types.CallbackQuery):
    try:
        if not call.data.lower() == 'back':
            del_cat = call.data.split('*')[1]
            con = db_client.Connect()
            l_del_cat = con.delete_main_menu(delete_cat=del_cat)
            bot.send_message(call.from_user.id, text=f'Вы удалили категорию: "{del_cat}"', reply_markup=first_keyboard())
        else:
            bot.send_message(call.from_user.id, text=f'Возврат в меню', reply_markup=first_keyboard())
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Обработка команты "new_dish"
@bot.message_handler(commands=['new_dish'])
def dish_select_cat(call):
    try:
        bot.send_message(call.from_user.id, 'Выберите категорию. Для отмени напишите back', reply_markup=select_dish())
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Выбор категории для нового блюда
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='new_dish' else False)
def new_dish(call:types.CallbackQuery):
    try:
        if not call.data.lower() == 'back':
            dish = call.data.split('*')[1]
            bot.send_message(call.from_user.id, text=f'Вы выбрали категорию: "{dish}". Введите название нового блюда, цену и вес через запятую:')
        else:
            bot.send_message(call.from_user.id, text=f'Возврат в меню', reply_markup=first_keyboard())
        bot.register_next_step_handler(call.message, add_new_dish,dish)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Добавление новой подкатегории категории
def add_new_dish(message, dish):
    try:
        if not message.text.lower() == 'back':
            dish_name = message.text.split(',')[0]
            price = message.text.split(',')[1]
            weight = message.text.split(',')[2]
            con = db_client.Connect()
            add_dish = con.new_dish(dish=dish_name, price=price, weight=weight, cat_id=dish)
            bot.send_message(message.chat.id, f'Добавлено новое блюдо:  {message.text}', reply_markup=first_keyboard())
        else:
            bot.send_message(message.chat.id, f'Возврат в меню', reply_markup=first_keyboard())
    except Exception as error:
        bot.send_message(message.chat.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)



#Приём текста + добавления данных в БД
def add_dish(message):
    try:
        if not message.text.lower() == 'back':
            cat = message.text
            con = db_client.Connect()
            add_cat = con.add_main_menu(new_cat=cat)
            bot.send_message(message.chat.id, f'Добавлена новая категория:  {message.text}', reply_markup=first_keyboard())
        else:
            bot.send_message(message.chat.id, f'Возврат в меню', reply_markup=first_keyboard())
    except Exception as error:
        bot.send_message(message.chat.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Обработчик команды уладения блюда
@bot.message_handler(commands=['delete_dish'])
def dish_select_cat(call):
    try:
        bot.send_message(call.from_user.id, 'Выберите категорию. Для отмени напишите back', reply_markup=select_del_cat_dish())
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#выбор категории для удаления блюда
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='s_del_dish' else False)
def s_del_dish(call:types.CallbackQuery):
    user_id = call.from_user.id
    try:
        con = db_client.Connect()
        button_list = con.del_second_button(button_name=call.data.split('*')[1], user_id=user_id)
        all_buttons = types.InlineKeyboardMarkup()
        for cat in button_list:
            all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'del_dish*{cat[1]}'))
        all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
        bot.send_message(call.from_user.id, 'Выберите блюдо для удаления:', reply_markup=all_buttons)
        bot.answer_callback_query(call.id)
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Удаление блюда
@bot.callback_query_handler(lambda call: True if call.data.split('*')[0]=='del_dish' else False)
def del_dish(call:types.CallbackQuery):
    try:
        if not call.data.lower() == 'back':
            del_dish = call.data.split('*')[1]
            con = db_client.Connect()
            # dish_name = con.dish_name(dish_id=del_dish)
            l_del_dish = con.delete_menu(delete_dish=del_dish)
            print(del_dish)
            bot.send_message(call.from_user.id, text=f'Вы удалили блюдо: "{del_dish}"', reply_markup=first_keyboard())
        else:
            bot.send_message(call.from_user.id, text=f'Возврат в меню', reply_markup=first_keyboard())
    except Exception as error:
        bot.send_message(call.from_user.id, text=f'Произошла ошибка. Попробуйте ещё раз!')
        print(error)


#Топ нажатых кнопок
@bot.message_handler(commands=['admin_buttons'])
def admin_buttons_top(message):
    con = users_db.Users()
    top_buttons = con.buttons_top()
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Топ нажатых кнопок за неделю: \n'
             f'🥇   {top_buttons[0][0]}\n                      Нажатий: {top_buttons[0][1]}\n'
             f'🥈   {top_buttons[1][0]}\n                      Нажатий: {top_buttons[1][1]}\n'
             f'🥉   {top_buttons[2][0]}\n                      Нажатий: {top_buttons[2][1]}\n'
             f'4   {top_buttons[3][0]}\n                       Нажатий: {top_buttons[3][1]}\n'
             f'5   {top_buttons[4][0]}\n                       Нажатий: {top_buttons[4][1]}\n',
        reply_markup=all_buttons
    )

#Топ активных пользователей
@bot.message_handler(commands=['admin_users'])
def admin_users_top(message):
    con = users_db.Users()
    top_users = con.users_top()
    user_1 = con.users_name_top(user_id=top_users[0][0])
    user_2 = con.users_name_top(user_id=top_users[1][0])
    user_3 = con.users_name_top(user_id=top_users[2][0])
    all_buttons = types.InlineKeyboardMarkup()
    all_buttons.add(types.InlineKeyboardButton('menu', callback_data=f'menu'))
    bot.send_message(
        chat_id=message.chat.id,
        text=f'🥇   {user_1[0]}    Нажатий: {top_users[0][1]}\n'
             f'🥈   {user_2[0]}    Нажатий: {top_users[1][1]}\n'
             f'🥉   {user_3[0]}    Нажатий: {top_users[2][1]}\n',
        reply_markup=all_buttons
    )


bot.polling(non_stop=True, interval=0)