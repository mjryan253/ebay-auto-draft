# AI-Powered eBay Listing Generator

## Overview

The AI-Powered eBay Listing Generator is a tool designed to automate and streamline the creation of eBay listings. It leverages the capabilities of OpenAI's GPT-4 Vision API to generate compelling titles and descriptions for your items based on provided text and images. The application supports two primary methods for inputting item data: IMAP (email) and a user-friendly web form.

Built with Python and containerized using Docker, this project aims to simplify your listing process and enhance your productivity on eBay.

## Features

*   **Automated Listing Content:** Generates catchy eBay titles and detailed bullet-point descriptions.
*   **Multi-Modal Input:** Processes both textual descriptions and images to enrich content generation.
*   **IMAP/Email Intake:** Automatically polls a specified IMAP email account for new items. Emails' subject/body are used as descriptions, and image attachments are processed.
*   **Web Form Intake:** Provides an intuitive web interface for manually uploading item images and descriptions.
*   **AI-Powered:** Utilizes OpenAI's GPT-4 Vision API for advanced natural language and image understanding.
*   **Dockerized Deployment:** Comes with `docker-compose` configuration for easy setup and deployment of services.
*   **Extensible Design:** (Currently includes mocked integration points for UPC database lookups and eBay API posting, which can be further developed).

## Prerequisites

*   **Docker and Docker Compose:** Ensure Docker Engine and Docker Compose are installed on your system. Visit the [official Docker website](https://docs.docker.com/get-docker/) for installation instructions.
*   **OpenAI API Key:** Required for accessing the GPT-4 Vision API. Obtainable from your [OpenAI account](https://platform.openai.com/api-keys).
*   **(Optional) IMAP Server Details:** If you plan to use the email intake feature, you'll need the connection URL and credentials for your IMAP email account.
*   **(Optional) eBay Developer Program Credentials:** For future development or enabling live eBay posting, you would need API credentials from the [eBay Developer Program](https://developer.ebay.com/).

## Configuration

All application configuration is managed through the `config/app.env` file. Ensure this file exists in the `config/` directory and is populated with the necessary values as described below.

**Key Environment Variables:**

*   `INPUT_HANDLER_WEB_PORT="8080"`: Port on which the `input-handler` service's web form will be accessible.
*   `WEBHOOK_URL="http://processing-service:8000/process"`: Internal URL used by the `input-handler` to communicate with the `processing-service`. Typically, this should not be changed unless you modify the service names or networking.

**IMAP Configuration (Optional):**
*   `IMAP_URL="imap+ssl://user:pass@imap.example.com/?inbox=INBOX&error=Error&success=Processed"`: Full IMAP connection URL for your email account.
    *   Replace `user:pass@imap.example.com` with your email address and password (or app password).
    *   `inbox=INBOX`: Specifies the mailbox to check.
    *   `error=Error`: Mailbox to move emails to if processing fails.
    *   `success=Processed`: Mailbox to move emails to after successful processing.
*   `IMAP_POLL_INTERVAL="60"`: Interval in seconds between polling the IMAP server for new emails.
*   `IMAP_ON_SUCCESS="move"`: Action to take on an email after successful processing. Can be `move` (to the 'success' mailbox) or `delete`.

**OpenAI Configuration:**
*   `OPENAI_API_KEY=""`: Your OpenAI API key for GPT-4 Vision.

**UPC & eBay Configuration (Functionality for these integrations is currently basic/mocked in the processing logic):**
*   `UPC_API_KEY=""`: API key for UPC database services (e.g., UPCItemDB).
*   `EBAY_CLIENT_ID=""`: Your eBay application Client ID.
*   `EBAY_CLIENT_SECRET=""`: Your eBay application Client Secret.
*   `EBAY_REFRESH_TOKEN=""`: Your eBay refresh token for OAuth.
*   `EBAY_MARKETPLACE_ID="EBAY_US"`: The eBay marketplace ID (e.g., `EBAY_US`, `EBAY_GB`).

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd <repository_directory> # Replace <repository_directory> with the folder name
    ```
2.  **Set up Configuration:**
    *   Navigate to the `config` directory.
    *   Create the `app.env` file if it doesn't exist.
    *   Edit `app.env` and fill in your specific details based on the descriptions in the "Configuration" section above. At a minimum, you'll need to set `OPENAI_API_KEY`. If using email intake, `IMAP_URL` is required.
3.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```
    The `-d` flag runs the services in detached mode. You can omit it to see logs directly in your terminal.
4.  **Check Logs:**
    To view logs from the running services:
    ```bash
    docker-compose logs input-handler
    docker-compose logs processing-service
    ```
    Use `docker-compose logs -f <service_name>` to follow logs in real-time.
5.  **Stopping Services:**
    ```bash
    docker-compose down
    ```

## Usage

Once the services are running, you can submit items for processing using one of the following methods:

**a) Web Form Intake:**
*   **Access:** Open your web browser and navigate to `http://localhost:<INPUT_HANDLER_WEB_PORT>` (e.g., `http://localhost:8080` if `INPUT_HANDLER_WEB_PORT` in `config/app.env` is set to `8080`).
*   **Submit:**
    1.  Enter a detailed description of your item in the "Description" text area.
    2.  Click "Choose Files" (or similar, depending on your browser) to select one or more images of your item.
    3.  Click the "Submit" button.
    4.  You should receive a confirmation message in your browser if the submission was successful.

**b) IMAP (Email) Intake:**
*   **Configuration:** Ensure `IMAP_URL` and other `IMAP_*` variables in `config/app.env` are correctly set up for your email account.
*   **Submit:**
    1.  Compose a new email.
    2.  Use the email subject and/or body for the item's description.
    3.  Attach one or more images of the item directly to the email.
    4.  Send the email to the account configured in `IMAP_URL`.
*   The `input-handler` service will poll this email account at the interval defined by `IMAP_POLL_INTERVAL`. New, unread emails in the specified mailbox will be processed.

## Services Description

The application consists of two main services orchestrated by Docker Compose:

*   **`input-handler`**:
    *   **Purpose:** Manages the intake of item data.
    *   **Functionality:**
        *   Serves a Flask-based web form for manual data entry and image uploads.
        *   Polls a configured IMAP email account for new items.
        *   Prepares the collected data (text, images as base64) and forwards it to the `processing-service`.
    *   **Key Technologies:** Python, Flask, imap_tools.

*   **`processing-service`**:
    *   **Purpose:** Handles the core logic of generating listing content.
    *   **Functionality:**
        *   Receives data from the `input-handler`.
        *   Interacts with the OpenAI GPT-4 Vision API to generate a title and description.
        *   (Currently includes basic/mocked logic for UPC lookups and posting listings to eBay).
    *   **Key Technologies:** Python, FastAPI, OpenAI API.

## License

This project is licensed under the terms of the `LICENSE` file.
```
