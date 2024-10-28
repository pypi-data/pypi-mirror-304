# Создай экземпляр класса управления учётными записями клиентов
from my_project.user_management import UserManager
from my_project.order_management import OrderManager
user_manager = UserManager()

# Создай экземпляр класса управления заказами
order_manager = OrderManager()


def main_menu():
    """
    Главное меню для выбора между управлением учётными записями и заказами.
    """
    while True:
        print('\nВыберите действие:')
        print('1. Управление учётными записями')
        print('2. Управление заказами')
        print('3. Выход')

        choice = input('Введите номер действия: ')

        if choice == '1':
            user_menu()
        elif choice == '2':
            order_menu()
        elif choice == '3':
            print('Работа завершена.')
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


def user_menu():
    """
    Меню для управления учётными записями клиентов.
    """
    while True:
        print('\nУправление учётными записями клиентов:')
        print('1. Добавить учётную запись')
        print('2. Найти учётную запись')
        print('3. Удалить учётную запись')
        print('4. Назад')

        choice = input('Выберите действие: ')

        if choice == '1':
            user_id = input('Введите email клиента: ')
            name = input('Введите имя: ')
            age = int(input('Введите возраст: '))
            # Вызов метода добавления учётной записи клиента
            user_manager.add_user(user_id, {'name': name, 'age': age})
            print(f'Учётная запись для {name} добавлена.')
        elif choice == '2':
            user_id = input('Введите email клиента: ')
            # Вызов метода поиска учётной записи клиента
            user = user_manager.find_user(user_id)
            if user:
                print(f'Найден клиент: {user}')
            else:
                print(f'Клиент с email {user_id} не найден.')
        elif choice == '3':
            user_id = input('Введите email клиента: ')
            # Вызов метода удаления учётной записи клиента
            user_manager.remove_user(user_id)
            print(f'Учётная запись с email {user_id} удалена.')
        elif choice == '4':
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


def order_menu():
    """
    Меню для управления заказами.
    """
    while True:
        print('\nУправление заказами:')
        print('1. Создать заказ')
        print('2. Обновить заказ')
        print('3. Отменить заказ')
        print('4. Назад')

        choice = input('Выберите действие: ')

        if choice == '1':
            order_id = input('Введите ID заказа: ')
            user = input('Введите учётную запись клиента: ')
            item = input('Введите товар: ')
            price = float(input('Введите цену: '))
            # Вызов метода создания заказа
            order_manager.create_order(order_id, {'user': user, 'item': item, 'price': price})
            print(f'Заказ {order_id} для клиента {user} создан.')
        elif choice == '2':
            order_id = input('Введите ID заказа: ')
            status = input('Введите новый статус: ')
            # Вызов метода обновления заказа
            order_manager.update_order(order_id, {'status': status})
            print(f'Заказ {order_id} обновлён со статусом: {status}.')
        elif choice == '3':
            order_id = input('Введите ID заказа: ')
            # Вызов метода отмены заказа
            order_manager.cancel_order(order_id)
            print(f'Заказ {order_id} отменён.')
        elif choice == '4':
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


if __name__ == '__main__':
    main_menu()
