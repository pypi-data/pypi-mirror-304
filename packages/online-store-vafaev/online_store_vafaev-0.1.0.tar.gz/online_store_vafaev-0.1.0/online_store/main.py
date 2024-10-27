from user_management import UserManager
from order_management import OrderManager

print('Задание №1')
manager = UserManager()

# Добавление нового клиента
manager.add_user('user1@example.com', {'name': 'John Doe', 'age': 30})

# Обновление данных клиента
manager.update_user('user1@example.com', {'age': 31})

# Поиск клиента
print(manager.find_user('user1@example.com'))

# Удаление клиента
manager.remove_user('user1@example.com')

# Попытка поиска удалённого клиента
print(manager.find_user('user1@example.com'))

print()

print('Задание №2')

order_manager = OrderManager()

# Создание нового заказа
order_manager.create_order('order1001', {'user': 'Alice', 'item': 'Smartphone', 'price': 799})

# Обновление данных заказа
order_manager.update_order('order1001', {'status': 'shipped'})

# Отмена заказа
order_manager.cancel_order('order1001')