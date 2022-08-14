# from app import app
from flask import Flask, flash, session, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# from models import User_Profile
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

import os



load_dotenv()

MONGODB_URI = os.getenv('MONGO_DB_URI')
app.config['MONGODB_SETTINGS'] = {
    'db': 'Covid-Aware',
    'host': MONGODB_URI,
}
db = MongoEngine()
db.init_app(app)

class User_Profile(db.Document):
    id = db.IntField(required=True)
    Age = db.IntField()
    Hypertension = db.BinaryField()
    diabetes = db.BinaryField()
    num_vaccines = db.IntField()
    obese = db.BinaryField()
    Gender = db.StringField()
    COPD = db.BinaryField()
    risk_score = db.StringField()

@app.route('/', methods=['GET'])
def query_records():
    # name = request.args.get('name')
    users = User_Profile.objects
    print(users)
    if not users:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(users.to_json())

if __name__ == "__main__":
    app.run(debug=True, port=5002)