class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        if user_id not in self.users:
            self.users[user_id] = user_data
            print(f'Клиент с ID {user_id} добавлен')
        else:
            print(f'Клиент с ID {user_id} уже существует')

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            print(f'Клиент с ID {user_id} удален')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def update_user(self, user_id, user_data):
        if user_id in self.users:
            self.users[user_id] = user_data
            print(f'Данные клиента с ID {user_id} обновлены')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def find_user(self, user_id):
        if user_id in self.users:
            print(f'ID {user_id}: {self.users[user_id]}')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def display_info(self):
        print(self.users)

# users = UserManager()
# users.add_user('123321', 'Alexey')
# users.add_user('333222', 'Maria')
# users.find_user('333222')
# users.update_user('333222', 'Lesya')
# users.find_user('333222')
# users.find_user('123321')
# users.remove_user('123321')
# users.find_user('123321')
