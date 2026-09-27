from textblob import TextBlob


def analyze_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Positive"

    elif polarity < -0.2:
        return "Negative"

    return "Neutral"