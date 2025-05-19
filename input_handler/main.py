import os
import json
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from imap_tools import MailBox, AND

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IMAP_URL = os.getenv("IMAP_URL")
IMAP_INTERVAL = int(os.getenv("IMAP_POLL_INTERVAL", 60))
WEBHOOK_URL = "http://processing-service:8000/process"

# --- TELEGRAM HANDLER ---
async def handle_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.caption or msg.text or ""
    images = []

    if msg.photo:
        for photo in msg.photo:
            file = await photo.get_file()
            images.append(file.file_path)

    payload = {
        "source": "telegram",
        "user_id": str(msg.from_user.id),
        "text": text,
        "images": images
    }

    requests.post(WEBHOOK_URL, json=payload)

# --- IMAP POLLER ---
def poll_email():
    if not IMAP_URL:
        return

    print("[IMAP] Polling...")
    try:
        mb = MailBox(IMAP_URL)
        with mb:
            for msg in mb.fetch(AND(seen=False)):
                images = []
                for att in msg.attachments:
                    if "image" in att.content_type:
                        images.append(f"data:{att.content_type};base64,{att.payload.decode('utf-8')}")

                payload = {
                    "source": "email",
                    "user_id": msg.from_,
                    "text": msg.text or msg.subject,
                    "images": images
                }

                requests.post(WEBHOOK_URL, json=payload)
                mb.move(msg.uid, "Processed")
    except Exception as e:
        print(f"[IMAP Error] {e}")

# --- ENTRYPOINT ---
def main():
    import threading
    if TELEGRAM_TOKEN:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.ALL, handle_telegram))

        threading.Thread(target=app.run_polling).start()

    if IMAP_URL:
        while True:
            poll_email()
            time.sleep(IMAP_INTERVAL)

if __name__ == "__main__":
    main()
