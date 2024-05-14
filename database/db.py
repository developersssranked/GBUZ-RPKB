import sqlite3

import datetime


def create_table_users_DB():
    db=sqlite3.connect('database/users.db',check_same_thread=False)
    sql=db.cursor()

    sql.execute('''CREATE TABLE "users" (

    "id" INTEGER NOT NULL UNIQUE,

    "username" TEXT DEFAULT (32),

    "chat_id" TEXT NOT NULL,
                
    "status" INTEGER NOT NULL,  

    PRIMARY KEY("id" AUTOINCREMENT)

    );''')
    
    db.commit()
    
    sql.close()





def is_exist_users_table_DB():
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()
    

    # Проверка существования таблицы "users"
    sql.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='users' ''')
    table_exists = sql.fetchone()


    if table_exists:
        db.close()
        return True
    else:
        db.close()
        return False


def insert_user_DB(users_data):
    """users_data format: dict({'username':username,'chat_id':chat_id})"""
    
    if not is_exist_users_table_DB():
        create_table_users_DB()
        
    # Соединение с базой данных
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()

    user_data=(users_data['username'], users_data['chat_id'], 0)
    
    

    # Загрузка данных в таблицу "leads"
    sql.execute('INSERT INTO "users" (username, chat_id, status) VALUES (?,?,?)', user_data)

    # Сохранение изменений
    db.commit()

    # Закрытие соединения с базой данных
    db.close()


def get_user_status(username):
    # Выполнение SQL-запроса для поиска пользователя по имени пользователя

    if not is_exist_users_table_DB():
        create_table_users_DB()
        
    # Соединение с базой данных
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()
    
    sql.execute("SELECT status FROM users WHERE username = ?", (username,))
    result = sql.fetchone()

    
    if result:
        return result[0]
    else:
        return None



def select_all_users_status_1_DB():
    if not is_exist_users_table_DB():
        create_table_users_DB()
        
    # Соединение с базой данных
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()
    
    sql.execute("SELECT username FROM users WHERE status = ?", (1,))
    result = sql.fetchall()

    db.close()

    return result

    



def update_user_status( status, chat_id = None, username = None):
    if not is_exist_users_table_DB():
        create_table_users_DB()
        
    # Соединение с базой данных
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()
    if chat_id is not None:

        sql.execute("UPDATE users SET status = ? WHERE chat_id = ?", (status, chat_id))
    else:
        sql.execute("UPDATE users SET status = ? WHERE username = ?", (status, username))
    db.commit()







def is_exist_user(username):

    if not is_exist_users_table_DB():
        create_table_users_DB()
        
    # Соединение с базой данных
    db = sqlite3.connect('database/users.db',check_same_thread=False)
    sql = db.cursor()

    sql.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    result = sql.fetchone()[0]

    
    return result > 0