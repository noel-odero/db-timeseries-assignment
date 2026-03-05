from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home():
    return "MongoDB API is running!"
# ------------------- Connect to MongoDB Atlas -------------------
MONGO_URI = "mongodb+srv://dbirenzi_db_user:0jNztsP3qkTYOniX@cluster0.tofse6y.mongodb.net/climate_health_db?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(MONGO_URI)
db = client["climate_health_db"]
mongo_collection = db["climate_data"]

# ------------------- CREATE -------------------
@app.route('/api/mongo/create', methods=['POST'])
def create_record():
    data = request.get_json()
    if 'date' in data:
        # Convert date string to ISODate
        data['date'] = datetime.fromisoformat(data['date'])
    result = mongo_collection.insert_one(data)
    return jsonify({"message": "Record inserted", "id": str(result.inserted_id)}), 201

# ------------------- READ: Latest Record by Country -------------------
@app.route('/api/mongo/latest/<country_name>', methods=['GET'])
def latest_record(country_name):
    result = mongo_collection.find_one(
        {"country_name": country_name},
        sort=[("date", -1)]
    )
    if result:
        result['_id'] = str(result['_id'])
        return jsonify(result)
    return jsonify({"error": "No data found"}), 404

# ------------------- READ: Records by Date Range -------------------
@app.route('/api/mongo/range/<country_name>', methods=['GET'])
def records_by_range(country_name):
    start = request.args.get('start')  # e.g., 2024-02-01
    end = request.args.get('end')      # e.g., 2025-05-31
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
    except:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400
    
    cursor = mongo_collection.find(
        {
            "country_name": country_name,
            "date": {"$gte": start_date, "$lte": end_date}
        }
    ).sort("date", 1)
    
    results = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    
    return jsonify(results)

# ------------------- UPDATE -------------------
@app.route('/api/mongo/update/<record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    if 'date' in data:
        data['date'] = datetime.fromisoformat(data['date'])
    result = mongo_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": data}
    )
    if result.matched_count:
        return jsonify({"message": "Record updated"})
    return jsonify({"error": "Record not found"}), 404

# ------------------- DELETE -------------------
@app.route('/api/mongo/delete/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    result = mongo_collection.delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count:
        return jsonify({"message": "Record deleted"})
    return jsonify({"error": "Record not found"}), 404

# ------------------- Run Flask App -------------------
if __name__ == '__main__':
    app.run(debug=True)