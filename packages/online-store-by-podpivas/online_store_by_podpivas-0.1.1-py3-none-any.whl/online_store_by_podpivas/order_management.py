class OrderManager:
    def __init__(self):
        # Добавь инициализацию атрибута — словаря для хранения заказов.
        self.orders = {}

    def create_order(self, order_id, order_data):
        #Проверяем, существует ли ID
        if order_id in self.orders:
            print(f'Заказ с ID {order_id} уже существует')
        else:
            #Создаем новый заказ
            self.orders[order_id] = order_data
            print(f'Заказ с ID {order_id} добавлен')

    def update_order(self, order_id, order_data):
        #Проверяем, существует ли ID
        if order_id in self.orders:
            #Обновляем данные заказа
            self.orders[order_id] = order_data
            print(f'Данные заказа с ID {order_id} обновлены')
        else:
            print(f'Заказ с ID {order_id} не найден')

    def cancel_order(self, order_id):
        #Проверяем, существует ли ID
        if order_id in self.orders:
            # Удаляем заказ из словаря
            self.orders.pop(order_id)
            print(f'Заказ с ID {order_id} отменён')
        else:
            print(f'Заказ с ID {order_id} не найден')

