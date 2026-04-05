import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

CHAINS = ["solana", "ethereum", "bsc", "base"]
seen = set()


# ---------------- FILTER LOGIC ----------------
def is_discord_only(socials: dict):
    if not socials:
        return False

    return (
        socials.get("discord")
        and not socials.get("twitter")
        and not socials.get("telegram")
        and not socials.get("website")
    )


# ---------------- FETCH DATA ----------------
async def fetch_pairs(session, chain):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}"
    try:
        async with session.get(url, timeout=15) as r:
            data = await r.json()
            return data.get("pairs", [])
    except:
        return []


# ---------------- SEND TO DISCORD ----------------
async def send_webhook(message):
    async with aiohttp.ClientSession() as session:
        await session.post(WEBHOOK_URL, json={
            "content": message
        })


# ---------------- SCANNER LOOP ----------------
async def scanner():
    async with aiohttp.ClientSession() as session:
        while True:
            for chain in CHAINS:
                pairs = await fetch_pairs(session, chain)

                for p in pairs:
                    pair_id = p.get("pairAddress")
                    if not pair_id or pair_id in seen:
                        continue

                    info = p.get("info", {})
                    socials_list = info.get("socials", [])

                    socials = {}
                    for s in socials_list:
                        socials[s.get("type")] = s.get("url")

                    if is_discord_only(socials):
                        seen.add(pair_id)

                        msg = (
                            f"🚨 NEW DISCORD GEM\n"
                            f"💎 Name: {p.get('baseToken', {}).get('name')}\n"
                            f"🔗 Chain: {chain}\n"
                            f"💰 Price: {p.get('priceUsd')}\n"
                            f"💧 Liquidity: {p.get('liquidity', {}).get('usd')}\n"
                            f"🔵 Discord: {socials.get('discord')}\n"
                            f"📍 Pair: {pair_id}"
                        )

                        await send_webhook(msg)

            await asyncio.sleep(60)


# ---------------- START ----------------
if __name__ == "__main__":
    if not WEBHOOK_URL:
        raise Exception("Missing DISCORD_WEBHOOK_URL in environment")

    keep_alive()
    asyncio.run(scanner())