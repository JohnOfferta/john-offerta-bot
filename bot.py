import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
import time

# Prende i dati dalle variabili d'ambiente di Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
AFFILIATE_ID = os.getenv("AFFILIATE_ID")

bot = Bot(token=BOT_TOKEN)

def get_amazon_deals():
    url = "https://www.amazon.it/gp/goldbox"  # Pagina offerte Amazon
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    deals = []

    for item in soup.select(".DealCardModule"):
        title_tag = item.select_one(".DealTitle")
        link_tag = item.select_one("a")
        image_tag = item.select_one("img")
        price_tag = item.select_one(".Price")

        if not all([title_tag, link_tag, image_tag, price_tag]):
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag["href"]
        image = image_tag["src"]
        price = price_tag.get_text(strip=True)

        affiliate_link = f"https://www.amazon.it{link}?tag={AFFILIATE_ID}"

        deals.append({
            "title": title,
            "link": affiliate_link,
            "image": image,
            "price": price
        })

    return deals

def send_deals():
    deals = get_amazon_deals()
    for deal in deals:
        message = f"🛒 <b>{deal['title']}</b>\n💸 Prezzo: {deal['price']}\n🔗 <a href='{deal['link']}'>Acquista su Amazon</a>"

        try:
            bot.send_photo(
                chat_id=GROUP_ID,
                photo=deal['image'],
                caption=message,
                parse_mode='HTML'
            )
            time.sleep(5)
        except TelegramError as e:
            print(f"Errore: {e}")

if _name_ == "_main_":
    send_deals()
