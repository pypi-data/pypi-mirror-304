class OrderManager:
    def __init__(self):
        # Добавь инициализацию атрибута — словаря для хранения заказов.
        self.order_dict = {}

    def create_order(self, order_id, order_data):

        # Добавь логику создания заказа.
        # Когда заказ обновлён, выведи сообщение 'Заказ с ID <order_id> обновлён'.
        # Если заказ с таким ID уже существует, создавать его заново не нужно. Выведи сообщение 'Заказ с ID <order_id> уже существует'.
        if order_id in self.order_dict.keys():
            print(f'Заказ с ID {order_id} обновлен')
        else:
            self.order_dict[order_id] = order_data
            print(f'заказ с ID <{order_id}> добавлен')

    def update_order(self, order_id, order_data):

        # Добавь логику обновления заказа — выведи соответствующее сообщение.
        # Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> добавлен'.
        # Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.
        if order_id not in self.order_dict.keys():
            print(f'Заказ с ID {order_id} не найден')
        else:
            self.order_dict[order_id] = order_data
            print(f'Данные заказа с ID <{order_id}> обновлены')

    def cancel_order(self, order_id):
        # Добавь логику отмены заказа.
        # Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> отменён'.
        # Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.
        if order_id in self.order_dict.keys():
            del self.order_dict[order_id]
            print(f'Заказ с ID <{order_id}> отменён')
        else:
            print(f'Заказ с ID <{order_id}> не найден')
