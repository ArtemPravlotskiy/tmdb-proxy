from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

@app.route("/proxy", methods=["GET"])
def proxy():
    endpoint = request.args.get("endpoint")
    if not endpoint:
        return jsonify({"error": "Missing endpoint"}), 400

    url = f"https://api.themoviedb.org/3/{endpoint}"
    params = request.args.to_dict()
    params["api_key"] = TMDB_API_KEY

    response = requests.get(url, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
