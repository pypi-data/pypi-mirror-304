class OrderManager:
    # Инициализация словаря
    def __init__(self):
        self.orders_dict = {}

    # Добавление заказа
    def create_order(self, order_id, order_data):
        if order_id in self.orders_dict:
            print(f'Заказ с ID {order_id} уже существует')
        else:
            self.orders_dict[order_id] = order_data
            print(f'Заказ с ID {order_id} добавлен')

    # Обновление заказа
    def update_order(self, order_id, order_data):
        if order_id in self.orders_dict:
            self.orders_dict[order_id] = order_data
            print(f'Заказ с ID {order_id} обновлён')
        else:
            print(f'Заказ с ID {order_id} не найден')

    # Отмена заказа
    def cancel_order(self, order_id):
        if order_id in self.orders_dict:
            self.orders_dict.pop(order_id)
            print(f'Заказ с ID {order_id} отменён')
        else:
            print(f'Заказ с ID {order_id} не найден')