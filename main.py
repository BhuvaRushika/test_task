import tkinter as tk
from tkinter import messagebox, ttk
from inventory import Inventory, ProductFactory, Category

class InventoryGUI:
    """
    GUI for managing the inventory with category filtering.
    """
    def __init__(self, root: tk.Tk, inventory: Inventory):
        self.root = root
        self.inventory = inventory
        self.root.title("Inventory Management System")
        self.categories = [Category("Electronics", "Devices"), Category("Books", "Literature")]
        self.current_filter = None 
        self.setup_gui()

    def setup_gui(self):
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.tree = ttk.Treeview(list_frame, columns=("SKU", "Name", "Price", "Category", "Quantity"), show="headings")
        self.tree.heading("SKU", text="SKU")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.pack(fill="both", expand=True)
        self.refresh_list()

        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=1, column=0, sticky="nsew")

        ttk.Label(input_frame, text="SKU:").grid(row=0, column=0)
        self.sku_entry = ttk.Entry(input_frame)
        self.sku_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="Name:").grid(row=1, column=0)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=1, column=1)

        ttk.Label(input_frame, text="Price:").grid(row=2, column=0)
        self.price_entry = ttk.Entry(input_frame)
        self.price_entry.grid(row=2, column=1)

        ttk.Label(input_frame, text="Category:").grid(row=3, column=0)
        self.category_combo = ttk.Combobox(input_frame, values=[cat.name for cat in self.categories])
        self.category_combo.grid(row=3, column=1)
        self.category_combo.set(self.categories[0].name)

        ttk.Label(input_frame, text="Quantity:").grid(row=4, column=0)
        self.quantity_entry = ttk.Entry(input_frame)
        self.quantity_entry.grid(row=4, column=1)
        
        ttk.Button(input_frame, text="Add Product", command=self.add_product).grid(row=5, column=0, pady=5)
        ttk.Button(input_frame, text="Remove Product", command=self.remove_product).grid(row=5, column=1, pady=5)
        ttk.Button(input_frame, text="Update Quantity", command=self.update_quantity).grid(row=6, column=0, pady=5)
        ttk.Button(input_frame, text="Update Price", command=self.update_price).grid(row=6, column=1, pady=5)
        filter_frame = ttk.Frame(self.root, padding="10")
        filter_frame.grid(row=1, column=1, sticky="nsew")

        ttk.Label(filter_frame, text="Filter by Category:").grid(row=0, column=0)
        self.filter_combo = ttk.Combobox(filter_frame, values=["All"] + [cat.name for cat in self.categories])
        self.filter_combo.grid(row=0, column=1)
        self.filter_combo.set("All")

        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=1, column=0, columnspan=2, pady=5)

    def refresh_list(self):
        """
        Refreshes the product list based on the current filter.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.current_filter is None:
            products = self.inventory.get_all_products()
        else:
            products = self.inventory.get_products_by_category(self.current_filter)
        
        for product in products:
            self.tree.insert("", "end", values=(product.sku, product.name, product.price, product.category.name, product.quantity))

    def apply_filter(self):
        """
        Applies the category filter and refreshes the list.
        """
        filter_value = self.filter_combo.get()
        if filter_value == "All":
            self.current_filter = None
        else:
            self.current_filter = next(cat for cat in self.categories if cat.name == filter_value)
        self.refresh_list()

    def add_product(self):
        sku = self.sku_entry.get().strip()
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        category_name = self.category_combo.get()
        quantity_str = self.quantity_entry.get().strip()

        if not sku:
            messagebox.showerror("Error", "SKU cannot be empty")
            return
        if sku.isdigit():
            messagebox.showerror("Error", "SKU must be a string")
            return
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if not price_str or not price_str.replace('.', '', 1).isdigit() or float(price_str) < 0:
            messagebox.showerror("Error", "Price must be a non-negative number")
            return
        if not quantity_str or not quantity_str.isdigit() or int(quantity_str) < 0:
            messagebox.showerror("Error", "Quantity must be a non-negative integer")
            return

        price = float(price_str)
        quantity = int(quantity_str)
        category = next(cat for cat in self.categories if cat.name == category_name)

        product = ProductFactory.create_product(sku, name, price, category, quantity)
        if product.sku in [p.sku for p in self.inventory.get_all_products()]:
            messagebox.showerror("Error", f"Product with SKU {sku} already exists")
            return

        self.inventory.add_product(product)
        self.refresh_list()
        self.clear_entries()

    def remove_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to remove")
            return

        sku = self.tree.item(selected[0])["values"][0]
        if sku not in [p.sku for p in self.inventory.get_all_products()]:
            messagebox.showerror("Error", f"Product with SKU {sku} not found")
            return

        self.inventory.remove_product(sku)
        self.refresh_list()

    def update_quantity(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to update")
            return

        sku = self.tree.item(selected[0])["values"][0]
        quantity_str = self.quantity_entry.get().strip()

        if not quantity_str or not quantity_str.isdigit() or int(quantity_str) < 0:
            messagebox.showerror("Error", "Quantity must be a non-negative integer")
            return

        new_quantity = int(quantity_str)
        product = self.inventory.get_product(sku)
        product.update_quantity(new_quantity)
        self.refresh_list()
        self.clear_entries()

    def update_price(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to update")
            return

        sku = self.tree.item(selected[0])["values"][0]
        price_str = self.price_entry.get().strip()

        if not price_str or not price_str.replace('.', '', 1).isdigit() or float(price_str) < 0:
            messagebox.showerror("Error", "Price must be a non-negative number")
            return

        new_price = float(price_str)
        product = self.inventory.get_product(sku)
        product.update_price(new_price)
        self.refresh_list()
        self.clear_entries()

    def clear_entries(self):
        self.sku_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    inventory = Inventory()
    app = InventoryGUI(root, inventory)
    root.mainloop()