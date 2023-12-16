import sqlite3

conn = sqlite3.connect('store.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
''')

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def save_to_db(self):
        cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
                       (self.name, self.price, self.quantity))
        conn.commit()

class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def save_to_db(self):
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                       (self.username, self.password, self.role))
        conn.commit()

    def get_all_products(self):
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()

    def add_product_to_order(self, product_id, quantity):
        all_products = self.get_all_products()
        product_ids = [product[0] for product in all_products]

        if int(product_id) in product_ids:
            available_quantity = [product[3] for product in all_products if product[0] == int(product_id)][0]

            if available_quantity >= int(quantity):
                cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))

                cursor.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)',
                               (self.user_id, product_id, quantity))
                conn.commit()

                print(f'Товар с ID {product_id} успешно добавлен в ваш заказ.')
            else:
                print(f'Недостаточное количество товара с ID {product_id} в магазине.')
        else:
            print(f'Товар с ID {product_id} не существует в магазине. Пожалуйста, выберите существующий товар.')

    def delete_order(self, order_id):
        cursor.execute('DELETE FROM orders WHERE id=? AND user_id=?', (order_id, self.user_id))
        conn.commit()

    def view_orders(self):
        cursor.execute('SELECT * FROM orders WHERE user_id=?', (self.user_id,))
        orders = cursor.fetchall()
        if orders:
            print("Ваши заказы:")
            for order in orders:
                print(f"Заказ {order[0]}: Товар {order[2]}, Количество: {order[3]}")
        else:
            print("У вас нет заказов.")

    def update_user_info(self, new_username, new_password):
        cursor.execute('UPDATE users SET username=?, password=? WHERE id=?',
                       (new_username, new_password, self.user_id))
        conn.commit()

    def add_product(self, name, price, quantity):
        if self.role == 'employee':
            new_product = Product(name, price, quantity)
            new_product.save_to_db()
            print(f'Товар "{name}" успешно добавлен в магазин.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def delete_product(self, product_id):
        if self.role == 'employee':
            cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
            conn.commit()
            print(f'Товар с ID {product_id} успешно удален из магазина.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def update_product(self, product_id, name, price, quantity):
        if self.role == 'employee':
            cursor.execute('UPDATE products SET name=?, price=?, quantity=? WHERE id=?',
                           (name, price, quantity, product_id))
            conn.commit()
            print(f'Товар с ID {product_id} успешно обновлен.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def filter_products(self, keyword):
        if self.role == 'employee':
            cursor.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + keyword + '%',))
            products = cursor.fetchall()
            if products:
                print("Результаты фильтрации:")
                for product in products:
                    print(f"ID: {product[0]}, Название: {product[1]}, Цена: {product[2]}, Количество: {product[3]}")
            else:
                print("Нет товаров по вашему запросу.")
        else:
            print('У вас нет прав для выполнения этого действия.')

    def view_all_products(self):
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        if products:
            print("Все товары в магазине:")
            for product in products:
                print(f"ID: {product[0]}, Название: {product[1]}, Цена: {product[2]}, Количество: {product[3]}")
        else:
            print("Магазин пуст, видимо сотрудник пока не добавил товар :/")

    def view_all_employees(self):
        if self.role == 'admin':
            cursor.execute('SELECT * FROM users WHERE role="employee"')
            employees = cursor.fetchall()
            if employees:
                print("Все сотрудники:")
                for employee in employees:
                    print(f"ID: {employee[0]}, Имя пользователя: {employee[1]}")
            else:
                print("Нет зарегистрированных сотрудников.")
        else:
            print('У вас нет прав для выполнения этого действия.')

    def add_employee(self, username, password):
        if self.role == 'admin':
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, "employee")',
                           (username, password))
            conn.commit()
            print(f'Сотрудник {username} успешно добавлен.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def update_employee_info(self, employee_id, new_username, new_password):
        if self.role == 'admin':
            cursor.execute('UPDATE users SET username=?, password=? WHERE id=? AND role="employee"',
                           (new_username, new_password, employee_id))
            conn.commit()
            print(f'Информация о сотруднике с ID {employee_id} успешно обновлена.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def delete_employee(self, employee_id):
        if self.role == 'admin':
            cursor.execute('DELETE FROM users WHERE id=? AND role="employee"', (employee_id,))
            conn.commit()
            print(f'Сотрудник с ID {employee_id} успешно удален.')
        else:
            print('У вас нет прав для выполнения этого действия.')

    def filter_employees(self, keyword):
        if self.role == 'admin':
            cursor.execute('SELECT * FROM users WHERE role="employee" AND username LIKE ?', ('%' + keyword + '%',))
            employees = cursor.fetchall()
            if employees:
                print("Результаты фильтрации сотрудников:")
                for employee in employees:
                    print(f"ID: {employee[0]}, Имя пользователя: {employee[1]}")
            else:
                print("Нет сотрудников по вашему запросу.")
        else:
            print('У вас нет прав для выполнения этого действия.')

def welcome_menu():
    print("Добро пожаловать в магазин")
    print("Выберите действие:")
    print("1. Авторизация")
    print("2. Регистрация")

if __name__ == '__main__':
    while True:
        welcome_menu()
        choice = input("Введите номер действия: ")

        if choice == '1':

            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user_data = cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()

            if user_data:
                user = User(*user_data)
                print(f'Добро пожаловать, {user.username} ({user.role})')

                while True:
                    print("\nМеню:")
                    if user.role == 'client':
                        print("1. Добавить товар в заказ")
                        print("2. Удалить заказ")
                        print("3. Просмотр заказа")
                        print("4. Изменить свои данные")
                        print("5. Просмотреть все товары")

                    elif user.role == 'employee':
                        print("1. Добавить товар")
                        print("2. Удалить товар")
                        print("3. Изменить товар")
                        print("4. Фильтр товаров")
                        print("5. Просмотреть все товары")
                        print("6. Изменить свои данные")

                    elif user.role == 'admin':
                        print("1. Просмотреть всех сотрудников")
                        print("2. Добавить сотрудника")
                        print("3. Изменить данные сотрудника")
                        print("4. Удалить сотрудника")
                        print("5. Фильтр сотрудников")

                    print("0. Выйти")

                    user_choice = input("Введите номер действия: ")

                    if user_choice == '1':

                        if user.role == 'client':
                            product_id = input("Введите ID товара: ")
                            quantity = input("Введите количество: ")
                            user.add_product_to_order(product_id, quantity)

                        elif user.role == 'employee':
                            product_name = input("Введите название товара: ")
                            product_price = input("Введите цену товара: ")
                            product_quantity = input("Введите количество товара: ")
                            user.add_product(product_name, product_price, product_quantity)

                        elif user.role == 'admin':
                            user.view_all_employees()


                    elif user_choice == '2':

                        if user.role == 'client':
                            order_id = input("Введите ID заказа для удаления: ")
                            user.delete_order(order_id)

                        elif user.role == 'employee':
                            product_id = input("Введите ID товара для удаления: ")
                            user.delete_product(product_id)

                        elif user.role == 'admin':
                            new_username = input("Введите имя пользователя нового сотрудника: ")
                            new_password = input("Введите пароль нового сотрудника: ")
                            user.add_employee(new_username, new_password)

                    elif user_choice == '3':

                        if user.role == 'client':
                            user.view_orders()

                        elif user.role == 'employee':
                            user.view_all_products()

                        elif user.role == 'admin':
                            employee_id = input("Введите ID сотрудника для изменения данных: ")
                            new_username = input("Введите новое имя пользователя: ")
                            new_password = input("Введите новый пароль: ")
                            user.update_employee_info(employee_id, new_username, new_password)

                    elif user_choice == '4':

                        if user.role == 'client':
                            new_username = input("Введите новое имя пользователя: ")
                            new_password = input("Введите новый пароль: ")
                            user.update_user_info(new_username, new_password)

                        elif user.role == 'employee':
                            keyword = input("Введите ключевое слово для фильтрации: ")
                            user.filter_products(keyword)

                        elif user.role == 'admin':
                            employee_id = input("Введите ID сотрудника для удаления: ")
                            user.delete_employee(employee_id)
                        else:
                            print('У вас нет прав для выполнения этого действия.')

                    elif user_choice == '5':
                        if user.role == 'client' or user.role == 'employee':
                            user.view_all_products()

                        elif user.role == 'admin':
                            keyword = input("Введите ключевое слово для фильтрации сотрудников: ")
                            user.filter_employees(keyword)
                        else:
                            print('У вас нет прав для выполнения этого действия.')

                    elif user_choice == '6' and user.role == 'employee':
                        if user.role == 'employee':
                            new_username = input("Введите новое имя пользователя: ")
                            new_password = input("Введите новый пароль: ")
                            user.update_user_info(new_username, new_password)
                        elif user.role == 'admin':
                            keyword = input("Введите ключевое слово для фильтрации сотрудников: ")
                            user.filter_employees(keyword)
                        else:
                            print('У вас нет прав для выполнения этого действия.')

                    elif user_choice == '0':
                        break

                    else:
                        print('Некорректный выбор. Пожалуйста, введите число от 0 до 6.')

                break
            else:
                print('Неверные учетные данные. Попробуйте еще раз.')
                print()

        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (client, employee, admin): ")

            if role not in ['client', 'emloyee', 'admin']:
                print('Некорректная роль. Регистрация отменена.')
                continue

            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            print('Регистрация успешна. Теперь вы можете авторизоваться.')

        else:
            print('Некорректный выбор. Пожалуйста, введите 1 или 2.')