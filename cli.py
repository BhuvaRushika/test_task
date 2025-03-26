from src.models.inventory import Inventory, ProductFactory, Category

def main():
    inventory = Inventory()
    categories = {
        "Electronics": Category("Electronics", "Devices"),
        "Books": Category("Books", "Literature")
    }
    
    print("Simple Inventory CLI")
    print("Commands: add, list, exit")
    
    while True:
        command = input("> ").strip().lower()
        
        if command == "exit":
            print("Exiting...")
            break
        elif command == "add":
            sku = input("Enter SKU: ")
            name = input("Enter Name: ")
            price = float(input("Enter Price: "))
            category_name = input("Enter Category (Electronics/Books): ")
            quantity = int(input("Enter Quantity: "))
            
            if category_name not in categories:
                print("Error: Invalid category. Use 'Electronics' or 'Books'.")
                continue
            
            try:
                product = ProductFactory.create_product(
                    sku, name, price, categories[category_name], quantity
                )
                inventory.add_product(product)
                print(f"Added: {product}")
            except ValueError as e:
                print(f"Error: {e}")
        elif command == "list":
            products = inventory.get_all_products()
            if not products:
                print("No products in inventory.")
            else:
                for p in products:
                    print(p)
        else:
            print("Unknown command. Use: add, list, exit")

if __name__ == "__main__":
    main()