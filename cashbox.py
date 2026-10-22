import tkinter as tk
from tkinter import ttk, messagebox


MENU = {
    1: {"name": "Бургер классический", "price": 7.00},
    2: {"name": "Бургер острый", "price": 7.50},
    3: {"name": "Картошка фри", "price": 3.50},
    4: {"name": "Кола", "price": 2.00},
    5: {"name": "Соус сырный", "price": 1.00}
}


current_budget = 10000000.00
cart_items = []


def calculate_total(cart_items, promo_code=None):

    if not cart_items:
        return 0.00

    total = sum(MENU[item_id]["price"] for item_id in cart_items if item_id in MENU)

    if promo_code:
        clean_code = str(promo_code).strip().upper()
        if clean_code == "TEEN10":
            total = total * 0.9

    return round(total, 2)




def update_ui():
    promo = promo_entry.get()
    total_cost = calculate_total(cart_items, promo_code=promo)

    projected_budget = current_budget - total_cost

    cart_box.delete(0, tk.END)
    for item_id in cart_items:
        cart_box.insert(tk.END, f"• {MENU[item_id]['name']} — {MENU[item_id]['price']:.2f} руб.")

    lbl_total.config(text=f"Итого к оплате: {total_cost:.2f} руб.")
    lbl_budget.config(text=f"Текущий бюджет: {projected_budget:,.2f} руб.".replace(",", " "))


def add_to_cart():
    selected_text = menu_combobox.get()
    if not selected_text:
        return

    try:
        item_id = int(selected_text.split(".")[0])
        cart_items.append(item_id)
        update_ui()
    except ValueError:
        messagebox.showerror("Ошибка", "Не удалось определить блюдо")


def clear_cart():

    cart_items.clear()
    update_ui()


def checkout():

    global current_budget

    if not cart_items:
        messagebox.showwarning("Внимание", "Ваша корзина пуста! Добавьте блюда перед покупкой.")
        return

    promo = promo_entry.get()
    total_cost = calculate_total(cart_items, promo_code=promo)

    if total_cost > current_budget:
        messagebox.showerror("Ошибка", "Недостаточно средств в бюджете проекта!")
        return


    current_budget -= total_cost
    cart_items.clear()
    promo_entry.delete(0, tk.END)

    update_ui()
    messagebox.showinfo("Успех", f"Покупка совершена успешно!\nСписано: {total_cost:.2f} руб.\nНовый баланс обновлен.")



root = tk.Tk()
root.title("Бацькi")
root.geometry("450x600")
root.resizable(False, False)


style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 10, "bold"))


top_frame = tk.LabelFrame(root, text=" Финансовый трекер проекта ", font=("Arial", 10, "bold"), padx=10, pady=10)
top_frame.pack(fill="x", padx=15, pady=10)

lbl_budget = ttk.Label(top_frame, text="", font=("Arial", 12, "bold"), foreground="green")
lbl_budget.pack(anchor="w", pady=5)


menu_frame = tk.LabelFrame(root, text=" Меню ", font=("Arial", 10, "bold"), padx=10, pady=10)
menu_frame.pack(fill="x", padx=15, pady=5)

menu_options = [f"{item_id}. {info['name']} ({info['price']:.2f} руб.)" for item_id, info in MENU.items()]
menu_combobox = ttk.Combobox(menu_frame, values=menu_options, state="readonly", font=("Arial", 10), width=32)
menu_combobox.pack(side="left", padx=5)
menu_combobox.current(0)

btn_add = ttk.Button(menu_frame, text="Добавить", command=add_to_cart)
btn_add.pack(side="right", padx=5)


cart_frame = tk.LabelFrame(root, text=" Ваша корзина ", font=("Arial", 10, "bold"), padx=10, pady=10)
cart_frame.pack(fill="both", expand=True, padx=15, pady=5)

cart_box = tk.Listbox(cart_frame, font=("Arial", 10), height=8)
cart_box.pack(fill="both", expand=True, side="left", padx=5)

scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=cart_box.yview)
scrollbar.pack(side="right", fill="y")
cart_box.config(yscrollcommand=scrollbar.set)


bottom_frame = tk.Frame(root, padx=15, pady=5)
bottom_frame.pack(fill="x")

lbl_promo = ttk.Label(bottom_frame, text="Промокод:")
lbl_promo.pack(side="left")

promo_entry = ttk.Entry(bottom_frame, width=12, font=("Arial", 10))
promo_entry.pack(side="left", padx=5)
promo_entry.bind("<KeyRelease>", lambda event: update_ui())

btn_clear = ttk.Button(bottom_frame, text="Очистить всё", command=clear_cart)
btn_clear.pack(side="right")

lbl_total = tk.Label(root, text="", font=("Arial", 13, "bold"), fg="blue", anchor="e", padx=20, pady=5)
lbl_total.pack(fill="x")

btn_checkout = tk.Button(
    root,
    text="🛒 КУПИТЬ",
    font=("Arial", 14, "bold"),
    bg="#2ecc71",
    fg="white",
    activebackground="#27ae60",
    activeforeground="white",
    relief="groove",
    pady=10,
    command=checkout
)
btn_checkout.pack(fill="x", padx=15, pady=15)

update_ui()

root.mainloop()


