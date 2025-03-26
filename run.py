from src.gui.main import InventoryGUI, tk
from src.models.inventory import Inventory

if __name__ == "__main__":
    root = tk.Tk()
    inventory = Inventory()
    app = InventoryGUI(root, inventory)
    root.mainloop()