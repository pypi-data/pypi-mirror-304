class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        if user_id in self.users:
            print(f"Клиент с ID {user_id} уже существует")
            return
        self.users[user_id] = user_data
        print(f"Клиент с ID {user_id} добавлен")

    def remove_user(self, user_id):
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return
        del self.users[user_id]
        print(f"Клиент с ID {user_id} удалён")

    def update_user(self, user_id, user_data):
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return
        user = self.users[user_id]
        for key, val in user_data.items():
            user[key] = val
        print(f"Данные клиента с ID {user_id} обновлены")

    def find_user(self, user_id):
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return
        return self.users[user_id]
