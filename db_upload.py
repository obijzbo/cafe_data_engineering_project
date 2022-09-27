import json
from pymongo import MongoClient
from configs.data_config import ROOT_PATH, DATA_PATH, VERSION
from configs.mad_chef_config import DATA_Dir as mad_chef_path
from configs.pizza_hut_config import DATA_Dir as pizza_hut_path


mad_chef_menu = f"{ROOT_PATH}/{DATA_PATH}/{mad_chef_path}/{VERSION}/menu_info.json"
mad_chef_location = f"{ROOT_PATH}/{DATA_PATH}/{mad_chef_path}/{VERSION}/location_info.json"
pizza_hut_menu = f"{ROOT_PATH}/{DATA_PATH}/{pizza_hut_path}/{VERSION}/menu_info.json"
pizza_hut_location = f"{ROOT_PATH}/{DATA_PATH}/{pizza_hut_path}/{VERSION}/location_info.json"

client = MongoClient("mongodb://localhost:27017/")

db = client["mad_chef_menu"]

Collection = db["data"]

with open(mad_chef_menu) as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)


db = client["mad_chef_location"]

Collection = db["data"]

with open(mad_chef_location) as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)


db = client["pizza_hut_menu"]

Collection = db["data"]

with open(pizza_hut_menu) as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)


db = client["pizza_hut_location"]

Collection = db["data"]

with open(pizza_hut_location) as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)