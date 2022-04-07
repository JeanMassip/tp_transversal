from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/events")
def get_events():
    collection = get_collection()
    result = []
    if collection == None:
        return {"error": "Failed to connect to DB"}, 500
    events = collection.find()
    for event in events:
        event["_id"] = str(event["_id"])
        result.append(event["message"])

    return jsonify(result)

@app.get("/events/<id>")
def get_event(id):
    collection = get_collection()
    if collection == None:
        return {"error": "Failed to connect to DB"}, 500
    event = collection.find_one({"_id": ObjectId(id)})
    if len(event) == 0:
        return {"error":"No event with this id"}, 404
    event["_id"] = str(event["_id"])
    return jsonify(event)

@app.post("/events")
def create_event():
    if request.is_json:
        event = request.get_json()
        collection = get_collection()
        if collection == None:
            return {"error": "Failed to connect to DB"}, 500
        res = collection.insert_one(event)
        return str(res.inserted_id), 201
    return {"error": "Request must be JSON"}, 415

def get_collection():
    client = MongoClient("mongodb://database:27017/")
    try:
        client.admin.command("ismaster")
    except ConnectionError:
        print("Failed to connect to DB")
        return None
    db = client['tp_transversam']
    return db["denm_events"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)