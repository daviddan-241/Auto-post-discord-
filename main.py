import time
import requests

from keep_alive import keep_alive
from sources import scan_dexscreener, scan_gecko, scan_pump_fun
from filters import is_relevant

WEBHOOK = "YOUR_DISCORD_WEBHOOK"

seen = set()

def send(msg):
    try:
        requests.post(WEBHOOK, json={"content": msg}, timeout=10)
    except:
        pass


def dedupe(item):
    key = item["name"] + item["chain"]
    if key in seen:
        return False
    seen.add(key)
    return True


def format_item(item):
    return f"""🔥 {item['source']} ALERT
Name: {item['name']} ({item['symbol']})
Chain: {item['chain']}
Liquidity/MC: ${item['liq']}
{item['url']}"""


def run_all():
    results = []

    results += scan_dexscreener()
    results += scan_gecko()
    results += scan_pump_fun()

    for r in results:
        try:
            if not dedupe(r):
                continue

            if not is_relevant(r.get("name", "")):
                continue

            send(format_item(r))

        except:
            continue


def main():
    keep_alive()
    send("✅ Meme Radar PRO ONLINE (Multi-chain + Multi-source)")

    while True:
        try:
            run_all()
            time.sleep(90)  # stable for APIs
        except Exception as e:
            print("loop error:", e)
            time.sleep(10)


main()