import os
import openai
import requests
from fastapi import FastAPI, Request

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
UPC_API_KEY = os.getenv("UPC_API_KEY")
EBAY_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")  # Normally use OAuth flow

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    print("[INPUT RECEIVED]", data)

    # 1. Validate and generate content
    prompt = f"Generate a catchy eBay title and bullet-point description for this item: '{data['text']}'"
    if data["images"]:
        prompt += "\nUse context from the images if relevant."

    try:
        ai_response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant writing eBay listings."},
                {"role": "user", "content": prompt}
            ],
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

    # 3. Post to eBay (mocked)
    ebay_draft_url = "https://www.ebay.com/draft/xyz123"

    # 4. Send result back to user
    message = f"✅ eBay Draft Created!\n{content}\n\nView/Edit: {ebay_draft_url}"

    if data["source"] == "email":
        send_email(data["user_id"], message)

    return {"status": "success"}

def send_email(to_email, message):
    print(f"[Mock Email to {to_email}]\n{message}")
