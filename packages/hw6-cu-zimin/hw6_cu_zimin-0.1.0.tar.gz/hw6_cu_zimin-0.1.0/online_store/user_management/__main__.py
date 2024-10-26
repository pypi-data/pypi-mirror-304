from online_store.user_management import UserManager

manager = UserManager()

# Добавление нового клиента
manager.add_user('user1@example.com', {'name': 'John Doe', 'age': 30})

# Обновление данных клиента
manager.update_user('user1@example.com', {'age': 31})

# Поиск клиента
print(manager.find_user('user1@example.com'))

# Удаление клиента
manager.remove_user('user1@example.com')

# Попытка поиска удалённого клиента
print(manager.find_user('user1@example.com'))
