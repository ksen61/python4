import sqlite3
import SQL


class registrati:
    def regist(self):
        name = input("Введите имя: ")
        pasword = input("Введите пароль: ")
        while True:
            pasword2 = input("Подтвердите пароль: ")
            if pasword == pasword2:
                break
            else:
                print("Пароли не совпадают, введите пароль заново")
        data = {
            "Username": name,
            "Password": pasword,
            "Dolznost_ID": 3
        }
        SQL.SQLmy.insertdata('Clients', data)
        print("Вы зарегестрировались")

    def autoriz(login, pasword):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        sqlclient = f"SELECT username, password FROM Clients WHERE username ='{login}' AND password ='{pasword}'"
        id_client = f"SELECT Dolznost_ID FROM Clients WHERE username = '{login}'AND password ='{pasword}'"
        sqlsot = f"SELECT username, password FROM Sotrudnic WHERE username ='{login}' AND password ='{pasword}'"
        id_dolznostsot = f"SELECT Dolznost_ID FROM Sotrudnic WHERE username = '{login}'AND password ='{pasword}'"
        cursor.execute(sqlsot)
        resultst = cursor.fetchall()
        cursor.execute(sqlclient)
        resultcl = cursor.fetchall()
        if resultcl == [] and resultst == []:
            print("Пользователь не найден")
            return
        else:
            print("----------------------------")
            print("Вы вошли в систему")
            print("----------------------------")
        cursor.execute(id_dolznostsot)
        id_dolsot = cursor.fetchone()
        cursor.execute(id_client)
        id_dolcl = cursor.fetchone()
        if id_dolcl == None:
            return id_dolsot[0]
        elif id_dolsot == None:
            return id_dolcl[0]
        else:
            return