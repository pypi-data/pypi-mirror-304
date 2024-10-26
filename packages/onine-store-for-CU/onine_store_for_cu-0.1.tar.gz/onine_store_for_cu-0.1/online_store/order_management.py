class OrderManager:
    def __init__(self):
        self.OrderManager = {}

    def create_order(self, order_id, order_data):
        if order_id in self.OrderManager:
            print(f'Заказ с ID {order_id} уже существует')
        else:
            print(f'Заказ с ID {order_id} добавлен')
            self.OrderManager[order_id] = order_data

    def update_order(self, order_id, order_data):
        if order_id in self.OrderManager:
            for item in order_data:
                self.OrderManager[order_id][item] = order_data[item]
            print(f'Заказ с ID {order_id} обновлен')
        else:
            print(f'Заказ с ID {order_id} не найден')

    def cancel_order(self, order_id):
        if order_id in self.OrderManager:
            self.OrderManager.pop(order_id)
            print(f'Клиент с ID {order_id} отменен')
        else:
            print(f'Клиент с ID {order_id} не найден')