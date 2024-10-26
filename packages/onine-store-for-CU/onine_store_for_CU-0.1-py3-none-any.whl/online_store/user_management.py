class UserManager:
    def __init__(self):
        self.User_Manager = {}

    def add_user(self, user_id, user_data):
        if user_id in self.User_Manager:
            print(f'Клиент с ID {user_id} уже существует')
        else:
            print(f'Клиент с ID {user_id} добавлен')
            self.User_Manager[user_id] = user_data

    def remove_user(self, user_id):
        if user_id in self.User_Manager:
            self.User_Manager.pop(user_id)
            print(f'Клиент с ID {user_id} удален')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def update_user(self, user_id, user_data):
        if user_id in self.User_Manager:
            for item in user_data:
                self.User_Manager[user_id][item] = user_data[item]
            print(f'Клиент с ID {user_id} обновлены')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def find_user(self, user_id):
        if user_id in self.User_Manager:
            return self.User_Manager[user_id]
        else:
            print(f'Клиент с ID {user_id} не найден')

