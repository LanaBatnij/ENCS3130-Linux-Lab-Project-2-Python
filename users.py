
class Users:

    shoppers = {}
    existing_user_ids = set()
    #****************************************
    def insert_users(line):
        user_id, user_name, DOB, role, actv, basket_str, order = line.strip().split(";")
        basket_dic = {}
        if basket_str:
            itemsOfBasket = basket_str.split(',')
            for item in itemsOfBasket:
                item_id, numOfItems = item.split(':')
                basket_dic[item_id] = int(numOfItems)
        order = int(order)
        if user_id in Users.shoppers:
            Users.shoppers[user_id]['user_name'] = user_name
            Users.shoppers[user_id]['DOB'] = DOB
            Users.shoppers[user_id]['Role'] = role
            Users.shoppers[user_id]['Active'] = actv
            Users.shoppers[user_id]['Basket'] = basket_dic
            Users.shoppers[user_id]['order'] = order
        else:
            Users.shoppers[user_id] = {
                'user_name': user_name,
                'DOB': DOB,
                'Role': role,
                'Active': actv,
                'Basket': basket_dic,
                'order': order
            }

    # *******************************************************************
    @staticmethod
    def save_users_to_file():
        with open("users.txt", "w") as f:
            for user_id, user_data in Users.shoppers.items():
                basket_str = ",".join(
                    [f"{item_id}:{numOfItems}" for item_id, numOfItems in user_data['Basket'].items()])
                f.write(f"{user_id};{user_data['user_name']};{user_data['DOB']};{user_data['Role']};"
                        f"{user_data['Active']};{basket_str};{user_data['order']}\n")

    # ******************************************************************
    @staticmethod
    def load_users_from_file():
        with open("users.txt", "r") as f:
            for line in f:
                Users.insert_users(line)
    #*********************************************************************
    @staticmethod
    def clean_user_baskets(users_db, product_list):
        for user in users_db:  # assuming `users_db` is your users database
            basket = user.get('basket', {})
            for product_id in list(basket.keys()):
                if product_id not in product_list:
                    print(
                        f"WARNING: Product {product_id} in user {user['id']}'s basket not found in the main product database. Removing it from the basket.")
                    del basket[product_id]
    #*****************************************************
