import psycopg2


DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = ''
HOST = 'localhost'
PORT = '8000'


class Connect:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def select_all(self):
        self.cur.execute("SELECT * FROM menu WHERE menu.cat_id = cat_id")
        return self.cur.fetchall()

    #Берём из БД все категории блюд
    def button_list(self):
        self.cur.execute("SELECT * FROM main_menu")
        return self.cur.fetchall()


    #Берём из БД названия блюд определенной категории (по ID) и логируем кнопку
    def second_button(self, button, user_id):
        self.cur.execute(f"SELECT menu_cat FROM main_menu WHERE id = {button}")
        button_name = self.cur.fetchone()
        self.cur.execute(f"INSERT INTO buttons (user_id, button_name) VALUES ({user_id},'{button_name[0]}')")
        self.db.commit()
        self.cur.execute(f"SELECT id, dish FROM menu WHERE cat_id = {button}")
        return self.cur.fetchall()


    #Берём из БД названия блюд определенной категории (По нахванию) и логируем кнопку
    def del_second_button(self, button_name, user_id):
        self.cur.execute(f"SELECT * FROM main_menu WHERE menu_cat = '{button_name}'")
        button = self.cur.fetchall()
        self.cur.execute(f"INSERT INTO buttons (user_id, button_name) VALUES ({user_id},'{button_name[0]}')")
        self.db.commit()
        self.cur.execute(f"SELECT id, dish FROM menu WHERE cat_id = {button[0][0]}")
        return self.cur.fetchall()

    #Получаем название блюда по ID
    def dish_name(self, dish_id):
        self.cur.execute(f"SELECT dish FROM menu WHERE id = {dish_id}")
        return self.cur.fetchone()

    #Берёт иб БД информацию о выбраном блюде
    def info(self, item_id, user_id):
        self.cur.execute(f"SELECT dish FROM menu WHERE id = {item_id}")
        button_name = self.cur.fetchone()
        self.cur.execute(f"INSERT INTO buttons (user_id, button_name) VALUES ({user_id},'{button_name[0]}')")
        self.db.commit()
        self.cur.execute(f"SELECT  dish, weight, price, cat_id FROM menu WHERE id = {item_id}")
        return self.cur.fetchall()

    #Добавляем в БД новые категории блюд
    def add_main_menu(self, new_cat):
        self.cur.execute(f"INSERT INTO main_menu (menu_cat) VALUES ('{new_cat}')")
        self.db.commit()

    #Удаляем категорию из меню
    def delete_main_menu(self, delete_cat):
        self.cur.execute(f"DELETE FROM main_menu WHERE menu_cat = '{delete_cat}'")
        self.db.commit()

    #Удаление блюда
    def delete_menu(self, delete_dish):
        self.cur.execute(f"DELETE FROM menu WHERE dish='{delete_dish}'")
        self.db.commit()

    #Добавляем блюдо в меню
    def new_dish(self, dish, price, weight, cat_id):
        self.cur.execute(f"SELECT id FROM main_menu WHERE menu_cat = '{cat_id}'")
        id = self.cur.fetchone()
        self.cur.execute(f"INSERT INTO menu (dish, price, weight, cat_id) VALUES ('{dish}',{price},{weight},{id[0]})")
        self.db.commit()

    #Удаление блюда из меню
    def del_dish(self, dish, user_id):
        self.cur.execute(f"DELETE FROM menu WHERE dish='{dish}'")
        self.db.commit()

    #Логинование сообщений + чистка станых сообщений после 1000-го
    def log(self, button, user_id):
        self.cur.execute(f"SELECT * FROM logs LIMIT 1")
        min = self.cur.fetchone()
        self.cur.execute(f"SELECT * FROM logs ORDER BY date_time DESC LIMIT 1 ")
        max = self.cur.fetchone()
        if max[0] - min[0] == 999:
            self.cur.execute(f"DELETE FROM logs WHERE id={min[0]}")
            self.db.commit()
        self.cur.execute(f"INSERT INTO logs (user_id, buttons) VALUES ({user_id}, '{button}')")
        self.db.commit()

    #Получение названия кнопки категорий
    def select_cat_name(self, button):
        self.cur.execute(f"SELECT menu_cat FROM main_menu WHERE id = {button}")
        return self.cur.fetchall()

    #Полечение названия кнопки подкатегории
    def select_info_name(self, button):
        self.cur.execute(f"SELECT dish FROM menu WHERE id = {button}")
        return self.cur.fetchall()


