import datetime
import random
import sqlite3
import time

import psycopg2

from connectors.DataBases import *


def reconnect_db():
    from connectors import DataBases
    DataBases.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot", host="illyashost.ddns.net")
    DataBases.db = DataBases.database.db
    DataBases.sql = DataBases.database.sql

    DataBases.stages = DataBases.database.stages
    DataBases.staff = DataBases.database.staff
    DataBases.settings = DataBases.database.settings


class DB:
    def __init__(self, db, sql):
        self.db = db
        self.sql = sql

    def create_table(self, table, columns_list):
        print(f"[...] Table {table} init...", end="")

        try:
            command = f"CREATE TABLE IF NOT EXISTS {table}("

            column_num = 1
            for column in columns_list:
                if column_num == 1:
                    command += f"{column} TEXT PRIMARY KEY, "
                else:
                    command += f"{column} TEXT, "
                column_num += 1
            command = command[:len(command) - 2] + ")"
            self.sql.execute(command)
            self.db.commit()
            print(f"\r[+] Table {table} init done")

        except psycopg2.OperationalError:
            print("[-] ", datetime.datetime.now())
            print(f"[-] Table {table} init OperationalError")

        except Exception as ex:
            print(f"\r[-] Table {table} init Error:")
            print("[-]", datetime.datetime.now())
            print("[-]", ex)


dbs = DB(db, sql)
dbs.create_table('crm', [
    'user_id',
    'balance',
    'reg_date',
    'last_update'])
dbs.create_table('developers', [
    'user_id',
    'status',
    'bio',
    'link1',
    'link2'
    ])
dbs.create_table('dev_reviews', [
    'row_id',
    'user_id',
    'dev_id',
    'stars',
    'comment',
    'review_date'])
dbs.create_table('customers', [
    'user_id',
    'status'])
dbs.create_table('softs', [
    "row_id",
    'developer_id',
    "soft_name",
    "soft_desc",
    'soft_link',
    'status'])
dbs.create_table('cli_reviews', [
    'row_id',
    'dev_id',
    'user_id',
    'stars',
    'comment',
    'review_date'])
dbs.create_table("personal_data", [
    "user_id",
    "phone1",
    "phone2",
    "country",
    "city"
])
dbs.create_table("fake_views", [
    "soft_id",
    "views"
])


class Sub:
    def __init__(self, user_id=None):
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot", host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql
        self.user_id = user_id

    def update(self):
        try:
            self.sql.execute(f"SELECT * FROM crm WHERE user_id = '{self.user_id}'")
            if self.sql.fetchone() is None:
                self.sql.execute(f"INSERT INTO crm VALUES ('{self.user_id}', '0', '{str(datetime.datetime.now())}', '{str(datetime.datetime.now())}')")
                self.db.commit()
            else:
                self.sql.execute(f"UPDATE crm SET last_update = '{str(datetime.datetime.now())}' WHERE user_id = '{self.user_id}'")
                self.db.commit()

        except psycopg2.OperationalError:
            time.sleep(1)
            reconnect_db()
            self.update()
        self.db.close()



class CRM:

    """
Данный класс описывает работу с базой данных "CRM". Он содержит методы для проверки существования пользователей в БД, получения данных о пользователе, изменения данных о пользователе и добавления новых пользователей в БД. Вводится идентификатор пользователя, который используется как ключ для доступа к данным в БД.
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql

    def exists(self) -> bool:
        self.sql.execute(f"SELECT * FROM crm WHERE user_id = '{self.user_id}'")
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def get(self) -> dict:
        if self.exists():
            self.sql.execute(f"SELECT * FROM crm WHERE user_id = '{self.user_id}'")
            for user in self.sql.fetchall():
                return {
                    "user_id": user[0],
                    "balance": user[1],
                    "reg_date": user[2],
                    "last_update": user[3],
                }

    def set(self, column: str, value: str, where: list):
        if self.exists():
            self.sql.execute(f"UPDATE crm SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
            self.db.commit()

    def new(self):
        if not self.exists():
            sql.execute(f"INSERT INTO crm VALUES ('{self.user_id}', '0', '{str(datetime.datetime.now())}', '{str(datetime.datetime.now())}')")
            db.commit()




class Customers:

    """
