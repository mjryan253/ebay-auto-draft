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
4. IMAP credentials for any email provider  

---

#
##  ⚙️ Configuration

Create a `config/` directory and add:

### `config/input.env`
```dotenv
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_MODE=polling          # or 'webhook'

# IMAP-to-Webhook
IMAP_URL=imap+ssl://user:pass@imap.example.com/?inbox=INBOX&error=Error&success=Processed
IMAP_POLL_INTERVAL=60          # seconds
IMAP_ON_SUCCESS=move           # move or delete
````

### `config/processing.env`

```dotenv
# OpenAI
OPENAI_API_KEY=sk-...

# UPCItemDB
UPC_API_KEY=your_upcitemdb_key

# eBay Sell Listing API
EBAY_CLIENT_ID=...
EBAY_CLIENT_SECRET=...
EBAY_REFRESH_TOKEN=...
EBAY_MARKETPLACE_ID=EBAY_US
```

---

## 🐳 Running the Pipeline

1. **Clone repo**

   ```bash
   git clone <your-repo-url>
   cd project-root
   ```

2. **Populate config**

   ```bash
   mkdir config
   # create input.env and processing.env as above
   ```

3. **Start services**

   ```bash
   docker-compose up -d --build
   ```

4. **(If webhook mode) Set Telegram webhook**

   ```bash
   curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=https://your.domain/webhook/telegram"
   ```

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

## 📄 License

MIT © Your Name

```
```
