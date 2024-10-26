class UserManager:
    # Инициализация словаря
    def __init__(self):
        self.user_dict = {}

    # Добавление пользователя
    def add_user(self, user_id, user_data):
        if user_id in self.user_dict:
            print(f'Клиент с ID {user_id} уже существует')
        else:
            self.user_dict[user_id] = user_data
            print(f'Клиент с ID {user_id} добавлен')

    # Удаление пользователя
    def remove_user(self, user_id):
        if user_id in self.user_dict:
            self.user_dict.pop(user_id)
            print(f'Клиент с ID {user_id} удалён')
        else:
            print(f'Клиент с ID {user_id} не найден')

    # Обновление данных о клиенте
    def update_user(self, user_id, user_data):
        if user_id in self.user_dict:
            self.user_dict[user_id] = user_data
            print(f'Клиент с ID {user_id} обновлён')
        else:
            print(f'Клиент с ID {user_id} не существует')

    # Вывод пользователя из словаря
    def find_user(self, user_id):
        if user_id in self.user_dict:
            return self.user_dict
        else:
            return f'Клиент с ID {user_id} не найден'