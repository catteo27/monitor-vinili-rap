import requests
from bs4 import BeautifulSoup
import json
import os
from telegram import Bot

TELEGRAM_TOKEN = "8268703478:AAHrGJKkaxfuEp2k3iNIPPah_J6quN2kB1o"
CHAT_ID = "1095947842"

URLS = {
    "Feltrinelli": "https://www.feltrinelli.it/catalogo/musica/vinili/",
    "Universal": "https://www.universalmusicstore.it/it_IT/music",
    "Sony": "https://www.sonymusicshop.it/it_IT/music"
}

KEYWORDS = ["rap", "hip hop", "hip-hop", "vinile", "lp", "33 giri", "italiano"]
SEEN_FILE = "visti.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_seen(data):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def send(msg):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=msg, disable_web_page_preview=True)


def check():
    seen = load_seen()

    for site, url in URLS.items():
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            if not title:
                continue

            text = title.lower()
            if any(k in text for k in KEYWORDS):
                key = site + title
                if key not in seen:
                    seen[key] = a["href"]
                    send(
                        f"🎧 NUOVO VINILE TROVATO\n\n"
                        f"{title}\n"
                        f"Sito: {site}\n"
                        f"{a['href']}"
                    )

    save_seen(seen)


if __name__ == "__main__":
    check()
