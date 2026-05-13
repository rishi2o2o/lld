from stock_item import StockItem

class AlertService:
    def notify_low_stock(self, stock_item: StockItem):
        print(
            f"[ALERT] Low stock for {stock_item.product.name} "
            f"in {stock_item.warehouse.name}. "
            f"Remaining = {stock_item.quantity}"
        )

