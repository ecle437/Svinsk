import tkinter as tk
from tkinter import ttk, messagebox

# --- ОБНОВЛЕННОЕ МЕНЮ И ДАННЫЕ ---

MENU = {
    1: {"name": "Бургер классический", "price": 7.00},
    2: {"name": "Бургер острый", "price": 7.50},
    3: {"name": "Картошка фри", "price": 3.50},
    4: {"name": "Кола", "price": 2.00},
    5: {"name": "Соус сырный", "price": 1.00},
    6: {"name": "Сосиска в тесте", "price": 4.50}  # ДОБАВИЛИ СОСИСКУ В ТЕСТЕ 🌭
}

current_budget = 10000000.00  # Личный бюджет на покупки
total_cafe_sales = 0.00  # Общая касса (выручка кафе)
order_counter = 0  # Счетчик чеков
cart_items = []  # Список ID блюд в текущей корзине


def calculate_total(cart_items, promo_code=None):
    """Считает итог с учетом промокода TEEN10 (-10%)"""
    if not cart_items:
        return 0.00

    total = sum(MENU[item_id]["price"] for item_id in cart_items if item_id in MENU)

    if promo_code:
        clean_code = str(promo_code).strip().upper()
        if clean_code == "TEEN10":
            total = total * 0.9  # Скидка 10%

    return round(total, 2)


# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ---

def update_ui():
    """Обновляет все тексты, списки и балансы в окне"""
    promo = promo_entry.get()
    total_cost = calculate_total(cart_items, promo_code=promo)

    # Расчет остатка личного бюджета
    projected_budget = current_budget - total_cost

    # Обновление списка товаров в корзине
    cart_box.delete(0, tk.END)
    for item_id in cart_items:
        cart_box.insert(tk.END, f"• {MENU[item_id]['name']} — {MENU[item_id]['price']:.2f} руб.")

    # Обновление финансовых лейблов
    lbl_total.config(text=f"Итого к оплате: {total_cost:.2f} руб.")
    lbl_budget.config(text=f"Ваш личный бюджет: {projected_budget:,.2f} руб.".replace(",", " "))
    lbl_cafe_sales.config(text=f"💰 Касса кафе (Выручка): {total_cafe_sales:,.2f} руб.".replace(",", " "))


def add_to_cart():
    """Добавляет блюдо в корзину"""
    selected_text = menu_combobox.get()
    if not selected_text:
        return

    try:
        item_id = int(selected_text.split("."))
        cart_items.append(item_id)
        update_ui()
    except ValueError:
        messagebox.showerror("Ошибка", "Не удалось определить блюдо")


def clear_cart():
    """Очищает текущую корзину"""
    cart_items.clear()
    update_ui()


def checkout():
    """Покупка: списывает личный бюджет, добавляет деньги в кассу кафе"""
    global current_budget, total_cafe_sales, order_counter

    if not cart_items:
        messagebox.showwarning("Внимание", "Добавьте блюда в корзину перед покупкой.")
        return

    promo = promo_entry.get()
    total_cost = calculate_total(cart_items, promo_code=promo)

    if total_cost > current_budget:
        messagebox.showerror("Ошибка", "Недостаточно денег в личном бюджете!")
        return

    # Фиксируем сделку
    current_budget -= total_cost  # Снимаем у покупателя
    total_cafe_sales += total_cost  # Добавляем в общую кассу кафе
    order_counter += 1  # Номер чека

    # Добавляем запись в историю заказов (Кассу)
    history_box.insert(tk.END, f"Заказ #{order_counter}: +{total_cost:.2f} руб. ({len(cart_items)} шт.)")
    history_box.see(tk.END)  # Автопрокрутка вниз

    # Сброс корзины
    cart_items.clear()
    promo_entry.delete(0, tk.END)

    update_ui()
    messagebox.showinfo("Касса", f"Заказ #{order_counter} успешно оплачен!\nСумма: {total_cost:.2f} руб.")


