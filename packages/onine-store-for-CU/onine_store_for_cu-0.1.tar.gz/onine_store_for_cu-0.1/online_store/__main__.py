from online_store import UserManager, OrderManager

user_manager = UserManager()
order_manager = OrderManager()


def user_menu():
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
        user_manager.add_user(user_id = user_id, user_data= {'name': name, 'age': age})

    elif choice == '2':
        user_id = input('Введите email клиента: ')
        user_manager.find_user(user_id = user_id)
    elif choice == '3':
        user_id = input('Введите email клиента: ')
        user_manager.remove_user(user_id=user_id)
    elif choice == '4':
        return
    else:
        print('Некорректный ввод.')

def order_menu():
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
       order_manager.create_order(order_id=order_id, order_data={'user': user, 'item': item, 'price': price})
    elif choice == '2':
       order_id = input('Введите ID заказа: ')
       status = input('Введите статус: ')
       order_manager.update_order(order_id=order_id, order_data=status)
    elif choice == '3':
        order_id = input('Введите ID заказа: ')
        order_manager.cancel_order(order_id=order_id)
    elif choice == '4':
       return
    else:
       print('Некорректный ввод.')

def main_menu():
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

if __name__ == '__main__':
    main_menu()