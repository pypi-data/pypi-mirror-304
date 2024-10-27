class OrderManager:
    def __init__(self):
        self.orders = dict()
    def create_order(self, order_id, order_data):
        if order_id in self.orders:
            print("Заказ с ID "+str(order_id)+" уже существует")
        else:
            self.orders[order_id] = order_data
            print("Заказ с ID "+str(order_id)+" добавлен")

    def update_order(self, order_id, order_data):
        if order_id not in self.orders:
            print("Заказ с ID "+str(order_id)+" не найден")
        else:
            self.orders[order_id] = order_data
            print("Заказ с ID " + str(order_id) + " обновлен")

    def cancel_order(self, order_id):
        if order_id not in self.orders:
            print("Заказ с ID "+str(order_id)+" не найден")
        else:
            del self.orders[order_id]
            print("Заказ с ID " + str(order_id) + " удален")