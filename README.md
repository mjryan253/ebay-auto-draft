# eBay Listing Automation

A self-hosted pipeline for automatically creating eBay draft listings from images and text submitted via a **web form** or **email (IMAP)**. Built as two core microservices—Input Handler and Processing Service—running in Docker Compose.

---

## 🚀 Features

- **Web Form & Email Intake**
  - Submit items directly through a user-friendly web form.
  - Poll any IMAP mailbox and forward new messages (with attachments).

- **AI Processing & Enrichment**
  - Validate and enrich using OpenAI’s GPT-4 Vision + UPCItemDB.
  - Generate eBay-optimized titles and bullet-point descriptions.

- **eBay Draft Creation**
  - Manage OAuth2 and call eBay Sell Listing API `createItemDraft`.
  - Return deep-link to draft for manual review and publishing.

- **Email Reply**
  - For email submissions, replies (like the draft link) flow back to the same email thread.

---

## 📦 Repository Structure

```
/project-root
├── docker-compose.yaml
├── config/
│   └── app.env  # Consolidated environment variables
├── input_handler/
│   ├── Dockerfile
│   ├── main.py
│   ├── web_server.py
│   ├── requirements.txt
│   └── templates/
│       └── upload_form.html
└── processing_service/
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```
---

## 🛠️ Prerequisites

1. Docker & Docker Compose installed.
2. Accounts & API keys:
   - OpenAI API Key.
   - UPCItemDB API Key (optional, for product enrichment).
   - eBay Developer credentials (Client ID, Client Secret, Refresh Token, Marketplace ID).
     - https://developer.ebay.com/join (signup can take 24 hours to be live).
3. IMAP credentials for any email provider (if using email intake).

---

## ⚙️ Configuration

All configuration is managed via environment variables in the `config/app.env` file. Create this file by copying or renaming `config/app.env.example` (if provided) or by creating it manually.

Below are the key variables:

### `config/app.env`
```dotenv
# --- Input Handler Service ---

# Web Form Configuration
INPUT_HANDLER_WEB_PORT=8080   # Port for the web form interface

# IMAP-to-Webhook (Email Intake)
IMAP_URL=imap+ssl://user:pass@imap.example.com/?inbox=INBOX&error=Error&success=Processed # Set your IMAP server URL, credentials, and folders
IMAP_POLL_INTERVAL=60         # Seconds between email polls
IMAP_ON_SUCCESS=move          # Action after processing: 'move' or 'delete'

# --- Processing Service ---

# OpenAI API for GPT-4 Vision
OPENAI_API_KEY=sk-<<your-openai-key-here>>

# UPCItemDB for product metadata (Optional)
UPC_API_KEY=<<your_upcitemdb_key>>

# eBay Sell Listing API credentials
EBAY_CLIENT_ID=<<your-ebay-client-id>>
EBAY_CLIENT_SECRET=<<your-ebay-client-secret>>
EBAY_REFRESH_TOKEN=<<your-ebay-refresh-token>>
EBAY_MARKETPLACE_ID=EBAY_US   # e.g., EBAY_US, EBAY_GB, etc.

# --- Shared ---
# URL for the processing service (used by input_handler to send data)
# Typically, this is the internal Docker network address.
WEBHOOK_URL=http://processing-service:8000/process
```
*Fill in your actual credentials and settings in `config/app.env`.*

---

## 🐳 Running the Pipeline

1.  **Clone repo**
    ```bash
    git clone https://github.com/mjryan253/ebay-auto-draft.git # Replace with the actual repo URL if different
    cd ebay-auto-draft
    ```

2.  **Populate `config/app.env`**
    *   Create the `config/app.env` file if it doesn't exist.
    *   Fill in all the required environment variables as described in the "Configuration" section.

3.  **Start services**
    ```bash
    docker-compose up -d --build
    ```
    This will build the Docker images and start the `input-handler` and `processing-service` containers. The web form will be accessible on the port specified by `INPUT_HANDLER_WEB_PORT` (default 8080) if mapped in `docker-compose.yaml`.

4.  **Verify & Test**
    *   **Web Form:** Open your browser and navigate to `http://localhost:INPUT_HANDLER_WEB_PORT` (e.g., `http://localhost:8080`). Submit an item with a description and images.
    *   **Email:** Send a test photo/text via email to the configured IMAP account.
    *   Check logs:
        ```bash
        docker-compose logs -f input-handler processing-service
        ```
    *   Confirm the draft link is returned (e.g., in the web form's response or as an email reply).

---

## 📚 Further Improvements

* Add retry/backoff and robust error handling
* Integrate logging/monitoring (Prometheus, ELK stack)
* Migrate secrets to Docker secrets or a vault
* Expand eBay API support for inventory/offers

---

## 🤝 Contributing and Development Path
Check out the evolving document of next-steps.md -> https://github.com/mjryan253/ebay-auto-draft/blob/main/next-steps.md (Update URL if needed)

To contribute to these goals, or add any features of your own, simply:

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
