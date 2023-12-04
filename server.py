from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.json
    youtube_url = data['url']
    print("Received URL:", youtube_url)  # Log the received URL to console

    # Placeholder for fetching comments and analyzing sentiment
    sentiments = ['positive']  # Static positive response for now

    # Return the results
    return jsonify({"sentiments": sentiments})

if __name__ == '__main__':
    app.run(debug=True)
