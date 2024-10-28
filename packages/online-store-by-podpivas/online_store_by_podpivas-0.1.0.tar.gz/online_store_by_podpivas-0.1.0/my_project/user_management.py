class UserManager:
    def __init__(self):
        # Создай словарь для хранения учётных записей, где ключ - ID клиента, а значение - данные клиента.
        self.users = {}

    def add_user(self, user_id, user_data):
        # Проверяем, что данный ID зарегистрирован
        if user_id in self.users:
            print(f"Клиент с ID {user_id} уже существует")
        else:
            # Добавляем нового юзера
            self.users[user_id] = user_data
            print(f"Клиент с ID {user_id} добавлен")

    def remove_user(self, user_id):
        #Проверяем, что данный ID зарегистрирован
        if user_id in self.users:
            # Удаляем юзера из словаря
            self.users.pop(user_id)
            print(f"Клиент с ID {user_id} удалён")
        else:
            print(f"Клиент с ID {user_id} не найден")

    def update_user(self, user_id, user_data):
        # Проверяем, что данный ID зарегистрирован
        if user_id in self.users:
            # Обновляем данные клиента в словаре
            self.users[user_id] = user_data
            print(f"Данные клиента с ID {user_id} обновлены")
        else:
            print(f"Клиент с ID {user_id} не найден")

    def find_user(self, user_id):
        # Проверяем, что данный ID зарегистрирован
        if user_id in self.users:
            # Возвращаем данные клиента
            return self.users[user_id]
        else:
            print(f"Клиент с ID {user_id} не найден")
            return None
