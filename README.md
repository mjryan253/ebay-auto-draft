# eBay Listing Automation

A self-hosted pipeline for automatically creating eBay draft listings from images and text submitted via Telegram or email (IMAP). Built as two core microservices—Input Handler and Processing Service—running in Docker Compose.

---

## 🚀 Features

- **Telegram & Email Intake**  
  - Receive photos and descriptions via Telegram bot (polling or webhook).  
  - Poll any IMAP mailbox and forward new messages (with attachments).  

- **AI Processing & Enrichment**  
  - Validate and enrich using OpenAI’s GPT-4 Vision + UPCItemDB.  
  - Generate eBay-optimized titles and bullet-point descriptions.  

- **eBay Draft Creation**  
  - Manage OAuth2 and call eBay Sell Listing API `createItemDraft`.  
  - Return deep-link to draft for manual review and publishing.  

- **Two-Way Threading**  
  - Replies flow back through the same Telegram chat or email thread.

---

## 📦 Repository Structure

```
/project-root
├── docker-compose.yaml
├── config/
│   ├── input.env
│   └── processing.env
├── input_handler/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── processing_service/
├── Dockerfile
├── main.py
└── requirements.txt
```
---

## 🛠️ Prerequisites

1. Docker & Docker Compose installed  
2. Public IP or domain for Telegram webhooks (if using webhook mode)  
3. Accounts & API keys:  
   - Telegram Bot Token  
   - OpenAI API Key  
   - UPCItemDB API Key  
   - eBay Developer credentials (Client ID, Client Secret, Refresh Token, Marketplace ID)
     - https://developer.ebay.com/join (signup can take 24 hours to be live)
4. IMAP credentials for any email provider  

---

#
##  ⚙️ Configuration

Browse to `config/` directory and edit:

### `config/input.env`
```dotenv
# Telegram
TELEGRAM_BOT_TOKEN=<<your_telegram_bot_token>>
TELEGRAM_MODE=polling          # or 'webhook'

# IMAP-to-Webhook
IMAP_URL=<<imap+ssl://user:pass@imap.example.com/?inbox=INBOX&error=Error&success=Processed>>
IMAP_POLL_INTERVAL=60          # seconds
IMAP_ON_SUCCESS=move           # move or delete
````

### `config/processing.env`

```dotenv
# OpenAI
OPENAI_API_KEY=sk-<<your-key-here>>

# UPCItemDB
UPC_API_KEY=<<your_upcitemdb_key>>

# eBay Sell Listing API
EBAY_CLIENT_ID=<<your-ID-#>>
EBAY_CLIENT_SECRET=<<your-secret>>
EBAY_REFRESH_TOKEN=<<your-token>>
EBAY_MARKETPLACE_ID=EBAY_US
```

---

## 🐳 Running the Pipeline

1. **Clone repo**

   ```bash
   git https://github.com/mjryan253/ebay-auto-draft.git
   cd ebay-auto-draft
   ```

2. **Populate config**

 * Insert variables into their respective places, in both `input.env` and `processing.env` as seen above.

3. **Start services**

   ```bash
   docker-compose up -d --build
   ```

4. **(Optional) Set Telegram webhook**

   ```bash
   curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=https://your.domain/webhook/telegram"
   ```
   * **IMPORTANT** - the default setting is `polling`. If using `webhook`, be sure to update your operating mode in the `input.env` config.

5. **Verify & Test**

   ```bash
   docker-compose logs -f input-handler processing-service
   ```

   * Send a test photo/text via Telegram or email.
   * Confirm draft link is returned in the same channel.

---

## 📚 Further Improvements

* Add retry/backoff and robust error handling
* Integrate logging/monitoring (Prometheus, ELK stack)
* Migrate secrets to Docker secrets or a vault
* Expand eBay API support for inventory/offers

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/xyz`)
5. Open a Pull Request

---

## Donations

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J11F9UA1)


## 📄 License

eBay listing generator docker stack

Copyright (C) 2025  **Matthew Ryan**

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

