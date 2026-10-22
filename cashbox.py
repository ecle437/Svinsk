# Меню из 5 позиций (раздел 2)
MENU = {
    1: {"name": "Бургер классический", "price": 7.00},
    2: {"name": "Бургер острый", "price": 7.50},
    3: {"name": "Картошка фри", "price": 3.50},
    4: {"name": "Кола", "price": 2.00},
    5: {"name": "Соус сырный", "price": 1.00}
}


def calculate_total(cart_items):
    """
    Принимает список ID блюд, например: [1, 1, 4]
    Возвращает итоговую сумму (float)
    """
    if not cart_items:
        return 0.00

    total = sum(MENU[item_id]["price"] for item_id in cart_items if item_id in MENU)
    return round(total, 2)