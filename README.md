# Simple E-commerce Inventory Management

A Python-based inventory management system with a GUI for a small e-commerce store.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd testdemo
   ```

2. Install dependencies: 
Ensure Python 3.6+ is installed
```
pip install -r requirements.txt
```
Note: tkinter is included with Python; only pytest is needed.

3. Run the Application: 
```python run.py```

4. Run tests: 
```pytest tests/test_inventory.py -v```


## Quick Setup and Test
- GUI:
1. Run python run.py to launch the GUI.
2. Add a test product:
    ``` SKU: "ABC123"
    Name: "Test Product"
    Price: "10.99"
    Category: "Electronics"
    Quantity: "5" ```
3. Verify the product appears in the table and test filtering by category

- CLI:
1. Run the CLI:
    ```python cli.py```
2. Test adding a product:
    - Type add 
    - Enter SKU: "XYZ789", Enter Name: "Test Book", Enter Price: "5.99", Enter Category (Electronics/Books): "Books", Enter Quantity: "10"
3. List products: 
    - Type list to see all products.
4. Exit:
    - Type exit


## Features
Add, remove, update product quantities, and update prices via a GUI.
View all products in a table format.
Categories: Electronics and Books (hardcoded for simplicity).


## Design Decisions
**OOP**: Separated core logic and GUI for modularity.
**Design Pattern**: Factory pattern via ProductFactory for product creation.
**GUI**: Built with tkinter using a Treeview for product display and entry fields for management.
**CLI**: Simple script for command-line testing without a web server.
**Error Handling**: Explicit validation in GUI layer; no try-except. Core logic uses ValueError for invalid states.

## Testing Strategy
Unit tests cover model creation, inventory operations, and edge cases.
Focused on inventory.py to ensure core logic is robust.
Used pytest for testing framework