from enum import Enum

class Categ(Enum):
    Electronics = "Electronics"
    Gadgets = "Gadgets"
    Tools = "Tools"
    Apparel = "Apparel"
    Accessories = "Accessories"
    Books = "Books"
    Toys = "Toys"
    Furniture = "Furniture"


class Products:
    products_db = {}
    #*******************************************
    @classmethod
    def load_products_from_file(cls):
        with open("product.txt", "r") as f:
            for line in f:
                parts = line.strip().split(";")
                product_id = parts[0]
                product_name = parts[1]
                category = parts[2]
                price = float(parts[3])
                inventory = int(parts[4])
                supplier = parts[5]
                on_offer = bool(int(parts[6]))
                offer_price = float(parts[7])
                valid_until = parts[8]
                if category not in cls.products_db:
                    cls.products_db[category] = {}

                cls.products_db[category][product_id] = {
                    'name': product_name,
                    'price': price,
                    'inventory': inventory,
                    'supplier': supplier,
                    "on_offer": on_offer,
                    "offer_price": offer_price,
                    "valid_until": valid_until
                }
                print(f"Added product {product_name} with ID {product_id} under category {category}")
        print(f"Loaded {len(cls.products_db)} categories and {sum([len(products) for products in cls.products_db.values()])} products.")
        print(Products.products_db)
    #**************************************************************************************
    @classmethod
    def display_product_details(cls, product_id):
        product = cls.get_product_by_id(product_id)
        if product:
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            if product['on_offer']:
                print(f"Special Offer Price: ${product['offer_price']:.2f} (Valid until {product['valid_until']})")
            print(f"Inventory: {product['inventory']}")
            print(f"Supplier: {product['supplier']}")
    #******************************************************************************
    @classmethod
    def consistency_check(cls):
        from users import Users
        for user_id, user_data in Users.shoppers.items():
            basket = user_data.get('Basket', {})
            for product_id in list(basket.keys()):
                product_found = False
                for category, products in cls.products_db.items():
                    if str(product_id) in products:
                        product_found = True
                        break
                if not product_found:
                    print(f"WARNING: Product {product_id} in user {user_id}'s basket not found in the main product database. Removing it from the basket.")
                    del basket[product_id]
    #********************************************************
    @classmethod
    def get_product_by_id(cls, product_id):
        product_id_str = str(product_id)
        for category, products in cls.products_db.items():
            if product_id_str in products:
                return products[product_id_str]
        return None
    #*********************************************************