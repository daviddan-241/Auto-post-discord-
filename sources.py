import requests

# ---------------- DEXSCREENER (ALL CHAINS) ----------------
def scan_dexscreener():
    url = "https://api.dexscreener.com/latest/dex/pairs"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return []

        data = r.json()
        pairs = data.get("pairs", [])

        results = []

        for p in pairs[:50]:
            try:
                liquidity = p.get("liquidity", {}).get("usd", 0)
                chain = p.get("chainId", "unknown")

                if liquidity and liquidity > 5000:
                    results.append({
                        "source": "DEXScreener",
                        "name": p["baseToken"]["name"],
                        "symbol": p["baseToken"]["symbol"],
                        "liq": liquidity,
                        "chain": chain,
                        "url": p["url"]
                    })
            except:
                continue

        return results

    except:
        return []


# ---------------- GECKO TERMINAL (NEW PAIRS) ----------------
def scan_gecko():
    url = "https://api.geckoterminal.com/api/v2/networks/trending_pools"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return []

        data = r.json()
        pools = data.get("data", [])

        results = []

        for p in pools[:30]:
            try:
                attr = p["attributes"]
                name = attr.get("name", "unknown")

                results.append({
                    "source": "GeckoTerminal",
                    "name": name,
                    "symbol": "",
                    "liq": attr.get("reserve_in_usd", 0),
                    "chain": p.get("id", "unknown"),
                    "url": attr.get("pool_address", "")
                })
            except:
                continue

        return results

    except:
        return []


# ---------------- PUMP.FUN LIGHT SCRAPER ----------------
def scan_pump_fun():
    url = "https://frontend-api.pump.fun/coins"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return []

        data = r.json()
        results = []

        for c in data[:30]:
            try:
                results.append({
                    "source": "Pump.fun",
                    "name": c.get("name"),
                    "symbol": c.get("symbol"),
                    "liq": c.get("usd_market_cap", 0),
                    "chain": "solana",
                    "url": f"https://pump.fun/{c.get('mint')}"
                })
            except:
                continue

        return results

    except:
        return []