class UserManager:
    def __init__(self, account_dict={}):
        # Добавь инициализацию атрибута — словаря для хранения учётных записей.
        self.account_dict = account_dict

    def add_user(self, user_id, user_data):
        # Добавь логику создания учётной записи.
        # Когда учётная запись создана, выведи сообщение 'Клиент с ID <user_id> добавлен'.
        # Если учётная запись уже существует, создавать её заново не нужно, необходимо вывести сообщение 'Клиент с ID <user_id> уже существует'.
        if user_id in self.account_dict.keys():
            print(f'Клиент с ID {user_id} уже существует')
        else:
            self.account_dict[user_id] = user_data
            print(f'Клиент с ID <{user_id}> добавлен')

    def remove_user(self, user_id):
        if user_id in self.account_dict.keys():
            del self.account_dict[user_id]
            print(f'Клиент с ID <{user_id}> удалён')
        else:
            print(f'Клиент с ID <{user_id}> не найден')

    # Добавь логику удаления учётной записи.
    # Когда учётная запись удалена, выведи сообщение 'Клиент с ID <user_id> удалён'.
    # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.

    def update_user(self, user_id, user_data):

        # Добавь логику обновления данных клиента.
        # Когда данные о клиенте обновлены, выведи сообщение 'Данные клиента с ID <user_id> обновлены'.
        # Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.
        if user_id not in self.account_dict.keys():
            print(f'Клиент с ID {user_id} не найден')
        else:
            self.account_dict[user_id] = user_data
            print(f'Данные клиента с ID <{user_id}> обновлены')

    def find_user(self, user_id):
        if user_id in self.account_dict:
            return {user_id: self.account_dict[user_id]}
        else:
            print(f'Клиент с ID {user_id} не найден')
            return
# Добавь логику поиска учётной записи.
# Верни словарь с данными клиента, если он найден.
# Если учётной записи не существует, выведи сообщение 'Клиент с ID <user_id> не найден'.
