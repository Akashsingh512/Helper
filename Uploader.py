# import requests
# import os
# import dotenv

# dotenv.load_dotenv()

# # Default credentials - replace with your actual values
# PAGE_NAME = ""
# PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# PAGES = [
#     {"name": "The Kocktail Cafe", "id": "486168597919158"},
#     {"name": "Adeeva Technologies", "id": "542288022301471"}
# ]
# PAGE_ID = "486168597919158"
# if not PAGE_ACCESS_TOKEN:
#     raise ValueError("PAGE_ACCESS_TOKEN is not set in environment variables")

# def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
#     """
#     Posts an image with caption to a Facebook page.
#     """
#     # Use provided tokens or fall back to defaults
#     token = page_access_token or PAGE_ACCESS_TOKEN
#     pid = page_id or PAGE_ID

#     if not os.path.exists(image_path):
#         return {"error": "Image file not found."}

#     url = f"https://graph.facebook.com/v24.0/{pid}/photos"
#     payload = {"caption": caption, "access_token": token}

#     with open(image_path, "rb") as img_file:
#         files = {"source": img_file}
#         try:
#             response = requests.post(url, data=payload, files=files)
#             result = response.json()
#         except Exception as e:
#             result = {"error": str(e)}

#     return result

import requests
import os
import dotenv

dotenv.load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
if not PAGE_ACCESS_TOKEN:
    raise ValueError("PAGE_ACCESS_TOKEN is not set in environment variables")

PAGES = [
    {"name": "The Kocktail Cafe", "id": "486168597919158"},
    {"name": "Adeeva Technologies", "id": "542288022301471"},
    {"name": "Cute Aura Perfumes", "id": "541588492373601"}
]

def get_page_by_name(name):
    for page in PAGES:
        if page["name"] == name:
            return page
    return PAGES[0]  # fallback to first page

def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
    token = page_access_token or PAGE_ACCESS_TOKEN
    pid = page_id or (PAGES[0]["id"] if PAGES else None)

    if not pid:
        return {"error": "No page ID available."}
    if not os.path.exists(image_path):
        return {"error": "Image file not found."}

    url = f"https://graph.facebook.com/v24.0/{pid}/photos"
    payload = {"caption": caption, "access_token": token}

    with open(image_path, "rb") as img_file:
        files = {"source": img_file}
        try:
            response = requests.post(url, data=payload, files=files)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
