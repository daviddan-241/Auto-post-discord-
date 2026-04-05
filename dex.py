import requests

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/{chain}"

def get_trending():
    res = requests.get(DEX_URL).json()
    pairs = res.get("pairs", [])

    results = []

    for p in pairs:
        try:
            liquidity = p["liquidity"]["usd"]
            age = p.get("pairCreatedAt", 0)

            if liquidity and liquidity > 8000:
                results.append({
                    "name": p["baseToken"]["name"],
                    "symbol": p["baseToken"]["symbol"],
                    "liq": liquidity,
                    "url": p["url"]
                })
        except:
            pass

    return results