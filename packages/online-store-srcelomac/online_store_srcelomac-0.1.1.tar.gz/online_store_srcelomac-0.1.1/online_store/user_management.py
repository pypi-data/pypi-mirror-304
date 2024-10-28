class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        if user_id in self.users.keys():
            print(f"Клиент с ID {user_id} уже существует")
        else:
            self.users[user_id] = {
                'name': user_data['name'],  # Присваиваем значение напрямую
                'age': user_data['age']
            }
            print(f"Клиент с ID {user_id} добавлен")
        # Добавь логику создания учётной записи.
        # Когда учётная запись создана, выведи сообщение 'Клиент с ID <user_id> добавлен'.
        # Если учётная запись уже существует, создавать её заново не нужно, необходимо вывести сообщение 'Клиент с ID <user_id> уже существует'.

    def remove_user(self, user_id):
        try:
            self.users.pop(user_id)
        except KeyError:
            print(f"Клиент с ID {user_id} не найден")
        else:
            print(f"Клиент с ID {user_id} удалён")

        # Добавь логику удаления учётной записи.
        # Когда учётная запись удалена, выведи сообщение 'Клиент с ID <user_id> удалён'.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.

    def update_user(self, user_id, user_data):
        if user_id in self.users.keys():
            if 'name' in user_data.keys():
                self.users[user_id]['name'] = user_data['name']
            if 'age' in user_data.keys():
                self.users[user_id]['age'] = user_data['age']
            print(f"Данные клиента с ID {user_id} обновлены")
        else:
            print(f"Клиент с ID {user_id} не найден")

        # Добавь логику обновления данных клиента.
        # Когда данные о клиенте обновлены, выведи сообщение 'Данные клиента с ID <user_id> обновлены'.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.

    def find_user(self, user_id):
        if user_id in self.users.keys():
            return self.users[user_id]
        else:
            return (f"Клиент с ID {user_id} не найден")

        # Добавь логику поиска учётной записи.
        # Верни словарь с данными клиента, если он найден.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.