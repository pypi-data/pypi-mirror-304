class UserManager:
    def __init__(self):
        self.data = {}

    def add_user(self, user_id, user_data):
        try:
            self.data.setdefault(user_id, user_data)
            print(f'Клиент с ID {user_id} добавлен')

        except KeyError:
            print(f'Клиент с ID {user_id} уже существует')

    def remove_user(self, user_id):
        try:
            self.data.pop(user_id)
            print(f'Клиент с ID {user_id} удалён')
        except KeyError:
            print(f'Клиент с ID {user_id} не найден')

    def update_user(self, user_id, user_data):
        try:
            self.data[user_id].update(user_data)
            print(f'Данные клиента с ID {user_id} обновлены')
        except KeyError:
            print(f'Клиент с ID {user_id} не найден')

    def find_user(self, user_id):
        try:
            return self.data[user_id]
        except KeyError:
            return 'Клиент с ID {0} не найден'.format(user_id)
