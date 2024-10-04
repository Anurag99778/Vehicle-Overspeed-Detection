import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

cluster = MongoClient("")
db = cluster['overspeed']

@app.route("/parent-alert/", methods=['GET'])
def add_value():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        car = request.args.get("car_no")
        
        if not all([lat, lon, car]):
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400
        
        current_time = datetime.now(pytz.timezone("Asia/Calcutta"))
        date = current_time.strftime("%d-%m-%Y")
        time = current_time.strftime("%I:%M:%S %p")

        alert_data = {
            "Date": date,
            "Time": time,
            "Latitude": lat,
            "Longitude": lon,
            "Car Number": car
        }

        db['car_alerts'].insert_one(alert_data)
        return jsonify({"status": "success", "message": "Alert added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An unexpected issue occurred"}), 500

@app.route('/alerts/', methods=['GET'])
def get_alerts():
    try:
        car_alerts = list(db['car_alerts'].find({}, {'_id': 0}))
        return jsonify({"status": "success", "alerts": car_alerts}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Unable to retrieve alerts"}), 500

@app.route('/delete_alert/', methods=['DELETE'])
def delete_alert():
    date = request.args.get("date")
    time = request.args.get("time")
    car = request.args.get("car")
    
    if not all([date, time, car]):
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    alert_to_delete = {
        "Date": date,
        "Time": time,
        "Car Number": car
    }

    result = db['car_alerts'].delete_one(alert_to_delete)
    if result.deleted_count == 1:
        return jsonify({"status": "success", "message": "Alert deleted successfully!"}), 200
    else:
        return jsonify({"status": "error", "message": "Alert not found"}), 404

@app.route('/contact', methods=['POST'])
def submit_contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        query = request.form.get('Querry')
        
        if not all([name, email, query]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        query_data = {
            "name": name,
            "email": email,
            "query": query
        }
        db['Querries'].insert_one(query_data)
        return jsonify({"status": "success", "message": "Query submitted successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "An unexpected issue occurred"}), 500

app.run(host="0.0.0.0", port=8080)
