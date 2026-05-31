from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)

def analyze_sentiment(text):
    try:
        result = sentiment_model(str(text)[:512])[0]
        label = result["label"]
        score = float(result["score"])

        label_map = {
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive",
            "negative": "negative",
            "neutral": "neutral",
            "positive": "positive"
        }

        return label_map.get(label, label), score

    except Exception:
        return "unknown", 0.0
