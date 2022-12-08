from telebot import types
import db_client



#Клавиатура для выбора категории
def first_keyboard():
    con = db_client.Connect()
    button_list = con.button_list()
    all_buttons = types.InlineKeyboardMarkup()
    for cat in button_list:
        all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'cat*{cat[0]}'))
    return all_buttons


#Клавиатура для удаления категории
def delete_keyboard():
    con = db_client.Connect()
    button_list = con.button_list()
    all_buttons = types.InlineKeyboardMarkup()
    for cat in button_list:
        all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'del*{cat[1]}'))
    return all_buttons


#Клавиатура для добавления  категории
def select_dish():
    con = db_client.Connect()
    button_list = con.button_list()
    all_buttons = types.InlineKeyboardMarkup()
    for cat in button_list:
        all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'new_dish*{cat[1]}'))
    return all_buttons


#Клавиатура для выбора катерогии удаляемого блюда
def select_del_cat_dish():
    con = db_client.Connect()
    button_list = con.button_list()
    all_buttons = types.InlineKeyboardMarkup()
    for cat in button_list:
        all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f's_del_dish*{cat[1]}'))
    return all_buttons


#Клавиатура для выбора удаляемого блюда
def key_del_dish():
    con = db_client.Connect()
    button_list = con.button_list()
    all_buttons = types.InlineKeyboardMarkup()
    for cat in button_list:
        all_buttons.add(types.InlineKeyboardButton(cat[1], callback_data=f'del_dish*{cat[1]}'))
    return all_buttons
