import pymongo
import json
import os

db_host = os.environ.get('MONGODB_HOST')
target_database = os.environ.get('MONGODB_DATABASE')
target_collection = os.environ.get('MONGODB_COLLECTION')

def insertJson(messages,json_data):
    mongo_client = pymongo.MongoClient(db_host)

    # 假設你要儲存JSON數據的數據庫名稱為"my_database"
    db = mongo_client[target_database]

    # 假設你要儲存JSON數據的集合名稱為"my_collection"
    collection = db[target_collection]

    response_data = {
        "id" : json_data["id"],
        "object" : json_data["object"],
        "created" : json_data["created"],
        "model" : json_data["model"],
        "prompt" : messages,
        "choices" : json_data["choices"],
        "usage" : json_data["usage"],
    }

    # 將JSON數據插入到集合中
    insert_result = collection.insert_one(response_data)

    # 關閉MongoDB連接
    mongo_client.close()
