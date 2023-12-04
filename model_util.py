from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification, AdamW
import torch



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
    

def main():
    model = SentimentModel()
    print(model.analyze_sentiment("This was amazing"))


main()