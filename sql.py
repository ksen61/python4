import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()
class SQLmy:
    def executeQuerry(querry, value = None):
        try:
            with sqlite3.connect('base.db') as conn:
                cursor = conn.cursor()
                if value:
                    cursor.execute(querry, value)
                else:
                    cursor.execute(querry)
                print("Операция успешна завершена")
        except sqlite3.Error as e:
            print(f"Ошибка: {e}")

    def insertdata(table, data):
        columns = ", ".join(data.keys())
        placeholder = ", ".join("?" for _ in data)
        querry = f"INSERT INTO {table}({columns}) VALUES ({placeholder})"
        SQLmy.executeQuerry(querry, tuple(data.values()))

    def updateData(table, data, id):
        updateData = ", ".join(f"{column} = ?" for column in data.keys())
        querry = f"UPDATE {table} SET {updateData} WHERE id = ?"
        listData = []
        for i in data.values():
            listData.append(i)
        listData.append(id)
        SQLmy.executeQuerry(querry, tuple(listData))

    def deleteData(table, id):
        delete_query = f"DELETE FROM {table} WHERE id = ?"
        listData = []
        listData.append(id)
        SQLmy.executeQuerry(delete_query, tuple(listData))

    def vivod(nametable):
        sql = f"SELECT * FROM {nametable}"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in range(len(result)):
            print(result[i])