import numpy as np
import os

from proximityCalculator import ProximityCalculator
from pymongo import MongoClient
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGO_DB_URI')

client = MongoClient(MONGODB_URI)

db = client.covid
user_profiles = db.user_profile
def get_users_affected(user_id, collection):
    positive_user_Data = collection.find_one({'id': user_id})
    # print(positive_user_Data["GPS_Data"][:10])
    positive_arr = np.array([[d["id"],d["id"], d["row"], d["col"], d["time"], d[" time_delta(s) "], 
                             d["lng"], d["lat"]]  for d in positive_user_Data["GPS_Data"]])
    print(positive_arr[:10])
    proximityCalc = ProximityCalculator(positive_arr)

    user_ids = collection.find( { "id": { "$not": { "$eq": user_id } } }, {"id" : 1} )
    proximityCalc.log1 = positive_arr
    proximities =[]
    for id_data in user_ids:
        user_data = collection.find_one({"id" : id_data["id"]})
        # print(user_data["GPS_Data"][:10])
        user_arr = np.array([[  
                                d["id"], d["id"], d["row"], d["col"], d["time"], d[" time_delta(s) "], 
                                d["lng"], d["lat"]]  for d in user_data["GPS_Data"]   
                            ])
        proximityCalc.log2 = positive_arr
        proximity_map = proximityCalc.calculate_proximity(user_arr)
        if len(proximity_map) != 0:
            proximities.append(list(proximity_map[user_id])[0])
        # print(positive_arr[:10])  
    
    return proximities
    

def mark_user_positive(user_id, collection):
    for doc in collection.find({'id': int(user_id)}, {"id": 1, "Age": 1, "risk_score": 1, "Covid_status": 1}):
        print(doc)
    collection.update_one({'id': int(user_id)}, {"$set":{"Covid_status": "positive"}})

if __name__ == "__main__":
    # get_users_affected(53, user_profiles)
    max_id = user_profiles.find({}, {"id": 1}).sort("id", -1).limit(1)
    print(list(max_id)[0]["id"])