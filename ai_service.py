import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

def get_caption_perplexity(image_bytes: bytes, platform: str, client_name: str) -> str:
    """
    Send image (base64) + prompt to Perplexity for caption generation
    """
    if not PERPLEXITY_API_KEY:
        raise ValueError("PERPLEXITY_API_KEY not found in environment")

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    # Convert image to base64 string
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # JSON body with multimodal input
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional social media caption writer."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Generate a catchy {platform} caption with at least 5 trending hashtags. Brand: {client_name}."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
                ]
            }
        ],
        "max_tokens": 200
    }

    response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Perplexity API error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
