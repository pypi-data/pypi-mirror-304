class OrderManager:
    def __init__(self):
        self.orders = {}

    # Добавь инициализацию атрибута — словаря для хранения заказов.

    def create_order(self, order_id, order_data):
        if order_id in self.orders.keys():
            print(f"Заказ с ID {order_id} уже существует")
        else:
            self.orders[order_id] = {
                'user': order_data['user'],
                'item': order_data['item'],
                'price': order_data['price']
            }
            print(f"Заказ с ID {order_id} добавлен")

    # Добавь логику создания заказа.
    # Когда заказ обновлён, выведи сообщение 'Заказ с ID <order_id> обновлён'.
    # Если заказ с таким ID уже существует, создавать его заново не нужно. Выведи сообщение 'Заказ с ID <order_id> уже существует'.

    def update_order(self, order_id, order_data):
        if order_id in self.orders.keys():
            if 'user' in order_data.keys():
                self.orders['user'] = order_data['user']
            if 'item' in order_data.keys():
                self.orders['item'] = order_data['item']
            if 'price' in order_data.keys():
                self.orders['price'] = order_data['price']
            if 'status' in order_data.keys():
                self.orders['status'] = order_data['status']
            print(f"Заказ с ID {order_id} обновлён")
        else:
            print(f"Заказ с ID {order_id} не найден")

    # Добавь логику обновления заказа — выведи соответствующее сообщение.
    # Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> добавлен'.
    # Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.

    def cancel_order(self, order_id):
        try:
            self.orders.pop(order_id)
        except KeyError:
            print(f"Заказ с ID {order_id} не найден")
        else:
            print(f"Заказ с ID {order_id} отменён")

    # Добавь логику отмены заказа.
    # Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> отменён'.
    # Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.