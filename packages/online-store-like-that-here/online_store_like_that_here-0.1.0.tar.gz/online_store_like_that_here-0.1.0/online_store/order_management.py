class OrderManager:
    def __init__(self, dictionary:dict={}):
        self.dictionary = dictionary

    # Добавь инициализацию атрибута — словаря для хранения заказов.

    def create_order(self, order_id, order_data):
        if order_id not in self.dictionary:
            self.dictionary[order_id] = order_data
            print(f'Заказ с ID {order_id} обновлён')
        else:
            print(f'Заказ с ID {order_id} уже существует')
    # Добавь логику создания заказа.
    # Когда заказ обновлён, выведи сообщение 'Заказ с ID <order_id> обновлён'.
    # Если заказ с таким ID уже существует, создавать его заново не нужно. Выведи сообщение 'Заказ с ID <order_id> уже существует'.

    def update_order(self, order_id, order_data):
        if order_id not in self.dictionary:
            print(f'Заказ с ID {order_id} не найден')
        else:
            for key, value in self.dictionary.items():
                self.dictionary[key] = value
            print(f'Заказ с ID {order_id} добавлен')
    # Добавь логику обновления заказа — выведи соответствующее сообщение.
    # Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> добавлен'.
    # Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.

    def cancel_order(self, order_id):
        if order_id not in self.dictionary:
            print(f'Заказ с ID {order_id} не найден')
        else:
            del self.dictionary[order_id]
            print(f'Заказ с ID {order_id} отменён')
# Добавь логику отмены заказа.
# Когда заказ создан, выведи сообщение 'Заказ с ID <order_id> отменён'.
# Если заказа не существует, выведи сообщение 'Заказ с ID <order_id> не найден'.