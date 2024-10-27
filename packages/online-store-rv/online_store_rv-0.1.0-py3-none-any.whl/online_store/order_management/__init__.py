class OrderManager:
    def __init__(self):

        self.order_dict = {}

    def create_order(self, order_id, order_data):

        if order_id in self.order_dict.keys():
            print(f'Заказ с ID {order_id} обновлен')
        else:
            self.order_dict[order_id] = order_data
            print(f'заказ с ID {order_id} добавлен')

    def update_order(self, order_id, order_data):


        if order_id not in self.order_dict.keys():
            print(f'Заказ с ID {order_id} не найден')
        else:
            self.order_dict[order_id] = order_data
            print(f'Данные заказа с ID {order_id} обновлены')

    def cancel_order(self, order_id):

        if order_id in self.order_dict.keys():
            del self.order_dict[order_id]
            print(f'Заказ с ID <{order_id}> отменён')
        else:
            print(f'Заказ с ID <{order_id}> не найден')