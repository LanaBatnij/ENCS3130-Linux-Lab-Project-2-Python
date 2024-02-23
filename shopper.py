from admin import Admin
from users import Users
from product import Products

class Shopper(Users):

    def __init__(self, user_id):
        self.user_id = user_id
        self.basket = Users.shoppers.get(user_id, {}).get('Basket', {})
    #************************************
    @staticmethod
    def add_product_to_basket(user_id):
        # Load products first
        Products.products_db = Admin.load_products_from_file()
        selected_product_id = input("Enter the Product ID of the item you want to add to the basket: ").strip()
        selected_product = None
        for category, category_data in Products.products_db.items():
            if selected_product_id in category_data:
                selected_product = category_data[selected_product_id]
                break
        if not selected_product:
            print("Product not found!")
            return
            # Ask for quantity
        quantity = int(input(f"How many units of {selected_product['name']} would you like to add to the basket? "))
            # Check if enough stock exists
        if quantity > selected_product['inventory']:
            print("Sorry, there isn't enough stock available!")
            return
                #  Using a simpler approach to add product to the basket
        basket = Users.shoppers[user_id].setdefault('Basket', {})
        basket[selected_product_id] = basket.get(selected_product_id, 0) + quantity
            # If the user's basket doesn't already have this product, initialize it with 0
        if not 'Basket' in Users.shoppers[user_id]:
            Users.shoppers[user_id]['Basket'] = {}
        if selected_product_id not in Users.shoppers[user_id]['Basket']:
            Users.shoppers[user_id]['Basket'][selected_product_id] = 0
            # Add the selected quantity to the user's basket
        Users.shoppers[user_id]['Basket'][selected_product_id] = quantity
            # Reduce the stock in the main product list (important to avoid over-selling)
        selected_product['inventory'] = quantity -1
        Admin.save_products_to_file_P()
        Users.save_users_to_file()
        print(f"{quantity} units of {selected_product['name']} have been added to your basket!")
    #******************************************************************
    @classmethod
    def display_basket(cls, user_id):
        Products.products_db = Admin.load_products_from_file()
        Users.load_users_from_file()
        Users.load_users_from_file()
        shopper = cls.shoppers.get(user_id)
        print(shopper)
        if not shopper:
            print("Shopper not found!")
            return
        basket = shopper.get('Basket', {})
        if not basket:
            print("Your basket is empty.")
            return
        total_cost = 0.0
        print("\nYour Basket:")
        print("-" * 50)
        print("{:<15} {:<10} {:<10} {:<15}".format('Product Name', 'Price', 'Quantity', 'Total'))
        print("-" * 50)
        for product_id, quantity in basket.items():
            product = Products.get_product_by_id(product_id)
            if product:
                product_name = product.get('name')
                price = float(product.get('price'))
                cost_of_purchase = price * quantity
                total_cost += cost_of_purchase
                print("{:<15} ${:<10.2f} {:<10} ${:<15.2f}".format(product_name, price, quantity, cost_of_purchase))
            else:
                print(f"DEBUG: No product data found for ID {product_id}.")  # Debugging print

        print("-" * 50)
        print("{:<35} ${:.2f}".format('Total Cost:', total_cost))
        print("\n")
    #*******************************************************
    @staticmethod
    def display_all_products():
        Products.products_db = Admin.load_products_from_file()
        for category, category_data in Products.products_db.items():
            for product_id, product_data in category_data.items():
                print(
                    f"Product ID: {product_id} | Category: {category.value} | Name: {product_data['name']} | Price: {product_data['price']} | Inventory: {product_data['inventory']}")

    #*****************************************************
    @classmethod
    def update_basket(cls):
        while True:
            print("\nUpdate Basket Options:")
            print("1. Clear Basket")
            print("2. Remove Product")
            print("3. Update Quantity")
            print("4. Return to previous menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                cls.clear_basket(cls)
            elif choice == "2":
                product_id = input("Enter the product ID to remove: ").strip()
                cls.remove_product(cls,product_id)
            elif choice == "3":
                product_id = input("Enter the product ID to update: ").strip()
                qty = int(input("Enter the new quantity: "))
                cls.update_product_quantity(cls,product_id, qty)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    @classmethod
    def clear_basket(cls):
        Users.shoppers[cls.user_id]['Basket'].clear()
        print("Basket cleared!")

    @classmethod
    def remove_product(cls, product_id):
        if product_id in cls.basket:
            del cls.basket[product_id]
            print(f"Product {product_id} removed from basket!")
        else:
            print(f"Product {product_id} not found in basket.")

    @classmethod
    def update_product_quantity(cls, product_id, qty):
        if product_id in cls.basket:
            cls.basket[product_id] = qty
            print(f"Updated quantity for Product {product_id} to {qty}!")
        else:
            print(f"Product {product_id} not found in basket.")
    #*****************************************************
    @classmethod
    def place_order(cls):
        Products.products_db = Admin.load_products_from_file()
        # Check if the basket is empty
        if not cls.basket:
            print("Your basket is empty. Add products to the basket before placing an order.")
            return

        total_price = 0
        print("Current Products:", Products.products_db)
        for product_id, quantity in cls.basket.items():
            product = Products.get_product_by_id(product_id)
            if product:
                total_price += float(product.get('price')) * quantity
            else:
                print(f"Product with ID {product_id} not found. It might have been removed or not added yet.")
        confirmation = input(f"Your order total is ${total_price:.2f}. Do you want to place the order? (yes/no): ")
        if confirmation.lower() == 'yes':
            cls.order = "Placed"
            cls.basket = {}
            print("Order placed successfully!")
        else:
            print("Order cancelled.")
    #*****************************************************