# Создание главного окна
root = tk.Tk()
root.title("Касса Кафе & Финансовый трекер")
root.geometry("500x680")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 10, "bold"))

# Блок 1: Панель бюджетов
top_frame = tk.LabelFrame(root, text=" Финансы ", font=("Arial", 10, "bold"), padx=10, pady=10)
top_frame.pack(fill="x", padx=15, pady=10)

lbl_budget = ttk.Label(top_frame, text="", font=("Arial", 11, "bold"), foreground="#2980b9")
lbl_budget.pack(anchor="w")

lbl_cafe_sales = ttk.Label(top_frame, text="", font=("Arial", 12, "bold"), foreground="#27ae60")
lbl_cafe_sales.pack(anchor="w", pady=(5, 0))

# Блок 2: Выбор блюд
menu_frame = tk.LabelFrame(root, text=" Выберите блюдо ", font=("Arial", 10, "bold"), padx=10, pady=10)
menu_frame.pack(fill="x", padx=15, pady=5)

menu_options = [f"{item_id}. {info['name']} ({info['price']:.2f} руб.)" for item_id, info in MENU.items()]
menu_combobox = ttk.Combobox(menu_frame, values=menu_options, state="readonly", font=("Arial", 10), width=35)
menu_combobox.pack(side="left", padx=5)
menu_combobox.current(0)

btn_add = ttk.Button(menu_frame, text="Добавить", command=add_to_cart)
btn_add.pack(side="right", padx=5)

# Блок 3: Списки (Корзина слева, История кассы справа)
lists_frame = tk.Frame(root)
lists_frame.pack(fill="both", expand=True, padx=15, pady=5)

# Текущая корзина
f_cart = tk.LabelFrame(lists_frame, text=" Текущая корзина ", font=("Arial", 9, "bold"), padx=5, pady=5)
f_cart.pack(side="left", fill="both", expand=True, padx=(0, 5))
cart_box = tk.Listbox(f_cart, font=("Arial", 9), height=10)
cart_box.pack(fill="both", expand=True)

# Журнал кассы (Куда суммируются заказы)
f_history = tk.LabelFrame(lists_frame, text=" История кассы (Заказы) ", font=("Arial", 9, "bold"), padx=5, pady=5)
f_history.pack(side="right", fill="both", expand=True, padx=(5, 0))
history_box = tk.Listbox(f_history, font=("Arial", 9), height=10, fg="#2c3e50")
history_box.pack(fill="both", expand=True)

# Блок 4: Управление и промокод
bottom_frame = tk.Frame(root, padx=15, pady=5)
bottom_frame.pack(fill="x")

lbl_promo = ttk.Label(bottom_frame, text="Промокод:")
lbl_promo.pack(side="left")

promo_entry = ttk.Entry(bottom_frame, width=12, font=("Arial", 10))
promo_entry.pack(side="left", padx=5)
promo_entry.bind("<KeyRelease>", lambda event: update_ui())

btn_clear = ttk.Button(bottom_frame, text="Очистить корзину", command=clear_cart)
btn_clear.pack(side="right")

# Итоговая цена текущего заказа
lbl_total = tk.Label(root, text="", font=("Arial", 13, "bold"), fg="#16a085", anchor="e", padx=20, pady=5)
lbl_total.pack(fill="x")

# Кнопка Оплатить / Купить
btn_checkout = tk.Button(
    root,
    text="🛒 ОФОРМИТЬ И ОПЛАТИТЬ ЗАКАЗ",
    font=("Arial", 12, "bold"),
    bg="#2ecc71",
    fg="white",
    activebackground="#27ae60",
    activeforeground="white",
    relief="groove",
    pady=12,
    command=checkout
)
btn_checkout.pack(fill="x", padx=15, pady=15)

# Запуск приложения
update_ui()
root.mainloop()
