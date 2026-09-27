CRISIS_KEYWORDS = [

    "suicide",
    "kill myself",
    "self harm",
    "end my life",
    "i want to die",
    "depressed",
    "hopeless"

]


def detect_crisis(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in CRISIS_KEYWORDS
    )