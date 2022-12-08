import psycopg2

DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = ''
HOST = 'localhost'
PORT = '8000'


class Users:
    def __init__(self):
        self.db = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cur = self.db.cursor()

    def user_register(self, user_id, user_name):
        self.cur.execute(f"INSERT INTO user_data (user_id, user_name) VALUES ({user_id}, '{user_name}')")
        self.db.commit()

    def buttons_top(self):
        self.cur.execute(f"SELECT button_name, COUNT(button_name) FROM buttons WHERE date_time > DATE(now() - interval '7 day') GROUP BY button_name ORDER BY count DESC LIMIT 5 ")
        return self.cur.fetchall()

    def users_top(self):
        self.cur.execute(f"SELECT user_id, COUNT(user_id) FROM buttons GROUP BY user_id ORDER BY count DESC LIMIT 3")
        return self.cur.fetchall()

    def users_name_top(self, user_id):
        self.cur.execute(f"SELECT user_name FROM user_data WHERE user_id = {user_id}")
        return self.cur.fetchone()



a = Users()

