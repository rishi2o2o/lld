from product import Product
from warehouse import Warehouse

class StockItem:
    def __init__(self, product: Product, warehouse: Warehouse, reorder_threshold: int = 10):
        self.product = product
        self.warehouse = warehouse
        self.quantity = 0
        self.reorder_threshold = reorder_threshold

    def add_stock(self, qty: int):
        self.quantity += qty

    def remove_stock(self, qty: int):
        if qty > self.quantity:
            raise Exception("Not enough stock available")

        self.quantity -= qty

    def is_low_stock(self):
        return self.quantity <= self.reorder_threshold

    def __repr__(self):
        return (
            f"StockItem(product={self.product.name}, "
            f"warehouse={self.warehouse.name}, "
            f"quantity={self.quantity})"
        )


