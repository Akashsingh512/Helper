# # linkedin_app.py
# import os
# import json
# import requests
# from fastapi import FastAPI, Request, Form, UploadFile, File
# from fastapi.responses import HTMLResponse, RedirectResponse
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# # LinkedIn App Config
# CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
# CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
# REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

# # In-memory store for access token (use DB in production)
# ACCESS_TOKEN = None
# PERSON_URN = None

# # Step 1: OAuth login
# @app.get("/")
# def home():
#     auth_url = (
#         f"https://www.linkedin.com/oauth/v2/authorization"
#         f"?response_type=code"
#         f"&client_id={CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         f"&scope=w_member_social%20r_liteprofile"
#     )
#     return HTMLResponse(f'<a href="{auth_url}">Login with LinkedIn</a>')

# # Step 2: Callback to exchange code for access token
# @app.get("/linkedin/callback")
# def linkedin_callback(code: str):
#     global ACCESS_TOKEN, PERSON_URN
#     token_url = "https://www.linkedin.com/oauth/v2/accessToken"
#     data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": REDIRECT_URI,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }
#     response = requests.post(token_url, data=data)
#     token_data = response.json()
#     ACCESS_TOKEN = token_data.get("access_token")

#     # Get user URN
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
#     me = requests.get("https://api.linkedin.com/v2/me", headers=headers).json()
#     PERSON_URN = me.get("id")
    
#     return HTMLResponse(f"LinkedIn Connected! Person URN: {PERSON_URN}<br>"
#                         f"Now go to /post to upload image and text.")

# # Step 3: Form to post text + image
# @app.get("/post")
# def post_form():
#     html_content = """
#     <h3>Post on LinkedIn</h3>
#     <form action="/post" enctype="multipart/form-data" method="post">
#         Text: <input name="text" type="text" /><br><br>
#         Image: <input name="image" type="file" /><br><br>
#         <input type="submit" value="Post"/>
#     </form>
#     """
#     return HTMLResponse(html_content)

# # Step 4: Handle form submission and post
# @app.post("/post")
# def post_linkedin(text: str = Form(...), image: UploadFile = File(...)):
#     global ACCESS_TOKEN, PERSON_URN
#     if not ACCESS_TOKEN:
#         return HTMLResponse("Please connect LinkedIn first: <a href='/'>Login</a>")

#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "X-Restli-Protocol-Version": "2.0.0"
#     }

#     # 1️⃣ Register image upload
#     register_payload = {
#         "registerUploadRequest": {
#             "owner": f"urn:li:person:{PERSON_URN}",
#             "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
#             "serviceRelationships": [
#                 {"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
#             ]
#         }
#     }
#     r = requests.post("https://api.linkedin.com/v2/assets?action=registerUpload",
#                       headers={**headers, "Content-Type": "application/json"},
#                       json=register_payload)
#     upload_data = r.json()
#     upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
#     asset_urn = upload_data["value"]["asset"]

#     # 2️⃣ Upload image
#     requests.put(upload_url, data=image.file.read(),
#                  headers={"Authorization": f"Bearer {ACCESS_TOKEN}",
#                           "Content-Type": image.content_type})

#     # 3️⃣ Create post
#     post_payload = {
#         "author": f"urn:li:person:{PERSON_URN}",
#         "lifecycleState": "PUBLISHED",
#         "specificContent": {
#             "com.linkedin.ugc.ShareContent": {
#                 "shareCommentary": {"text": text},
#                 "shareMediaCategory": "IMAGE",
#                 "media": [
#                     {
#                         "status": "READY",
#                         "description": {"text": "Uploaded Image"},
#                         "media": asset_urn,
#                         "title": {"text": "AI Project Image"}
#                     }
#                 ]
#             }
#         },
#         "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
#     }

#     post_response = requests.post(
#         "https://api.linkedin.com/v2/ugcPosts",
#         headers={**headers, "Content-Type": "application/json"},
#         json=post_payload
#     )

#     return HTMLResponse(f"Posted Successfully!<br>{post_response.json()}")

