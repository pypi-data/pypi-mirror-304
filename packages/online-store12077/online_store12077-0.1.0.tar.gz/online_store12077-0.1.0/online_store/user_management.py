class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        if user_id not in self.users:
            self.users[user_id] = user_data
            return f'Клиент с ID {user_id} добавлен'
        else:
            return f'Клиент с ID {user_id} уже существует'

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return f'Клиент с ID {user_id} удалён'
        else:
            return f'Клиент с ID {user_id} не найден'

    def update_user(self, user_id, user_data):
        if user_id in self.users:
            self.users[user_id].update(user_data)
            return f'Данные клиента с ID {user_id} обновлены'
        else:
            return f'Клиент с ID {user_id} не найден'

    def find_user(self, user_id):
        if user_id in self.users:
            return f'Данные клиента: {self.users[user_id]}'
        else:
            return f'Клиент с ID {user_id} не найден'
