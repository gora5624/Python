from flask import render_template, request

sellers = [
    {},
    {},
    {},
    {},
]

def get_orders():
    # Обработка фильтров и получение заказов из базы данных
    # ...

    return render_template('orders.html')#, orders=orders)