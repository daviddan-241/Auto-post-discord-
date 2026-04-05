KEYWORDS = [
    "meme", "launch", "fair launch", "stealth", "airdrop",
    "pump", "CA:", "discord.gg", "new token"
]

def is_relevant(text):
    text = text.lower()
    return any(k in text for k in KEYWORDS)