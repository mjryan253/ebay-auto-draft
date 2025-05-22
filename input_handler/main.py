import os
import json
import time
import requests
import threading # Added
from imap_tools import MailBox, AND
from web_server import app as flask_app # Changed import

IMAP_URL = os.getenv("IMAP_URL")
IMAP_INTERVAL = int(os.getenv("IMAP_POLL_INTERVAL", 60))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://processing-service:8000/process") # Updated to use getenv
INPUT_HANDLER_WEB_PORT = os.getenv("INPUT_HANDLER_WEB_PORT", "8080") # Added

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
    # Start Flask app in a new thread
    web_port = int(os.getenv("INPUT_HANDLER_WEB_PORT", "8080"))
    print(f"Starting Flask app on port {web_port} with debug=True, use_reloader=False...")
    flask_thread = threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=web_port, debug=True, use_reloader=False), daemon=True)
    flask_thread.start()

    if IMAP_URL:
        print("IMAP_URL found, starting IMAP poller...")
        # Loop for IMAP polling
        while True:
            poll_email()
            time.sleep(IMAP_INTERVAL)
    else:
        print("No IMAP_URL found. IMAP poller not started.")
        # If no IMAP poller, keep the main thread alive for the Flask thread
        while True:
            time.sleep(3600) # Sleep for an hour, or use another method to keep alive

if __name__ == "__main__":
    main()
