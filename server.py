from flask import Flask, request, jsonify
from flask_cors import CORS
from model_util import SentimentModel, getComments, calculate_video_sentiment

app = Flask(__name__)
CORS(app)
model = SentimentModel()

def summarize_sentiment(score):
    if score > 60:
        return "positive"
    elif score >= 40 and score <= 60:
        return "neutral"
    else:
        return "negative"

@app.route('/analyze', methods=['GET'])
def analyze_video():
    youtube_url = request.args.get('url')
    print("Received URL:", youtube_url)

    video_id = youtube_url.split('watch?v=')[-1]
    comments = getComments(video_id)
    sentiment_score = calculate_video_sentiment(comments, model)
    overall_sentiment = summarize_sentiment(sentiment_score)
    print(sentiment_score)
    print(overall_sentiment)

    return jsonify({"sentiment": overall_sentiment, "average_score": sentiment_score})

if __name__ == '__main__':
    app.run(debug=True)
