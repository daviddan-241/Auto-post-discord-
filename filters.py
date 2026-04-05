KEYWORDS = [
    "meme", "fair launch", "launch", "pump", "stealth",
    "airdrop", "new pair", "token", "CA:", "discord"
]

def is_relevant(text):
    text = str(text).lower()
    return any(k in text for k in KEYWORDS)