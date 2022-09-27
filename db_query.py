import pymongo

def query(location, item, price):
    results = []

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mad_chef_menu_db = client["mad_chef_menu"]
    mad_chef_location_db = client["mad_chef_location"]
    pizza_hut_menu_db = client["pizza_hut_menu"]
    pizza_hut_location_db = client["pizza_hut_location"]

    mad_chef_menu_collection = mad_chef_menu_db["data"]
    mad_chef_location_collection = mad_chef_location_db["data"]
    pizza_hut_menu_collection = pizza_hut_menu_db["data"]
    pizza_hut_location_collection = pizza_hut_location_db["data"]

    mad_chef_loc = []
    for loc in mad_chef_location_collection.find():
        mad_chef_loc = loc
    mad_chef_loc = mad_chef_loc['mad_chef']

    mad_chef_menu = []
    for menu in mad_chef_menu_collection.find():
        mad_chef_menu.append(menu)

    pizza_hut_loc = []
    for loc in pizza_hut_location_collection.find():
        pizza_hut_loc = loc
    pizza_hut_loc = pizza_hut_loc['pizza_hut']

    pizza_hut_menu = []
    for menu in pizza_hut_menu_collection.find():
        pizza_hut_menu.append(menu)


    for menu in mad_chef_menu:
        if location in mad_chef_loc and item == menu['index'] and int(price) >= int(menu['item_price']):
            result = {}
            result['shop_name'] = "Mad chef"
            result['location'] = location
            result['menu'] = item
            result['name'] = menu['item_name']
            result['description'] = menu['item_description']
            result['price'] = menu['item_price']
            results.append(result)


    for menu in pizza_hut_menu:
        if location in pizza_hut_loc and item == menu['index'] and int(price) >= int(menu['item_price']):
            result = {}
            result['shop_name'] = "Pizza Hut"
            result['location'] = location
            result['menu'] = item
            result['name'] = menu['item_name']
            result['description'] = menu['item_description']
            result['price'] = menu['item_price']
            results.append(result)


    return results