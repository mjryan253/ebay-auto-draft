# eBay Auto-Draft

## Overview
eBay Auto-Draft is a **Docker-based automation tool** designed to streamline the process of listing items on eBay. It automates the intake of text and photos, generates optimized descriptions and titles, and publishes draft listings directly to eBay.

## Features
- **Automated Item Intake**: Upload text and images for an item, and the system processes them automatically.
- **Title & Description Generation**: AI-powered content creation ensures compelling and accurate listings.
- **Draft Publishing**: Seamlessly pushes listings to eBay as drafts for review and finalization.
- **Docker-Based Deployment**: Easily deployable using Docker for a consistent and scalable setup.

## Installation
### Prerequisites
- Docker installed on your system
- eBay API credentials

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mjryan253/ebay-auto-draft.git
   cd ebay-auto-draft
   ```
2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```
3. Configure your eBay API credentials in the environment variables.

## Usage
1. Upload item details (text and images).
2. The system processes the input and generates a listing.
3. Review and finalize the draft before publishing.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the **GPL-3.0** license.

---
