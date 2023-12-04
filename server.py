from flask import Flask, request, jsonify
from flask_cors import CORS
from model_util import SentimentModel, getComments, calculate_video_sentiment  # Import from your sentiment analysis script

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
model = SentimentModel()  # Instantiate the sentiment model

def summarize_sentiment(score):
    if score > 60:
        return "positive"
    elif score >= 40 and score <= 60:
        return "neutral"
    else:
        return "negative"

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.json
    youtube_url = data['url']
    print("Received URL:", youtube_url)  # Log the received URL to console

    # Extract video ID from the YouTube URL
    video_id = youtube_url.split('watch?v=')[-1]  # Basic parsing, consider more robust methods for different URL formats

    # Fetch comments and analyze sentiment
    comments = getComments(video_id)
    sentiment_score = calculate_video_sentiment(comments, model)
    overall_sentiment = summarize_sentiment(sentiment_score)

    # Return the summarized sentiment
    return jsonify({"sentiment": overall_sentiment, "average_score": sentiment_score})

if __name__ == '__main__':
    app.run(debug=True)
