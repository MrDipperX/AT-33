import psycopg2
from datetime import datetime


class PgConn:
    def __init__(self, host, dbname, user, port, password):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            print(error)

    def set_time(self):
        with self.conn:
            self.cur.execute("ALTER DATABASE d9ocvq1c3g3kb5 SET DATESTYLE TO PostgreSql,European;")
            self.conn.commit()
            self.cur.execute("SET TIME ZONE 'Asia/Tashkent'")
            self.conn.commit()

    def create_tables(self):
        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_tg BIGINT ,
                                username CHARACTER VARYING(100) ,
                                name CHARACTER VARYING(30),
                                date_reg TIMESTAMP WITHOUT TIME ZONE,
                                date_birth DATE,
                                phone_numb BIGINT,
                                dolj BOOLEAN DEFAULT False,
                                temp CHARACTER VARYING(50) DEFAULT 'no')""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS admins(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_tg BIGINT ,
                                username CHARACTER VARYING(100))
                                """)
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS ads(
                                id SERIAL PRIMARY KEY NOT NULL,
                                text TEXT,
                                photo_url CHARACTER VARYING(100))
                                """)
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS English(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Psychology(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Graj_zash(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS IIS(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                lab6 BOOLEAN DEFAULT False,
                                lab7 BOOLEAN DEFAULT False,
                                lab8 BOOLEAN DEFAULT False,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS KIS(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                lab6 BOOLEAN DEFAULT False,
                                lab7 BOOLEAN DEFAULT False,
                                lab8 BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False,
                                Kurs BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS WEB(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                lab6 BOOLEAN DEFAULT False,
                                lab7 BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False,
                                Kurs BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS JAVA(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Info_sys(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                lab6 BOOLEAN DEFAULT False,
                                lab7 BOOLEAN DEFAULT False,
                                lab8 BOOLEAN DEFAULT False,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Tech_auto(
                                id SERIAL PRIMARY KEY NOT NULL,
                                id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                lab1 BOOLEAN DEFAULT False,
                                lab2 BOOLEAN DEFAULT False,
                                lab3 BOOLEAN DEFAULT False,
                                lab4 BOOLEAN DEFAULT False,
                                lab5 BOOLEAN DEFAULT False,
                                lab6 BOOLEAN DEFAULT False,
                                lab7 BOOLEAN DEFAULT False,
                                lab8 BOOLEAN DEFAULT False,
                                lab9 BOOLEAN DEFAULT False,
                                lab10 BOOLEAN DEFAULT False,
                                lab11 BOOLEAN DEFAULT False,
                                lab12 BOOLEAN DEFAULT False,
                                lab13 BOOLEAN DEFAULT False,
                                lab14 BOOLEAN DEFAULT False,
                                lab15 BOOLEAN DEFAULT False,
                                lab16 BOOLEAN DEFAULT False,
                                SR BOOLEAN DEFAULT False,
                                PK BOOLEAN DEFAULT False, 
                                IK BOOLEAN DEFAULT False)""")
            self.conn.commit()

    def add_user(self, user_id, user_name, message_date):
        with self.conn:
            self.cur.execute(f"SELECT id FROM users WHERE id_tg={user_id}")
            id_data = self.cur.fetchone()
            if id_data is None:
                date_login = datetime.fromtimestamp(message_date).strftime('%d-%m-%y %H:%M:%S')
                self.cur.execute("INSERT INTO users(id_tg, username, date_reg) VALUES(%s,%s,%s);",
                                 (user_id, user_name, date_login))
                self.conn.commit()
                subjects = ["English", "KIS", "IIS", "WEB", "JAVA", "Info_sys", "Psychology", "Graj_zash", "Tech_auto"]
                for subject in subjects:
                    self.cur.execute(f"INSERT INTO {subject}(id_user) VALUES((SELECT id FROM users WHERE id_tg = %s));",
                                     (user_id,))
                    self.conn.commit()
            else:
                return
            return id_data

    def del_user(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE id_tg = %s;", (user_id,))
            self.conn.commit()

    def add_user_contact(self, user_id, user_phone):
        with self.conn:
            self.cur.execute("UPDATE users SET phone_numb = %s WHERE id_tg =%s;", (user_phone, user_id,))
            self.conn.commit()

    def add_user_date_birth(self, user_id, date_birth):
        with self.conn:
            self.cur.execute("UPDATE users SET date_birth = %s WHERE id_tg = %s;", (date_birth, user_id,))
            self.conn.commit()

    def add_user_name(self, user_id, name):
        with self.conn:
            self.cur.execute("UPDATE users SET name = %s WHERE id_tg = %s;", (name, user_id,))
            self.conn.commit()

    def get_user_info(self, user_id, ):
        with self.conn:
            self.cur.execute(f"SELECT name, phone_numb, date_birth FROM users WHERE id_tg={user_id}")
            user_info = self.cur.fetchall()
            return user_info

    def get_all_info_user(self):
        with self.conn:
            self.cur.execute(f"SELECT name, username, phone_numb, id_tg FROM users")
            user_info = self.cur.fetchall()
            return user_info

    def set_task_status(self, user_id, subject, task, status):
        with self.conn:
            self.cur.execute(f"UPDATE {subject} SET {task} = %s WHERE id_user = (SELECT id FROM users WHERE "
                             f"id_tg = %s);", (status, user_id))
            self.conn.commit()

    def get_task_status(self, user_id, subject, task):
        with self.conn:
            self.cur.execute(f"SELECT {task} FROM {subject} WHERE id_user = (SELECT id FROM users WHERE id_tg = %s);",
                             (user_id,))
            task_status = self.cur.fetchone()
            return task_status[0]

    def set_user_temp(self, user_id, temp):
        with self.conn:
            self.cur.execute("UPDATE users SET temp = %s WHERE id_tg = %s;", (temp, user_id,))
            self.conn.commit()

    def get_user_temp(self, user_id):
        with self.conn:
            self.cur.execute("SELECT temp FROM users WHERE id_tg = %s;", (user_id,))
            temp = self.cur.fetchone()
            return temp[0]

    def get_users_id_db(self):
        with self.conn:
            self.cur.execute("SELECT id_tg, date_birth, name FROM users")
            return self.cur.fetchall()

    def add_main_admin(self):
        with self.conn:
            self.cur.execute("SELECT username FROM admins")
            admin_name = self.cur.fetchone()
            if admin_name is None:
                self.cur.execute("INSERT INTO admins(id_tg,username) VALUES(%s,%s);", ("111312651", "MrDipper"))
                self.conn.commit()
            else:
                pass

    def add_admin(self, user_id, username):
        with self.conn:
            self.cur.execute("INSERT INTO admins(id_tg,username) VALUES(%s,%s);", (user_id, username))
            self.conn.commit()

    def edit_admin(self, user_id, username):
        with self.conn:
            self.cur.execute("UPDATE admins SET username = %s WHERE id_tg = %s;", (username, user_id))
            self.conn.commit()

    def get_admin_info(self, user_id):
        with self.conn:
            self.cur.execute("SELECT id_tg, username FROM admins WHERE id_tg = %s;", (user_id,))
            admin_id = self.cur.fetchone()
            return admin_id

    def add_ad_text(self, text):
        with self.conn:
            self.cur.execute(f"INSERT INTO ads(text) VALUES(%s)", (text,))
            self.conn.commit()

    def send_add(self):
        with self.conn:
            self.cur.execute(f"SELECT text, photo_url FROM ads WHERE id = (SELECT MAX(id) FROM ads)")
            return self.cur.fetchone()

    def add_ad_photo(self, src):
        with self.conn:
            self.cur.execute(f"UPDATE ads SET photo_url= %s WHERE id = (SELECT MAX(id) From ads);", (src,))
            self.conn.commit()
