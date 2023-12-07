import SQL


class Sotrud:
    def vibordei(self):
        while True:
            print("Выберите функцию:\n1. Посмотреть все товары\n2. Удалить товар\n3. Изменить товар\n4. Добавить товар\n5. Вернуться в главное меню")
            vibor = input()
            if vibor == "1":
                SQL.SQLmy.vivod('Products')
            elif vibor == "2":
                SQL.SQLmy.vivod('Products')
                while True:
                    try:
                        id = int(input("Введите id столбца, который хотите удалить: "))
                        break
                    except:
                        print("Это не число")
                SQL.SQLmy.deleteData('Products', id)
            elif vibor == "3":
                Sotrud.change(self)
            elif vibor == "4":
                Sotrud.dobav(self)
            else:
                break
    def change(self):
        SQL.SQLmy.vivod('Products')
        while True:
            try:
                id = int(input("Введите id продукта, данные которого нужно поменять: "))
                break
            except:
                print("Это не число")
        new_name = input("Введите новое название продукта: ")
        while True:
            try:
                new_price = float(input("Введите новую цену для продукта: "))
                break
            except:
                print("Неверная цена")
        newdata = {
            "Product": new_name,
            "Price": new_price
        }
        SQL.SQLmy.updateData('Products', newdata, id)
    def dobav(self):
        name = input("Введите название товара: ")
        while True:
            try:
                price = float(input("Введите цену товара: "))
                break
            except:
                print("Это не число")
        newdata = {
            "Product": name,
            "Price": price
        }
        SQL.SQLmy.insertdata('Products', newdata)