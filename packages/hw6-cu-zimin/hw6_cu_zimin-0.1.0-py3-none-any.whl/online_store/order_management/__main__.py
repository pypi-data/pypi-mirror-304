from online_store.order_management import OrderManager

order_manager = OrderManager()

# Создание нового заказа
order_manager.create_order('order1001', {'user': 'Alice', 'item': 'Smartphone', 'price': 799})

# Обновление данных заказа
order_manager.update_order('order1001', {'status': 'shipped'})

# Отмена заказа
order_manager.cancel_order('order1001')
