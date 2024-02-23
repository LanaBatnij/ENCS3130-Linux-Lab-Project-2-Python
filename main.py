
from product import Categ,Products
from shopper import Shopper
from users import Users
from admin import Admin


def main():
    all_products = []
    for category, products in Products.products_db.items():
        for product_id, details in products.items():
            all_products.append(details)
    Users.load_users_from_file()  # Load users before displaying menu
    while True:
        print("_" * 70)
        print("_________________Welcome to the E-commerce System_____________________")
        print("_" * 70)
        print("\n1. Admin Login")
        print("2. Shopper Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            while True:
                print("\n-----Admin Options-----")
                print("a. Add Product")
                print("b. Add User")
                print("c. Display All Users")
                print("d. List of Shoppers ")
                print("e. List of Products")
                print("f. Place an item on sale")
                print("g. Update User")
                print("h. Execute Order")
                print("i. Save Products to a file ")
                print("j. Save Users to a file ")
                print("z. Return to main menu")
                admin_choice = input("Enter your choice: ").strip().lower()
                if admin_choice == "a":
                    Admin.add_product()
                elif admin_choice == "b":
                    Admin.add_user()
                elif admin_choice == "c":
                    Admin.display_all_users()
                elif admin_choice == "d":
                    Admin.view_all_shoppers()
                elif admin_choice == "e":
                    Admin.display_all_products()
                elif admin_choice == "f":
                    Admin.place_item_on_sale()
                elif admin_choice == "g":
                    Admin.update_user()
                elif admin_choice == "h":
                    Admin.execute_order()
                elif admin_choice == "i":
                    Admin.save_products_to_file_P()
                    print("It is saved successfully on the products.txt check it")
                elif admin_choice == "j":
                    Admin.save_users_to_file_P()
                    print("It is saved successfully on the users.txt check it")
                elif admin_choice == "z":
                    break
            else:
                print("Invalid choice. Please try again.")
        elif choice == "2":
            user_id = input("Enter your user ID to login: ").strip()
            if user_id in Users.shoppers:
                if Users.shoppers[user_id]['Active'] and Users.shoppers[user_id]['Role'] == 'Shopper':
                    shopper = Shopper(user_id)

                else:
                    print("You either have an inactive account or you are not a shopper.")
            else:
                print("Invalid Id ")
            while True:
                print("Welcome Back, " + user_id + "!")
                print("\n-----Shopper Options-----")
                print("a. View Products")
                print("b. Add Product to Basket")
                print("c. Display the Basket ")
                print("d. Update the Basket ")
                print("e. Place Order ")
                print("z. Return to main menu")
                shopper_choice = input("Enter your choice: ").lower()
                if shopper_choice == "a":
                    Admin.display_all_products()  # Or `shopper.display_all_products()` if you want it instance-based
                elif shopper_choice == "b":
                    Shopper.add_product_to_basket(user_id)
                elif shopper_choice == "c":
                    Shopper.display_basket(user_id)
                elif shopper_choice == "d":
                    Shopper.update_basket()
                elif shopper_choice == "e":
                    Shopper.place_order()
                elif shopper_choice == "z":
                    break
            else:
                print("User ID not found. Please register as a shopper first.")
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
