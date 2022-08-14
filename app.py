from enum import unique
from flask import Flask, render_template, request, url_for, redirect
from logging import FileHandler,WARNING
from pymongo import MongoClient
from dotenv import load_dotenv
from covid_tracer import get_users_affected, mark_user_positive


import os

app = Flask(__name__, template_folder = 'templates')
app.secret_key = "secret key"

load_dotenv()

user_id_map = {}

MONGODB_URI = os.getenv('MONGO_DB_URI')

client = MongoClient(MONGODB_URI)

db = client.covid
user_profiles = db.user_profile


@app.route('/', methods=('GET', 'POST'))
def index():
    profiles = user_profiles.find({}, {"id": 1, "Age": 1, "risk_score": 1, "Covid_status": 1})
    # print(profiles)
    profiles_arr = []
    for profile in profiles:
        profiles_arr.append(profile)
    return render_template('index.html', profiles=profiles_arr)

@app.route('/locationUpdate', methods=('GET', 'POST'))
def locationUpdate():
    # print(request.data)
    # print(request.form["location"])
    lat, lng, date = request.form["lat"], request.form["lng"], request.form["date"]
    uniqueID = request.form["uniqueID"]
    db_id = get_unique_user_id(uniqueID)
    print("********DATA RECEIVED*************")
    print(uniqueID, (lat, lng, date))
    insert_data_to_db(uniqueID, (lat, lng, date))
    return {"blah": "hello"}

@app.route('/getUserID', methods=['POST'])
def getUserID():
    print(request.data)
    print(request.form["uniqueID"])
    uniqueID = request.form["uniqueID"]
    
    return {"id" : get_unique_user_id(uniqueID)}

@app.route("/mark-covid-positive", methods=['POST'])
def stop():
    user_id = request.form['id']
    print(user_id)
    try:
        mark_user_positive(user_id, user_profiles)
        # get_users_affected(user_id, user_profiles)
    except Exception as e:
        print(e)
    # instances = describe_ec2_instance(EC2_INSTANCE)
    return redirect(url_for('index'))

@app.route("/fetch-contacts", methods=['POST'])
def fetch_contacts():
    """
    Fetches users affected by being in close contact with id user_id
    """
    user_id = request.form['id']
    print(user_id)
    try:
        users_affected = get_users_affected(int(user_id), user_profiles) # list of users possibly infected
        print(users_affected)
        profiles = user_profiles.find({"id": {"$in": users_affected}}, {"id": 1, "Age": 1, "risk_score": 1, "Covid_status": 1, "num_vaccines": 1,
                                       "last_vaccination_date" : 1, "vaccine_effectiveness": 1})
        print(profiles)
        # get_users_affected(user_id, user_profiles)
    except Exception as e:
        print(e)
    # instances = describe_ec2_instance(EC2_INSTANCE)
    return render_template('contacts.html', users_affected=profiles, user_id=user_id)


def get_unique_user_id(uniqueID):
    if user_id_map.get(uniqueID) is None:
        max_id = user_profiles.find({}, {"id": 1}).sort("id", -1).limit(1)
        user_id_map[uniqueID] = list(max_id)[0]["id"] + 1
    return user_id_map[uniqueID]

def insert_data_to_db(id, data):
    if db.app_profile.count_documents({"id": id}) == 0:
        x = db.app_profile.insert_one({"id" : id})
    
    db.app_profile.update_one({"id": id}, {"$push":
    {
        "GPS_Data" : {
            "lat" : data[0],
            "lng": data[1],
            "date": data[2]
        }
    }})

if __name__ == '__main__':
    app.run(host='0.0.0.0')