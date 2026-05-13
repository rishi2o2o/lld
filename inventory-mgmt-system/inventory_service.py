from alert_service import AlertService
from stock_item import StockItem
from inventory_transaction import TransactionType, InventoryTransaction

class InventoryService:
    def __init__(self):
        self.stock_items = {}  # (product_id, warehouse_id) -> stock_item
        self.transactions = []
        self.alert_service = AlertService()

    def _get_stock_item_key(self, product, warehouse):
        return (product.product_id, warehouse.warehouse_id)


    def _get_or_create_stock_item(self,product, warehouse) -> StockItem:

        key = self._get_stock_item_key(product, warehouse)

        if key not in self.stock_items:
            self.stock_items[key] = StockItem(product, warehouse)

        return self.stock_items[key]


    def add_stock(self, product, warehouse, qty):

        print(f"Adding {qty} {product.name} to {warehouse.name}")

        stock_item = self._get_or_create_stock_item(product, warehouse)
        stock_item.add_stock(qty)

        transaction = InventoryTransaction(
            TransactionType.STOCK_IN,
            product,
            qty,
            source_warehouse=None,
            destination_warehouse=warehouse
        )

        self.transactions.append(transaction)


    def remove_stock(self, product, warehouse, qty: int):

        print(f"Removing {qty} {product.name} from {warehouse.name}")

        stock_item = self._get_or_create_stock_item(product, warehouse)
        stock_item.remove_stock(qty)

        transaction = InventoryTransaction(
            TransactionType.STOCK_OUT,
            product,
            qty,
            source_warehouse=warehouse,
            destination_warehouse=None,
        )

        self.transactions.append(transaction)

        if stock_item.is_low_stock():
            self.alert_service.notify_low_stock(stock_item)


    def transfer_stock(self, product, source_warehouse, destination_warehouse, qty):

        print(f"Transferring {qty} {product.name} from {source_warehouse.name} to {destination_warehouse.name}")

        source_stock = self._get_or_create_stock_item(product, source_warehouse)
        destination_stock = self._get_or_create_stock_item(product, destination_warehouse)

        source_stock.remove_stock(qty)
        destination_stock.add_stock(qty)

        transaction = InventoryTransaction(
            TransactionType.TRANSFER,
            product,
            qty,
            source_warehouse,
            destination_warehouse
        )

        self.transactions.append(transaction)

        if source_stock.is_low_stock():
            self.alert_service.notify_low_stock(source_stock)


    def print_inventory(self):
        print("\n--- INVENTORY ---")

        for stock_item in self.stock_items.values():
            print(stock_item)

    def print_transactions(self):
        print("\n--- TRANSACTIONS ---")

        for txn in self.transactions:
            print(txn)


