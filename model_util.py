from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification, AdamW
import torch
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

def getComments(video_id):
    #Youtube API setup
    youtube = build('youtube', 'v3', developerKey='AIzaSyDwG5Vzg4OduSTkl6YYHXPA9OK35hn2y0Q')

    #List to hold all comments:
    comments = []   

    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50,  # Set the number of comments you want to retrieve
        textFormat='plainText'
    ).execute()

    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

def classify_sentiment(score):
    if score < 0.4:
        return 0
    elif score > 0.6:
        return 1
    else:
        return 0.5

def calculate_video_sentiment(comments, sentiment_model):
    df = pd.DataFrame(np.array(comments), columns=['comment'])

    df['sentiment'] = df['comment'].apply(lambda x: sentiment_model.analyze_sentiment(x[:512]))
    df['sentiment_category'] = df['sentiment'].apply(classify_sentiment)
    positive_percentage = df['sentiment_category'].mean() * 100

    return positive_percentage


class SentimentModel:
    def __init__(self):
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        model_path = 'model_state_dict.pth'
        self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
        model_state_dict = torch.load(model_path, map_location='cpu')
        self.model.load_state_dict(model_state_dict)
        self.model.to(self.device)
        self.model.eval()

    def analyze_sentiment(self, comment):

        inputs = self.tokenizer(comment, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        probabilities = torch.nn.functional.softmax(logits, dim=1)
        positive_prob = probabilities[0, 1].item()

        return positive_prob
