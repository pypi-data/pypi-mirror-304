class UserManager:
    def __init__(self, dictionary:dict={}):
        self.dictionary = dictionary
        # Добавь инициализацию атрибута — словаря для хранения учётных записей.

    def add_user(self, user_id, user_data):
        if user_id not in self.dictionary:
            self.dictionary[user_id] = user_data
            print(f'Клиент с ID {user_id}> добавлен')
        else:
            print(f'Клиент с ID {user_id} уже существует')
        # Добавь логику создания учётной записи.
        # Когда учётная запись создана, выведи сообщение 'Клиент с ID <user_id> добавлен'.
        # Если учётная запись уже существует, создавать её заново не нужно, необходимо вывести сообщение 'Клиент с ID <user_id> уже существует'.

    def remove_user(self, user_id):
        if user_id in self.dictionary:
            del self.dictionary[user_id]
            print(f'Клиент с ID {user_id} удалён')
        else:
            print(f'Клиент с ID {user_id} не найден')

        # Добавь логику удаления учётной записи.
        # Когда учётная запись удалена, выведи сообщение 'Клиент с ID <user_id> удалён'.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.

    def update_user(self, user_id, user_data):
        if user_id in self.dictionary:
            for key, value in user_data.items():
                self.dictionary[key] = value
            print(f'Данные клиента с ID {user_id} обновлены')
        else:
            print(f'Клиент с ID {user_id} не найден')
        # Добавь логику обновления данных клиента.
        # Когда данные о клиенте обновлены, выведи сообщение 'Данные клиента с ID <user_id> обновлены'.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.

    def find_user(self, user_id):
        if user_id in self.dictionary:
            return self.dictionary[user_id]
        else:
            print(f'Клиент с ID {user_id} не найден')
        # Добавь логику поиска учётной записи.
        # Верни словарь с данными клиента, если он найден.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.