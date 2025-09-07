import requests
import time
from datetime import datetime
import pytz
import os

# Конфигурация
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "ТВОЙ_ТОКЕН")
CHAT_ID = os.getenv("CHAT_ID", "5172658362")
API_URL = os.getenv("API_URL", "https://gagstock.gleeze.com/grow-a-garden")
BISHKEK_TZ = pytz.timezone("Asia/Bishkek")

# Редкие продавцы
RARE_SELLERS = [
    "Bee Keeper",
    "Mushroom Merchant",
    "Witch",
    "Ghost",
    "Secret Seller",
    "Sprinkler Seller",
    "Gnome",
    "Summer Seller"
]

# Редкие предметы/погоды
RARE_ITEMS = {
    "Plasmatic Plant": "🌱",
    "Divine Plant": "🌱",
    "Pitcher Plant": "🌱",
    "Level-up Lollipop": "🍭",
    "Sprinkler": "💧",
    "Rare Egg": "🥚",
    "Bee Egg": "🥚",
    "Rare Summer Egg": "🥚",
    "Paradise Egg": "🥚",
    "Legendary Egg": "🥚",
    "Mythical Egg": "🥚",
    "Sugar Apple": "🍎",
    "Rainbow Weather": "🌈",
    "Snowstorm": "❄️",
    "Thunderstorm": "⚡",
    "Tornado": "🌪",
    "Eclipse": "🌞",
    "Celestial Storm": "🌌",
    "Black Hole": "🕳️",
    "Disco Weather": "🎉"
}

# Флаг для продавцов, чтобы писать только 1 раз
seen_sellers = set()

def send_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

def check_stock():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
    except Exception as e:
        print(f"Ошибка API: {e}")
        return

    if data.get("status") != "success":
        return

    stock = data["data"]

    # Traveling Merchant
    merchant = stock.get("travelingmerchant", {})
    if merchant.get("status") == "present":
        name = merchant.get("merchantName", "Unknown")
        if name in RARE_SELLERS and name not in seen_sellers:
            send_message(f"🚨 Редкий продавец появился: <b>{name}</b> 🚨")
            seen_sellers.add(name)

        items = merchant.get("items", [])
        for item in items:
            item_name = item.get("name")
            qty = item.get("qty", 0)
            price = item.get("price", "?")

            if item_name in RARE_ITEMS:
                emoji = RARE_ITEMS[item_name]
                now = datetime.now(BISHKEK_TZ).strftime("%Y-%m-%d %H:%M:%S")
                msg = (
                    f"🔥 В стоке у <b>{name}</b>:\n"
                    f"{emoji} {item_name} x{qty} — 💰 {price}\n\n"
                    f"⏰ {now}"
                )
                send_message(msg)

    # Gear shop (он не продавец, просто редкие предметы)
    gearshop = stock.get("gearshop", {})
    if gearshop.get("status") == "present":
        items = gearshop.get("items", [])
        for item in items:
            item_name = item.get("name")
            qty = item.get("qty", 0)
            price = item.get("price", "?")

            if item_name in RARE_ITEMS:
                emoji = RARE_ITEMS[item_name]
                now = datetime.now(BISHKEK_TZ).strftime("%Y-%m-%d %H:%M:%S")
                msg = (
                    f"🛠 Gear Shop редкий предмет!\n"
                    f"{emoji} {item_name} x{qty} — 💰 {price}\n\n"
                    f"⏰ {now}"
                )
                send_message(msg)

    # Погода
    weather = stock.get("event", {})
    if weather.get("status") == "present":
        items = weather.get("items", [])
        for item in items:
            item_name = item.get("name")
            if item_name in RARE_ITEMS:
                emoji = RARE_ITEMS[item_name]
                now = datetime.now(BISHKEK_TZ).strftime("%Y-%m-%d %H:%M:%S")
                msg = (
                    f"🌦 Редкая погода!\n"
                    f"{emoji} {item_name}\n\n"
                    f"⏰ {now}"
                )
                send_message(msg)

if __name__ == "__main__":
    while True:
        check_stock()
        time.sleep(60)
