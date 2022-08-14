import os
import json
import pandas as pd

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGO_DB_URI')

client = MongoClient(MONGODB_URI)

db = client.covid
user_profiles = db.user_profile

def mongoimport(csv_path, db_name, coll_name, db_url='localhost', db_port=27000):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    data = pd.read_csv(csv_path)
    payload = json.loads(data.to_json(orient='records'))
    coll.remove()
    coll.insert_many({"GPS_Data": payload})
    return coll.count()
def load_locations():
    # for doc in db.user_profile.find({'id': 8}):
    #     print(doc)

    # x = user_profiles.delete_many({})

    # print(x.deleted_count, " documents deleted.")


    # print(db.list_collection_names())

    # db.user_profile.update_one({}, {"$set":{"Covid_status": "negative"}})
    db.user_profile.update_many(
        { },
        { "$unset": { "GPS_Data": "" } }
        )
    directory = r"C:\\Users\\mahno\\Documents\\Thesis\\Code\\server\\data\\"
    files_arr= []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            ext = os.path.splitext(filename)[-1].lower()
            if ext == ".csv":
    #         print(os.path.join(root, filename))
                files_arr.append(os.path.join(root, filename))

                data = pd.read_csv(os.path.join(root, filename))
                payload = json.loads(data.to_json(orient='records'))
                print(data.id[0])
                # for doc in db.user_profile.find({'id': int(data.id[0])}):
                #     print(doc)
                myquery = { "id": int(data.id[0]) }
                newvalues = { "$set": { "GPS_Data": payload } }

                x = user_profiles.update_many(myquery, newvalues)

def add_ve(file_path):
    data = pd.read_csv(file_path)
    for index,instance in data.iterrows():
        myquery = { "id": int(instance.id + 8) }
        newvalues = { "$set": { "vaccine_effectiveness": instance.vaccine_effectiveness_against_hospitalisation } }
        print(newvalues, myquery)
        x = user_profiles.update_many(myquery, newvalues)
        print(x)

def find_id_locations(id):
    for doc in db.user_profile.find({'id': id}):
        print(doc["GPS_Data"][:10])
        print(doc["Covid_status"])


if __name__ == "__main__":
    data_path = r"C:\Users\mahno\Documents\Thesis\datasets\synthetic data\shopping_mall_data_generator\Untitled Folder\User_Profile_with_ve.csv"
    add_ve(data_path)
    