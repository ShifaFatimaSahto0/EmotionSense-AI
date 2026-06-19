from transformers import pipeline

# Load model once
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def predict_emotion(text):

    results = classifier(text)[0]

    best_emotion = max(results, key=lambda x: x["score"])

    emotion = best_emotion["label"]
    confidence = best_emotion["score"]

    return emotion, confidence