from typing import List, Optional

class Category:
    """
    Represents a product category.
    """
    def __init__(self, name: str, description: str):
        """
        Initializes a Category object with the given name and description.
        """
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """
        Returns a string representation of the category.
        """
        return f"{self.name}: {self.description}"

    def get_details(self) -> dict:
        """
        Returns a dictionary representation of the category.
        """
        return {"name": self.name, "description": self.description}


class Product:
    """
    product in the inventory.
    """
    def __init__(self, sku: str, name: str, price: float, category: Category, quantity: int):
        """
        Initializes a Product object with the given SKU, name, price, category, and quantity.
        """
        if not sku or not name or price < 0 or quantity < 0:
            raise ValueError("Invalid product data")
        self.sku = sku
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

    def __str__(self) -> str:
        """
        Return string representation of the product.
        """
        return f"{self.name} (SKU: {self.sku}) - ${self.price}, Qty: {self.quantity}"

    def get_details(self) -> dict:
        """
        Return a dictionary representation of the product.
        """
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "category": str(self.category),
            "quantity": self.quantity
        }

    def update_price(self, new_price: float) -> None:
        """
        Updates the price of the product.
        """
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def update_quantity(self, new_quantity: int) -> None:
        """
        Updates the quantity of the product.
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity


class ProductFactory:
    """
    Factory class to create Product instances.
    Design Pattern Choice: Factory - Centralizes product creation logic and ensures
    valid objects are instantiated with proper validation.
    """
    @staticmethod
    def create_product(sku: str, name: str, price: float, category: Category, quantity: int) -> Product:
        return Product(sku, name, price, category, quantity)


class Inventory:
    """
    Manages the collection of products.
    """
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product) -> None:
        """
        Adds a product to the inventory.
        """
        if product.sku in self.products:
            raise ValueError(f"Product with SKU {product.sku} already exists")
        self.products[product.sku] = product

    def remove_product(self, sku: str) -> None:
        """
        Removes a product from the inventory.
        """
        if sku not in self.products:
            raise ValueError(f"Product with SKU {sku} not found")
        del self.products[sku]

    def get_product(self, sku: str) -> Optional[Product]:
        """
        Retrieves a product from the inventory by SKU.
        """
        if sku not in self.products:
            raise ValueError(f"Product with SKU {sku} not found")
        return self.products[sku]

    def get_all_products(self) -> List[Product]:
        """
            Retrieves all products in the inventory.
        """
        return list(self.products.values())

    def get_products_by_category(self, category: Category) -> List[Product]:
        """
            Retrieves products in the inventory by category.
        """
        return [p for p in self.products.values() if p.category == category]
    