Данный класс представляет собой некоторую логику работы с таблицей "customers" в базе данных.

Конструктор принимает один аргумент - идентификатор пользователя.

Метод exists() проверяет, существует ли запись о пользователе в таблице по его идентификатору.

Метод get() возвращает словарь с информацией о пользователе (его идентификатор и статус) в том случае, если он существует в таблице.

Метод set() обновляет значение переданного атрибута у записи в таблице в соответствии с переданными условиями поиска записи.

Метод new() добавляет нового пользователя в таблицу, если его идентификатор еще не существует в ней.
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def exists(self):
        sql.execute(f"SELECT * FROM customers WHERE user_id = '{self.user_id}'")
        if sql.fetchone() is None:
            return False
        else:
            return True

    def get(self) -> dict:
        if self.exists():
            sql.execute(f"SELECT * FROM customers WHERE user_id = '{self.user_id}'")
            for user in sql.fetchall():
                return {
                    "user_id": user[0],
                    "status": user[1]
                }

    def set(self, column: str, value: str, where: list):
        if self.exists():
            sql.execute(f"UPDATE customers SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
            db.commit()

    def new(self):
        if not self.exists():
            sql.execute(f"INSERT INTO customers VALUES ('{self.user_id}', 'regular')")
            db.commit()


class Developers:

    """
Данный класс на языке Python выполняет функции работы с записями в базе данных разработчиков.

Метод '__init__' задает идентификатор разработчика при создании экземпляра класса.

Метод 'exists' выполняет выборку из базы данных, проверяет наличие заданного идентификатора и возвращает булево значение.

Метод 'get' также делает выборку из базы данных данных об указанном разработчике и возвращает словарь с данными - идентификатор и статус.

Метод 'set' изменяет значения отдельного поля (column) у конкретной записи (where) в базе данных.

Метод 'new' добавляет новую запись в базу данных, если запись с таким же идентификатором уже не существует.
    """

    def __init__(self, user_id=None):
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql
        self.user_id = user_id

    def exists(self):
        self.sql.execute(f"SELECT * FROM developers WHERE user_id = '{self.user_id}'")
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def get(self, status='checking'):
        if self.user_id == None:
            result = []
            self.sql.execute(f"SELECT * FROM developers WHERE status = '{status}'")
            for user in self.sql.fetchall():
                result.append({
                    "user_id": user[0],
                    "status": user[1],
                    "bio": user[2],
                    "link1": user[3],
                    "link2": user[4],
                })

            return result

        else:
            if self.exists():
                self.sql.execute(f"SELECT * FROM developers WHERE user_id = '{self.user_id}'")
                for user in self.sql.fetchall():
                    return {
                        "user_id": user[0],
                        "status": user[1],
                        "bio": user[2],
                        "link1": user[3],
                        "link2": user[4]
                    }

    def set(self, column: str, value: str, where: list):
        if self.exists():
            self.sql.execute(f"UPDATE developers SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
            self.db.commit()

    def new(self):
        if not self.exists():
            self.sql.execute(f"INSERT INTO developers VALUES ('{self.user_id}', 'regular', 'None', 'None', 'None')")
            self.db.commit()

    def remove(self):
        self.sql.execute(f"DELETE FROM developers WHERE user_id = '{self.user_id}'")
        self.db.commit()


class Softs:
    def __init__(self, developer_id=None, soft_id=None):
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql
        self.row_id = str(random.randint(1, int("9"*9)))
        self.developer_id = developer_id
        self.soft_id = soft_id

    def exists(self):
        if all((self.soft_id != None, self.developer_id != None)):
            self.sql.execute(f"SELECT * FROM softs WHERE developer_id = '{self.developer_id}' AND row_id = '{self.soft_id}'")
        elif all((self.soft_id != None, self.developer_id == None)):
            self.sql.execute(f"SELECT * FROM softs WHERE row_id = '{self.soft_id}'")
        elif all((self.soft_id == None, self.developer_id != None)):
            self.sql.execute(f"SELECT * FROM softs WHERE developer_id = '{self.developer_id}'")
        else:
            self.sql.execute(f"SELECT * FROM softs")

        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def get(self, status=None):
        if status != None:
            result = []
            self.sql.execute(f"SELECT * FROM softs WHERE status = '{str(status)}'")
            for i in self.sql.fetchall():
                result.append({
                    "row_id": i[0],
                    "developer_id": i[1],
                    "soft_name": i[2],
                    "soft_desc": i[3],
                    "soft_link": i[4],
                    "status": i[5]
                })
            return result
        else:
            result = []
            if self.exists():
                if all((self.soft_id != None, self.developer_id != None)):
                    self.sql.execute(f"SELECT * FROM softs WHERE developer_id = '{self.developer_id}' AND row_id = '{self.soft_id}'")
                    for i in self.sql.fetchall():
                        return {
                            "row_id": i[0],
                            "developer_id": i[1],
                            "soft_name": i[2],
                            "soft_desc": i[3],
                            "soft_link": i[4],
                            "status": i[5]
                            }
                else:
                    if self.soft_id != None:
                        self.sql.execute(f"SELECT * FROM softs WHERE row_id = '{self.soft_id}'")
                        for i in self.sql.fetchall():
                            return {
                            "row_id": i[0],
                            "developer_id": i[1],
                            "soft_name": i[2],
                            "soft_desc": i[3],
                            "soft_link": i[4],
                            "status": i[5]
                            }

                    elif self.developer_id != None:
                        self.sql.execute(f"SELECT * FROM softs WHERE developer_id = '{self.developer_id}'")
                        for i in sql.fetchall():
                            result.append({
                            "row_id": i[0],
                            "developer_id": i[1],
                            "soft_name": i[2],
                            "soft_desc": i[3],
                            "soft_link": i[4],
                            "status": i[5]
                            })
                return result

    def set(self, column: str, value: str, where: list):
        if self.exists():
            if len(where) == 2:
                self.sql.execute(f"UPDATE softs SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
            elif len(where) == 4:
                self.sql.execute(f"UPDATE softs SET {column} = '{value}' WHERE {where[0]} = '{where[1]}' AND {where[2]} = '{where[3]}'")
            self.db.commit()

    def remove(self):
        if all((self.soft_id != None, self.developer_id != None)):
            self.sql.execute(f"DELETE FROM softs WHERE developer_id = '{self.developer_id}' AND row_id = '{self.soft_id}'")
        else:
            if self.soft_id != None:
                self.sql.execute(f"DELETE FROM softs WHERE row_id = '{self.soft_id}'")
            elif self.developer_id != None:
                self.sql.execute(f"DELETE FROM softs WHERE developer_id = '{self.developer_id}'")
        self.db.commit()
 
    def new(self, soft_name, soft_desc, soft_link):
        self.sql.execute(f"INSERT INTO softs VALUES ('{self.soft_id}', '{self.developer_id}', '{soft_name}', '{soft_desc}', '{soft_link}', 'None')")
        self.db.commit()


class DevReviews:
    def __init__(self, user_id=None, developer_id=None):
        self.user_id = user_id
        self.developer_id = developer_id
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql

    def exists(self):
        if all((self.developer_id != None, self.user_id != None)):
            self.sql.execute(f"SELECT * FROM dev_reviews WHERE user_id = '{self.user_id}' AND dev_id = '{str(self.developer_id)}'")
        else:
            if all((self.developer_id != None, self.user_id == None)):
                self.sql.execute(f"SELECT * FROM dev_reviews WHERE dev_id = '{str(self.developer_id)}'")
            elif all((self.developer_id == None, self.user_id != None)):
                self.sql.execute(f"SELECT * FROM dev_reviews WHERE user_id = '{self.user_id}'")

        if self.sql.fetchone() is None:
            return False

        return True

    def get(self):
        if self.exists():
            if all((self.developer_id != None, self.user_id != None)):
                self.sql.execute(f"SELECT * FROM dev_reviews WHERE user_id = '{self.user_id}' AND dev_id = '{str(self.developer_id)}'")
                for i in self.sql.fetchall():
                    return {
                        "row_id": i[0],
                        'developer_id': i[1],
                        "soft_name": i[2],
                        "soft_desc": i[3],
                        'soft_link': i[4],
                        'status': i[5]
                    }

            else:
                result = []
                if all((self.developer_id != None, self.user_id == None)):
                    self.sql.execute(f"SELECT * FROM dev_reviews WHERE dev_id = '{str(self.developer_id)}'")
                elif all((self.developer_id == None, self.user_id != None)):
                    self.sql.execute(f"SELECT * FROM dev_reviews WHERE user_id = '{self.user_id}'")
                for i in self.sql.fetchall():
                    result.append({
                        "row_id": i[0],
                        'developer_id': i[1],
                        "soft_name": i[2],
                        "soft_desc": i[3],
                        'soft_link': i[4],
                        'status': i[5]
                    })
                return result

    def set(self, column: str, value: str, where: list):
        if self.exists():
            if len(where) == 2:
                self.sql.execute(f"UPDATE dev_reviews SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
            elif len(where) == 4:
                self.sql.execute(f"UPDATE dev_reviews SET {column} = '{value}' WHERE {where[0]} = '{where[1]}' AND {where[2]} = '{where[3]}'")
            self.db.commit()

    def remove(self):
        if all((self.developer_id != None, self.user_id != None)):
            if self.exists():
                self.sql.execute(f"DELETE FROM dev_reviews WHERE user_id = '{self.user_id}' AND dev_id = '{str(self.developer_id)}'")
                self.db.commit()

    def add(self, stars, comment):
        if self.exists():
            row_id = random.randint(1, 999999999)
            self.sql.execute(f"""INSERT INTO dev_reviews VALUES(
            '{str(row_id)}', 
            '{str(self.user_id)}', 
            '{str(stars)}', 
            '{str(comment)}', 
            '{str(datetime.datetime.now())}')""")
            self.db.commit()


class PersonalData:
    def __init__(self, user_id=None):
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql
        self.user_id = user_id

    def exists(self):
        if self.user_id != None:
            self.sql.execute(f"SELECT * FROM personal_data WHERE user_id = '{str(self.user_id)}'")
        else:
            self.sql.execute(f"SELECT * FROM personal_data")

        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def get(self):
        if self.exists():
            if self.user_id != None:
                self.sql.execute(f"SELECT * FROM personal_data WHERE user_id = '{str(self.user_id)}'")
                for data in self.sql.fetchall():
                    return {
                        "user_id": data[0],
                        "phone1": data[1],
                        "phone2": data[2],
                        "country": data[3],
                        "city": data[4]
                    }

            else:
                result = []
                self.sql.execute(f"SELECT * FROM personal_data")
                for data in self.sql.fetchall():
                    result.append({
                        "user_id": data[0],
                        "phone1": data[1],
                        "phone2": data[2],
                        "country": data[3],
                        "city": data[4]
                    })
                return result

    def set(self, column: str, value: str, where: list):
        if len(where) == 2:
            self.sql.execute(f"UPDATE personal_data SET {column} = '{value}' WHERE {where[0]} = '{where[1]}'")
        elif len(where) == 4:
            self.sql.execute(f"UPDATE personal_data SET {column} = '{value}' WHERE {where[0]} = '{where[1]}' AND {where[2]} = '{where[3]}'")
        self.db.commit()

    def new(self, phone1, phone2, country, city):
        if not self.exists():
            self.sql.execute(f"INSERT INTO personal_data VALUES('{self.user_id}', '{phone1}', '{phone2}', '{country}', '{city}')")
            self.db.commit()


class Fake_views:
    def __init__(self, soft_id):
        self.database = ilm.postgreSQL_connect(user="postgres", password="armageddon", database="projects_bot",
                                               host="illyashost.ddns.net")
        self.db = self.database.db
        self.sql = self.database.sql
        self.soft_id = soft_id

    def exists(self):
        self.sql.execute(f"SELECT * FROM fake_views WHERE soft_id = '{self.soft_id}'")
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def get(self):
        if self.exists():
            self.sql.execute(f"SELECT * FROM fake_views WHERE soft_id = '{self.soft_id}'")
            for i in self.sql.fetchall():
                return int(i[1])
        else:
            self.sql.execute(f"INSERT INTO fake_views VALUES ('{self.soft_id}','0')")
            self.db.commit()
            return 0

    def set(self, amount):
        self.sql.execute(f"UPDATE fake_views SET views = '{str(amount)}' WHERE soft_id = '{str(self.soft_id)}'")
        self.db.commit()





