import os
import openai
import requests
import base64
import uuid # Added for SKU generation
from fastapi import FastAPI, Request

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
UPC_API_KEY = os.getenv("UPC_API_KEY")
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")
EBAY_MARKETPLACE_ID = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US") # Default to EBAY_US
EBAY_OAUTH_TOKEN_URL = os.getenv("EBAY_OAUTH_TOKEN_URL", "https://api.sandbox.ebay.com/identity/v1/oauth2/token")
EBAY_API_BASE_URL = os.getenv("EBAY_API_BASE_URL", "https://api.sandbox.ebay.com")

def get_ebay_access_token():
    if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_TOKEN]):
        print("Error: eBay client ID, client secret, or refresh token is not set.")
        return None

    token_url = EBAY_OAUTH_TOKEN_URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode(f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}".encode()).decode()
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment" # Adjust scopes as needed
    }
    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            print(f"Error: Could not retrieve access token. Response: {token_data}")
            return None
        print("Successfully retrieved eBay access token.")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error getting eBay access token: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.content}")
        return None

def create_ebay_inventory_item(access_token, item_sku, title, description):
    if not access_token:
        print("Error: Missing access_token for create_ebay_inventory_item")
        return False

    inventory_item_url = f"{EBAY_API_BASE_URL}/sell/inventory/v1/inventory_item/{item_sku}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Language": "en-US" # Make sure this is appropriate for the target marketplace
    }
    payload = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 1
            }
        },
        "condition": "NEW", # Assuming NEW, this might need to be configurable
        "product": {
            "title": title,
            "description": description,
            # Consider adding brand, mpn, categoryId, imageUrls for better listings
        }
    }
    try:
        print(f"Attempting to create/replace inventory item: {item_sku} with Title: {title}")
        response = requests.put(inventory_item_url, headers=headers, json=payload)
        print(f"eBay Inventory API Response Status: {response.status_code}")
        print(f"eBay Inventory API Response Text: {response.text}")
        response.raise_for_status() # Will raise an exception for 4xx/5xx errors
        # A 200 OK or 204 No Content means success for PUT (create/replace)
        print(f"Successfully created/updated inventory item: {item_sku}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating/updating eBay inventory item {item_sku}: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.content}")
        return False

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    print("[INPUT RECEIVED]", data)

    # 1. Validate and generate content
    user_message_content = [
        {"type": "text", "text": f"Generate a catchy eBay title and bullet-point description for this item: '{data['text']}'"}
    ]

    if data.get("images"):
        for image_data_url in data["images"]:
            # Ensure the image_data_url is a string and starts with "data:image"
            if isinstance(image_data_url, str) and image_data_url.startswith("data:image"):
                user_message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image_data_url}
                })
            else:
                # Log or handle malformed image data if necessary
                print(f"Skipping malformed image data: {image_data_url}")
    
    messages_payload = [
        {"role": "system", "content": "You are a helpful assistant writing eBay listings."},
        {"role": "user", "content": user_message_content}
    ]

    try:
        ai_response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=messages_payload,
            max_tokens=500
        )
        content = ai_response.choices[0].message.content
    except Exception as e:
        return {"error": f"OpenAI error: {str(e)}"}

    # 2. Mock UPC lookup (replace with real UPCItemDB if needed)
    # Simulate enrichment for now
    enriched_data = {
        "category": "Electronics",
        "brand": "GenericBrand",
        "model": "ABC123"
    }

    # 3. Get eBay Access Token
    print("Attempting to get eBay access token...")
    access_token = get_ebay_access_token()
    if not access_token:
        return {"error": "Failed to obtain eBay access token. Check logs and eBay credentials."}
    print(f"eBay Access Token: {access_token[:20]}...")

    # 4. Create eBay Inventory Item
    item_sku = f"ITEM-{str(uuid.uuid4())[:8]}"
    
    # Placeholder for title and description extraction
    # TODO: Refine this based on actual OpenAI output structure
    # Assuming 'content' might be a markdown string with title and bullet points.
    # For now, let's try to split the first line as title and rest as description.
    content_lines = content.strip().split('\n', 1)
    ebay_title = content_lines[0] if content_lines else "Generated Listing Title (Fallback)"
    if len(content_lines) > 1 and content_lines[1].strip():
        ebay_description = content_lines[1].strip()
    else:
        ebay_description = content # Use the full AI content if no clear second part

    if not ebay_title.strip(): # Ensure title is not blank
        ebay_title = f"Item {item_sku}"

    print(f"Extracted Title: {ebay_title}")
    print(f"Extracted Description (first 100 chars): {ebay_description[:100]}...")

    inventory_item_created = create_ebay_inventory_item(access_token, item_sku, ebay_title, ebay_description)

    # 5. Send result back to user
    if inventory_item_created:
        message = f"✅ eBay Inventory Item '{item_sku}' Created/Updated!\nTitle: {ebay_title}\nDescription: {ebay_description[:100]}...\n\nNext step would be to create an offer and publish."
    else:
        message = f"❌ Failed to create eBay inventory item '{item_sku}'. OpenAI Content:\n{content}\n\nCheck logs for details."
    
    # ebay_draft_url = "https://www.ebay.com/draft/xyz123" # Commented out as we are using API

    if data["source"] == "email":
        send_email(data["user_id"], message)

    return {"status": "success" if inventory_item_created else "error", "message": message, "item_sku": item_sku if inventory_item_created else None}

def send_email(to_email, message):
    print(f"[Mock Email to {to_email}]\n{message}")
