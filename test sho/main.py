import tkinter as tk
from tkinter import ttk, messagebox


class Add_product:
    products = []

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_product(self):
        Add_product.products.append(self)
        return f"Product Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def delete_product(self):
        Add_product.products.remove(self)
        return f"Product {self.name} has been deleted."

    def show_products(self):
        if not Add_product.products:
            return "No products available."
        product_list = []
        for product in Add_product.products:
            product_list.append(f"Product Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")
        return "\n".join(product_list)


class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("учетник")
        self.root.geometry("710x450")
        self.root.resizable(False, False)

        
        form = ttk.LabelFrame(root, text="Добавить товар", padding=10)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Название:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Цена:").grid(row=0, column=2, sticky="w")
        self.price_entry = ttk.Entry(form, width=10)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Количество:").grid(row=0, column=4, sticky="w")
        self.qty_entry = ttk.Entry(form, width=10)
        self.qty_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(form, text="Добавить", command=self.add_product).grid(row=0, column=6, padx=10)
        ttk.Button(form, text="Удалить выбранный", command=self.delete_product).grid(row=1, column=6, padx=10)

        
        self.root.bind("<Return>", lambda event: self.add_product())

   
        table_frame = ttk.LabelFrame(root, text="Список товаров", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("name", "price", "quantity", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("name", text="Название")
        self.tree.heading("price", text="Цена")
        self.tree.heading("quantity", text="Количество")
        self.tree.heading("total", text="Сумма")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("price", width=100, anchor="center")
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("total", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    
        self.tree.bind("<Double-1>", self.edit_quantity)

        bottom = ttk.Frame(root, padding=10)
        bottom.pack(fill="x")

        self.total_label = ttk.Label(bottom, text="Товаров: 0    Общая сумма: 0", font=("Arial", 11, "bold"))
        self.total_label.pack(side="left")

        ttk.Button(bottom, text="Очистить всё", command=self.clear_all).pack(side="right")


    def add_product(self):
        name = self.name_entry.get().strip()
        price_text = self.price_entry.get().strip()
        qty_text = self.qty_entry.get().strip()

        if not name:
            messagebox.showwarning("Ошибка", "Введите название товара!")
            return

        try:
            price = float(price_text)
            quantity = int(qty_text)
            if price < 0 or quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка", "Цена и количество должны быть положительными числами!")
            return

        product = Add_product(name, price, quantity)
        product.add_product()

        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.name_entry.focus()

        self.refresh_table()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите товар в таблице!")
            return

        index = self.tree.index(selected[0])
        product = Add_product.products[index]
        product.delete_product()
        self.refresh_table()

    def edit_quantity(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        product = Add_product.products[index]

        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить количество")
        dialog.geometry("250x120")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=f"{product.name} — новое количество:").pack(pady=5)
        entry = ttk.Entry(dialog, width=10)
        entry.insert(0, str(product.quantity))
        entry.pack(pady=5)
        entry.focus()
        entry.select_range(0, tk.END)

        def save():
            try:
                new_qty = int(entry.get())
                if new_qty < 0:
                    raise ValueError
                product.quantity = new_qty
                dialog.destroy()
                self.refresh_table()
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите целое неотрицательное число!", parent=dialog)

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=5)

    def clear_all(self):
        if not Add_product.products:
            return
        if messagebox.askyesno("Подтверждение", "Удалить все товары?"):
            Add_product.products.clear()
            self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        total_sum = 0
        for product in Add_product.products:
            total = product.price * product.quantity
            total_sum += total
            self.tree.insert("", "end", values=(product.name, f"{product.price:.2f}", product.quantity, f"{total:.2f}"))

        self.total_label.config(
            text=f"Товаров: {len(Add_product.products)}    Общая сумма: {total_sum:.2f}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()