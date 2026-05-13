from product import Product
from warehouse import Warehouse
from inventory_service import InventoryService

if __name__ == "__main__":

    # products
    laptop = Product("P1", "MacBook Pro", "MBP-001")

    # warehouses
    bangalore = Warehouse("W1", "Bangalore Warehouse")
    mumbai = Warehouse("W2", "Mumbai Warehouse")

    # inventory service
    inventory_service = InventoryService()

    # add stock
    inventory_service.add_stock(laptop, bangalore, 50)

    # remove stock
    inventory_service.remove_stock(laptop, bangalore, 45)

    # transfer stock
    inventory_service.transfer_stock(laptop, bangalore, mumbai, 3)

    # print data
    inventory_service.print_inventory()
    inventory_service.print_transactions()



