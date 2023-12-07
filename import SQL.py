import SQL
import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()


class Admin:
    def new_people(self):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        while True:
            password2 = input("Подтвердите пароль: ")
            if password == password2:
                break
            else:
                print("Пароли не совпадают, введите пароль заново")
        cursor.execute("SELECT * FROM Dolznosts")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        while True:
            dolznost = int(input("Введите код должности: "))
            if dolznost == 1 or dolznost == 2 or dolznost == 3:
                break
            else:
                print("Такой должности не существует")
        sotrudnicdata = {
            "Username": username,
            "Password": password,
            "Dolznost_ID": dolznost
        }
        if dolznost == 1 or dolznost == 2:
            nametable = 'Sotrudnic'
            SQL.SQLmy.insertdata(nametable, sotrudnicdata)
        elif dolznost == 3:
            nametable = 'Clients'
            SQL.SQLmy.insertdata(nametable, sotrudnicdata)

    def updatetable(self):
        while True:
            print("В какую таблицу вносить изменения:\n1. Сотрудники\n2. Клиенты\n3. Вернуться")
            a = input("Сделайте выбор: ")
            if a == "1":
                nametable = 'Sotrudnic'
                break
            elif a == "2":
                nametable = 'Clients'
                break
            elif a == "3":
                return
            else:
                print("Неверный выбор")
        SQL.SQLmy.vivod(nametable)
        print("Введите id пользователя, данные которого нужно поменять: ")
        id = int(input())
        print("Введите новое имя пользователя: ")
        username = input()
        print("Введите новый пароль: ")
        password = input()
        SQL.SQLmy.vivod('Dolznosts')
        while True:
            dolznost = input("Введите код должности: ")
            if dolznost == "1" or dolznost == "2" or dolznost == "3":
                break
            else:
                print("Такой должности не существует")
        newdata = {
            "Username": username,
            "Password": password,
            "Dolznost_ID": int(dolznost)
        }
        SQL.SQLmy.updateData(nametable, newdata, id)


    def deleteAtr(self):
        while True:
            print("В какую таблицу вносить изменения:\n1. Сотрудники\n2. Клиенты\n3. Вернуться")
            a = input("Выберите действие: ")
            if a == "1":
                nametable = 'Sotrudnic'
                SQL.SQLmy.vivod(nametable)
                id = int(input("Введите id столбца, который хотите удалить: "))
                SQL.SQLmy.deleteData(nametable, id)
            elif a == "2":
                nametable = 'Clients'
                SQL.SQLmy.vivod(nametable)
                id = int(input("Введите id столбца, который хотите удалить: "))
                SQL.SQLmy.deleteData(nametable, id)
            elif a == "3":
                return
            else:
                print("Неверная операция")


    def vibordey(self):
        while True:
            print(
                "Выберите дейтсвие:\n1. Новый пользователь\n2. Обновить данные в таблице\n3. Удаление столбцa\n4. Вернуться в главное меню")
            vibor = input()
            if vibor == "1":
                Admin.new_people(self=1)
            elif vibor == "2":
                Admin.updatetable(self=1)
            elif vibor == "3":
                Admin.deleteAtr(self=1)
            elif vibor == "4":
                return
            else:
                print("Неверная операция")