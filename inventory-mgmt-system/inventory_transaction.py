from enum import Enum
from datetime import datetime
from typing import Optional
from product import Product
from warehouse import Warehouse

class TransactionType(Enum):
    STOCK_IN = "STOCK_IN"
    STOCK_OUT = "STOCK_OUT"
    TRANSFER = "TRANSFER"


class InventoryTransaction:
    def __init__(self,
        transaction_type: TransactionType,
        product: Product,
        quantity: int,
        source_warehouse: Optional[Warehouse],
        destination_warehouse: Optional[Warehouse]
    ):

        self.transaction_type = transaction_type
        self.product = product
        self.quantity = quantity
        self.source_warehouse = source_warehouse
        self.destination_warehouse = destination_warehouse
        self.timestamp = datetime.now()

    def __repr__(self):
        return (
            f"{self.transaction_type.value} | "
            f"{self.product.name} | "
            f"{getattr(self.source_warehouse, "name", None)} | "
            f"{getattr(self.destination_warehouse, "name", None)} | "
            f"qty={self.quantity} | "
            f"time={self.timestamp}"
        )


