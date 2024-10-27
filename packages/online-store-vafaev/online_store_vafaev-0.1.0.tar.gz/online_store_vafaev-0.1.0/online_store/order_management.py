class OrderManager:
    def __init__(self):
        self.orders_data = {}

    def create_order(self, order_id, order_data):
        try:
            self.orders_data.setdefault(order_id, order_data)
            print(f'Заказ с ID {order_id} добавлен')

        except KeyError:
            print(f'Заказ с ID {order_id} уже существует')

    def update_order(self, order_id, order_data):
        try:
            self.orders_data[order_id].update(order_data)
            print(f'Данные заказ с ID {order_id} обновлены')
        except KeyError:
            print(f'Заказ с ID {order_id} не найден')

    def cancel_order(self, order_id):
        try:
            self.orders_data.pop(order_id)
            print(f'Заказ с ID {order_id} отменён')
        except KeyError:
            print(f'Заказ с ID {order_id} не найден')
