from products import products
from product import Categ, Products
from users import Users

class Admin(Users):

    products = {}
    users = {}
    #********************************************************************
    @staticmethod
    def load_products_from_file():
        try:
            with open("products.txt", 'r') as f:
                lines = f.readlines()
                print(f"Number of lines in products.txt: {len(lines)}")

                for line in lines:
                    item = line.strip().split(';')
                    pro_id, pro_name, category, price, inventory, suppliers, onOffer, *remaining = item
                    offer_price, valid_until = remaining if len(remaining) == 2 else (None, None)
                    Cat = Categ[category]
                    if Cat not in Admin.products:
                        Admin.products[Cat] = {}
                    Admin.products[Cat][pro_id] = {
                        "id": pro_id,
                        "name": pro_name,
                        "price": float(price),
                        "inventory": int(inventory),
                        "suppliers": suppliers,
                        "on_Offer": int(onOffer),
                        "offer_price": None if offer_price == 'None' or offer_price is None else float(offer_price),
                        "valied_date": valid_until
                    }

        except FileNotFoundError:
            print("File not found!")
            # File doesn't exist yet, that's OK.
            pass

        Admin.save_products_to_file_P()
        return Admin.products
    #*******************************************************************
    @staticmethod
    def save_products_to_file_P():
        with open("products.txt", "w") as f:
            for category, category_data in Admin.products.items():
                for product_id, product_data in category_data.items():
                    f.write(f"{product_data['id']};{product_data['name']};{category.value};"
                                f"{product_data['price']};{product_data['inventory']};{product_data['suppliers']};"
                                f"{product_data['on_Offer']};{product_data.get('offer_price', '')};"
                                f"{product_data.get('valied_date', '')}\n")
    #********************************************************************
    @staticmethod
    def save_users_to_file_P():
        with open("users.txt", "w") as f:
            for user_id, user_data in Users.shoppers.items():
                # Convert user basket to string format
                basket_str = ",".join(
                    [f"{item_id}:{numOfItems}" for item_id, numOfItems in user_data['Basket'].items()])
                # Write the user's data to the file
                f.write(f"{user_id};{user_data['user_name']};{user_data['DOB']};{user_data['Role']};"
                        f"{user_data['Active']};{basket_str};{user_data['order']}\n")

    #********************************************************************
    @staticmethod
    def view_all_shoppers():
        criteria = input("Choose criteria (All, Basket, Unprocessed): ")
        print("\nShoppers:\n")
        print("Total Shoppers Loaded:", len(Users.shoppers))
        for user_id, user_data in Users.shoppers.items():
            # Diagnostic Print
            print("Checking user:", user_id)
            if criteria.lower() == "all":
                pass
            elif criteria.lower() == "basket" and not user_data['Basket']:
                continue
            elif criteria.lower() == "unprocessed" and user_data['order'] == 0:
                continue

            print(f"User ID: {user_id}")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("------")
    # ********************************************************************
    @staticmethod
    def add_product():
        product_id = Products.products_db.get('id')
        # Get input from the user
        pro_id = input("Enter Product ID (6-digit unique code): ").strip()
        pro_name = input("Enter Product Name (e.g., apple juice bottles): ").strip()
        pro_category = input("Enter Product Category (e.g., Electronics, Apparel, etc.): ").strip()
        price = input("Enter Price ($): ").strip()
        inventory = input("Enter Inventory (number of items available for sale): ").strip()
        supplier = input("Enter Supplier Name: ").strip()
        on_offer = input("Is this product on offer? Enter 1 for Yes and 0 for No: ").strip()

        # Validate input
        if not (pro_id.isdigit() and len(pro_id) == 6):
            print("Invalid Product ID. It must be a 6-digit unique code.")
            return

        if not pro_category in Categ.__members__:
            print(f"Invalid category. Available categories are: {', '.join([cat.name for cat in Categ])}")
            Admin.save_products_to_file()
            return

        Cat = Categ[pro_category]
        if Cat not in Admin.products:
            Admin.products[Cat] = {}

        Admin.products[Cat][pro_id] ={
                "id": pro_id,
                "name": pro_name,
                "price": price,
                "inventory": inventory,
                "suppliers": supplier,
                "on_Offer": on_offer,
                "offer_price": None if on_offer == 0 else float(input("Enter offer price: ")),
                "valied_date": None
            }

        print("Product added successfully!")
        Admin.save_products_to_file_P()
    #******************************************************************
    @staticmethod
    def display_all_users():
        print("\nAll Users:")
        for user_id, user_data in Users.shoppers.items():
            print(f"User ID: {user_id}")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("------")
    #********************************************************************
    @staticmethod
    def display_all_products():
        Admin.load_products_from_file()  # Assuming this loads the products
        criteria = input("Choose criteria (All, Offers, Category, Name): ").lower()
        if criteria == "all":
            print("\nAll Products:")
        elif criteria == "offers":
            print("\nProducts on Offer:")
        elif criteria == "category":
            category_choice = input("Enter the category name: ").strip()
            if category_choice not in Categ.__members__:
                print(f"Invalid category. Available categories are: {', '.join([cat.name for cat in Categ])}")
                return
            print(f"\nProducts in Category {category_choice}:")
        elif criteria == "name":
            product_name = input("Enter the product name: ").strip()
            print(f"\nProducts with Name {product_name}:")
        else:
            print("Invalid criteria!")
            return

        for category, category_data in Admin.products.items():
            for product_id, product_data in category_data.items():
                if criteria == "all" \
                        or (criteria == "offers" and product_data['on_Offer'] == 1) \
                        or (criteria == "category" and category.name == category_choice) \
                        or (criteria == "name" and product_data[
                    'name'].lower() == product_name.lower()):
                    print(f"Product ID: {product_id} | Category: {category.value}")
                    for key, value in product_data.items():
                        print(f"{key}: {value}")
                    print("------")
    #********************************************************************
    @staticmethod
    def add_user():
        # Get input from the user
        user_id = input("Enter User ID (6-digit unique code): ").strip()
        user_name = input("Enter User Name: ").strip()
        DOB = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        role = int(input("Enter Role (Admin or Shopper, enter 1 if it is admin and 2 if it is shopper): ").strip())
        active = int(input("Is the user active? Enter 1 for Yes and 0 for No: ").strip())
        order=0
        basket_str = input("Enter the items in the Baskec(cartoy,glasses,etc)")
        itemsOfBasket = basket_str.split(',')
        basket_dic = {}

        for item in itemsOfBasket:
            item = item.strip()
            numOfItems = input(f"How many {item}s do you want to add? ")

            try:
                basket_dic[item] = int(numOfItems)
            except ValueError:
                print(f"Invalid number of items for {item}. Skipping...")

        if not (user_id.isdigit() and len(user_id) == 6):
            print("Invalid User ID. It must be a 6-digit unique code.")
            return

        if role not in [1, 2]:
            print("Invalid Role. Enter 1 for Admin or 2 for Shopper.")
            return

        if active not in [0, 1]:
            print("Invalid Active status. Enter 1 for Yes and 0 for No.")
            return


        role_str = "Admin" if role == 1 else "Shopper"

        basket_format_str = ",".join([f"{item_id}:{numOfItems}" for item_id, numOfItems in basket_dic.items()])
        line = f'{user_id};{user_name};{DOB};{role_str};{active};{basket_format_str};{order}'

        # Use the insert_users function from the Users class (via inheritance)
        Admin.insert_users(line)
        Admin.save_users_to_file_P()
        print("User added successfully!")
    #*****************************************************************
    @staticmethod
    def place_item_on_sale():
        product_id = input("Enter the Product ID of the item you want to put on sale: ").strip()

        product_found = False
        for category, category_data in Admin.products.items():
            if product_id in category_data:
                product = category_data[product_id]
                product_found = True
                break

        if not product_found:
            print("Product not found!")
            return


        offer_price = input("Enter the discounted price for the product: ").strip()
        valid_until = input("Enter the validity date for the offer (YYYY-MM-DD): ").strip()

        try:
            product["on_Offer"] = 1
            product["offer_price"] = float(offer_price)
            product["valied_date"] = valid_until
        except Exception as e:
            print(f"Error updating product details: {e}")
            return

        print("Product sale details updated successfully!")
        Admin.save_products_to_file_P()
    #*********************************************************************
    @staticmethod
    def update_user():
        Users.load_users_from_file()
        user_id = input("Enter the User ID (6-digit unique code) of the user you want to update: ").strip()
        if user_id in Users.shoppers:
            user_data = Users.shoppers[user_id]
            print("\nUser Details:")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            fields = ["user_name", "DOB", "Role", "Active"]
            field_to_update = input(f"\nWhich field do you want to update? Choose from {fields}: ").strip()

            if field_to_update in fields:

                new_value = input(f"Enter new value for {field_to_update}: ").strip()

                if field_to_update == "Active":
                    if new_value not in ["0", "1"]:
                        print("Invalid Active status. Enter 1 for Yes and 0 for No.")
                        return
                    new_value = int(new_value)
                elif field_to_update == "Role":
                    if new_value not in ["Admin", "Shopper"]:
                        print("Invalid Role. Enter Admin or Shopper.")
                        return

                #Update the user's details
                Users.shoppers[user_id][field_to_update] = new_value

                #Save the updated user details to the file
                Users.save_users_to_file()

                print(f"{field_to_update} updated successfully!")
            else:
                print("Invalid field selected!")
        else:
            print("User not found!")
    #******************************************************************
    @staticmethod
    def execute_order():
        shopper_id = input("Enter the shopper ID: ").strip()

        shopper_data = Users.shoppers.get(str(shopper_id))
        if not shopper_data:
            print("Shopper not found!")
            return

        basket = shopper_data.get('Basket', {})

        for product_id, quantity in basket.items():
            product_found = False
            for category, category_data in Admin.products.items():
                if product_id in category_data:
                    product = category_data[product_id]
                    product_found = True
                    break
            if not product_found:
                print(f"Product with ID {product_id} not found!")
                continue

            # Update product inventory
            product_inventory = product.get('inventory', 0)
            if product_inventory < quantity:
                print(f"Insufficient inventory for product {product_id}.")
                continue
            product['inventory'] -= quantity

            # Clear the item from the shopper's basket
            del basket[product_id]
            print(f"Executed order for product {product_id}. New inventory: {product['inventory']}.")
        # Update the shopper's basket to be empty after all items are processed
        shopper_data['Basket'] = {}
        Admin.save_products_to_file_P()
        Users.save_users_to_file()
        print(f"Order for shopper {shopper_id} executed successfully!")
    #******************************************************************
