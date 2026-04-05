import time
import requests

from dex import get_trending
from xscanner import scan_x
from keep_alive import keep_alive

WEBHOOK = "https://discord.com/api/webhooks/1490137623577235497/ZzzvUp5fDvWuMwlWB8SVYyNe5KP70S3V7kpi5nefBSXi3eDxSy4CFQOzkvDXPT_F9WsJ"

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

def run_dex():
    tokens = get_trending()
    for t in tokens:
        send(f"🔥 DEX ALERT\n{t['name']} ({t['symbol']})\nLiquidity: ${t['liq']}\n{t['url']}")

def run_x():
    posts = scan_x()
    for p in posts:
        send(f"🐦 X SIGNAL\n{p}")

def main():
    keep_alive()
    send("✅ Meme Radar Pro ONLINE")

    while True:
        try:
            run_dex()
            run_x()
            time.sleep(60)
        except Exception as e:
            send(f"⚠️ Error: {str(e)}")
            time.sleep(10)

main()