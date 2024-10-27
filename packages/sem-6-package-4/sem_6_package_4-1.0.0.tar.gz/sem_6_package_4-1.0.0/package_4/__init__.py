def generate_check(order_data):
    customer_name = order_data['customer_name']
    items = order_data['items']

    check = f"Чек\n"
    check += f"Имя клиента: {customer_name}\n"
    check += "\n"
    check += "Товары:\n"
    total_price = 0
    for item in items:
        item_price = item['quantity'] * item['price']
        total_price += item_price
        check += f"{item['name']} x {item['quantity']} = {item_price} руб.\n"

    check += "\n"
    check += f"Итого: {total_price} руб."

    return check