import SQL
import regestration
import admin
import client
import sqlite3
import sotrudnic

conn = sqlite3.connect('base.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dolznosts (
            id INTEGER PRIMARY KEY,
            Dolznost TEXT NOT NULL
            )
    ''')
cursor.execute(f"SELECT * FROM Dolznosts")
a = cursor.fetchall()
if a == []:
    dolznostdata = {
        "Dolznost": "Admin",
    }
    dolznostdata2 = {
        "Dolznost": "Sotrudnic",
    }
    dolznostdata3 = {
        "Dolznost": "Clients",
    }
    SQL.SQLmy.insertdata('Dolznosts', dolznostdata)
    SQL.SQLmy.insertdata('Dolznosts', dolznostdata2)
    SQL.SQLmy.insertdata('Dolznosts', dolznostdata3)
    print("Таблица должностей заполнена")

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sotrudnic (
            id INTEGER PRIMARY KEY,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            Dolznost_ID INTEGER NOT NULL,
            FOREIGN KEY (Dolznost_ID) REFERENCES Dolznosts (ID_Dolznost),
            UNIQUE(Username)
            )
    ''')

sql = f"SELECT id FROM Sotrudnic WHERE id = 1"
cursor.execute(sql)
result = cursor.fetchall()
if result == []:
    data = {
        "Username": "admin",
        "Password": "admin",
        "Dolznost_ID": 1
    }
    SQL.SQLmy.insertdata('Sotrudnic', data)

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clients (
                id INTEGER PRIMARY KEY,
                Username TEXT NOT NULL,
                Password TEXT NOT NULL,
                Dolznost_ID INTEGER NOT NULL,
                FOREIGN KEY (Dolznost_ID) REFERENCES Dolznosts (ID_Dolznost),
                UNIQUE(Username)
                )
        ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bill (
           id INTEGER PRIMARY KEY,
           Products TEXT NOT NULL,
           Datebill DATE NOT NULL,
           PriceOfOrd INT NOT NULL,
           Client_ID int NOT NULL,
           FOREIGN KEY (Client_ID) REFERENCES Clients(ID_Client)
           )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        Product TEXT NOT NULL,
        Price FLOAT NOT NULL
        )
''')
while True:
    print("-------------------------------------------------------")
    print("1. Зарегистрироваться\n2. Авторизоваться\n3. Выйти")
    print("-------------------------------------------------------")
    vibor = input()
    if vibor == "1":
        regestration.registrati.regist(self=1)
    elif vibor == "2":
        login = input("Введите логин: ")
        pasword = input("Введите пароль: ")
        id = regestration.registrati.autoriz(login, pasword)
        if id == 1:
            admin.Admin.vibordey(self=1)
        elif id == 2:
            sotrudnic.Sotrud.vibordei(self=1)
        elif id == 3:
            client.Client.vibor(login, pasword)
    elif vibor == "3":
        exit()
    else:
        print("Неверная команда")