import logging
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("api")

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
collection = client["iot"]["humidity"]


@app.route("/humidity", methods=["POST"])
def add_humidity():
    data = request.get_json(silent=True)
    if not data or "humidity" not in data:
        log.warning("Invalid payload: %s", data)
        return jsonify({"error": "Field 'humidity' is required"}), 400

    doc = {
        "device_id": data.get("device_id", "unknown"),
        "humidity": data["humidity"],
        "timestamp": datetime.now(timezone.utc).isoformat(),  # BONUS: timestamp
    }
    collection.insert_one(doc)
    log.info("Stored reading: %s", doc)
    return jsonify({"message": "Data stored"}), 201


@app.route("/humidity", methods=["GET"])
def get_humidity():
    docs = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(100))
    return jsonify(docs), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)