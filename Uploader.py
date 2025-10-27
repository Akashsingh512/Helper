# # # Uploader.py which is used to generate captions and post to Facebook pages
# # import requests
# # import os

# # # Default credentials - replace with your actual values
# # PAGE_ACCESS_TOKEN = "EAAZATpmO9h3MBP08gyAY2xKTJ85E0uBq9ZA1QtmO8HBTc9OUULrZAZBzyKtmOlEyVxHnB3r5mcSoZBH8dzyUDFOinNYjMhmxXvpiTJgrraSVfw7yn7ZAE0V7fBwJNF7dHiYJ1u9mtyv9KGb2kBWGwc9tjhEPB5eXZCukx96q9JsAbrjezZAZA6piwTTv16arMGL4wGf4xmdTxvL2tDtH6rpuq"
# # PAGE_ID = "486168597919158"

# # def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
# #     """
# #     Posts an image with caption to a Facebook page.
# #     """
# #     # Use provided tokens or fall back to defaults
# #     token = page_access_token or PAGE_ACCESS_TOKEN
# #     pid = page_id or PAGE_ID

# #     if not os.path.exists(image_path):
# #         return {"error": "Image file not found."}

# #     url = f"https://graph.facebook.com/v24.0/{pid}/photos"
# #     payload = {"caption": caption, "access_token": token}

# #     with open(image_path, "rb") as img_file:
# #         files = {"source": img_file}
# #         try:
# #             response = requests.post(url, data=payload, files=files)
# #             result = response.json()
# #         except Exception as e:
# #             result = {"error": str(e)}

# #     return result


# """
# Uploader.py - Main uploader module for all social media platforms
# This file maintains backward compatibility with your existing code
# """

# import requests
# import os
# from requests_oauthlib import OAuth1
# import time

# # ============================================================================
# # FACEBOOK CONFIGURATION
# # ============================================================================
# PAGE_ACCESS_TOKEN = "EAAZATpmO9h3MBP08gyAY2xKTJ85E0uBq9ZA1QtmO8HBTc9OUULrZAZBzyKtmOlEyVxHnB3r5mcSoZBH8dzyUDFOinNYjMhmxXvpiTJgrraSVfw7yn7ZAE0V7fBwJNF7dHiYJ1u9mtyv9KGb2kBWGwc9tjhEPB5eXZCukx96q9JsAbrjezZAZA6piwTTv16arMGL4wGf4xmdTxvL2tDtH6rpuq"
# PAGE_ID = "486168597919158"
# PAGES = []  # Can be populated with multiple pages

# # ============================================================================
# # TWITTER CONFIGURATION
# # ============================================================================
# TWITTER_API_KEY = "gUVxEf3ySTnbpvrTmUEFazSKI"
# TWITTER_API_SECRET = "3LC4Xkpeodn3LBsa9QpmX6C9ZogOxX2IiFWPBNzSJhm7e6aBOX"
# TWITTER_ACCESS_TOKEN = "1982324681622593536-3FuNaDbKl6Z6EUzInKethuSuowBmrT"
# TWITTER_ACCESS_TOKEN_SECRET = "an1FSaObPz3zNdYO2JaeUJ8fSUOnqXk6ZWJNMcQXng4eB"

# # ============================================================================
# # LINKEDIN CONFIGURATION
# # ============================================================================
# LINKEDIN_ACCESS_TOKEN = "AQWyQ80Fce7rwfiZceHKfBdDGsdYFsBqss4sMPpnUH_E-Ua8wYOA_NhwqXXi1mfZhOHlw_egaRA25d85h8BkeyFFGPHqIezn00Lytg0uMcvBS6sJCUYmGmPW1abA3YsS-5ZQ1ObCX006HYl47noVzLyISlPuO03H931DNGuG4VUUSAi39qIhIP7ShRRi4CclwONUxFH4Z7i4VJDcJUISTwQZPeB913JPkvLIABqyz77N9sCiwjl3tqDcvCclGWEgph8Oo-SDs2Ee9yCte6Ya-Jm_WPcfK1sxTFbsyS23rzxm3y0i-MdB7-GIxHV09aMnQH_0Q1Y1ISIe0ns0gR3Ms1bJoEu3nw"
# LINKEDIN_PERSON_URN = "urn:li:person:YOUR_PERSON_ID"
# LINKEDIN_COMPANY_URNS = []  # List of company page URNs


# # ============================================================================
# # FACEBOOK FUNCTIONS
# # ============================================================================

# def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
#     """
#     Posts an image with caption to a Facebook page.
#     Maintains backward compatibility with your existing code.
#     """
#     token = page_access_token or PAGE_ACCESS_TOKEN
#     pid = page_id or PAGE_ID

#     if not os.path.exists(image_path):
#         return {"error": f"Image file not found at path: {image_path}"}

#     url = f"https://graph.facebook.com/v24.0/{pid}/photos"
#     payload = {"caption": caption, "access_token": token}

#     try:
#         with open(image_path, "rb") as img_file:
#             files = {"source": img_file}
#             response = requests.post(url, data=payload, files=files)
#             result = response.json()
            
#             if "error" in result:
#                 return {
#                     "error": result["error"].get("message", "Unknown Facebook API error"),
#                     "error_code": result["error"].get("code")
#                 }
#             return result
#     except Exception as e:
#         return {"error": f"Error posting to Facebook: {str(e)}"}


# # ============================================================================
# # TWITTER FUNCTIONS
# # ============================================================================

# def upload_media_to_twitter(image_path, api_key=None, api_secret=None, 
#                            access_token=None, access_token_secret=None):
#     """
#     Uploads media to Twitter and returns media_id.
#     """
#     if not os.path.exists(image_path):
#         return None
    
#     key = api_key or TWITTER_API_KEY
#     secret = api_secret or TWITTER_API_SECRET
#     token = access_token or TWITTER_ACCESS_TOKEN
#     token_secret = access_token_secret or TWITTER_ACCESS_TOKEN_SECRET
    
#     url = "https://upload.twitter.com/1.1/media/upload.json"
#     auth = OAuth1(key, client_secret=secret, 
#                   resource_owner_key=token, 
#                   resource_owner_secret=token_secret)
    
#     try:
#         with open(image_path, "rb") as img_file:
#             files = {"media": img_file}
#             response = requests.post(url, files=files, auth=auth)
#             if response.status_code == 200:
#                 return response.json().get("media_id_string")
#     except Exception as e:
#         print(f"Twitter media upload error: {e}")
    
#     return None


# def post_to_twitter(image_path, caption, api_key=None, api_secret=None,
#                    access_token=None, access_token_secret=None):
#     """
#     Posts an image with text to Twitter.
#     """
#     key = api_key or TWITTER_API_KEY
#     secret = api_secret or TWITTER_API_SECRET
#     token = access_token or TWITTER_ACCESS_TOKEN
#     token_secret = access_token_secret or TWITTER_ACCESS_TOKEN_SECRET
    
#     if not os.path.exists(image_path):
#         return {"error": f"Image file not found at path: {image_path}"}
    
#     # Upload the media first
#     media_id = upload_media_to_twitter(image_path, key, secret, token, token_secret)
    
#     if not media_id:
#         return {"error": "Failed to upload media to Twitter"}
    
#     # Create the tweet with the media
#     url = "https://api.twitter.com/2/tweets"
#     auth = OAuth1(key, client_secret=secret,
#                   resource_owner_key=token,
#                   resource_owner_secret=token_secret)
    
#     payload = {
#         "text": caption[:280],  # Twitter character limit
#         "media": {"media_ids": [media_id]}
#     }
    
#     try:
#         response = requests.post(url, json=payload, auth=auth)
#         result = response.json()
        
#         if response.status_code == 201:
#             result["success"] = True
#         elif "errors" in result:
#             result["error"] = result["errors"][0].get("message", "Unknown Twitter error")
        
#         return result
#     except Exception as e:
#         return {"error": f"Error posting to Twitter: {str(e)}"}


# # ============================================================================
# # LINKEDIN FUNCTIONS
# # ============================================================================

# def upload_image_to_linkedin(image_path, author_urn, access_token=None):
#     """
#     Uploads an image to LinkedIn and returns the asset URN.
#     """
#     token = access_token or LINKEDIN_ACCESS_TOKEN
    
#     if not os.path.exists(image_path):
#         return None
    
#     # Step 1: Register the upload
#     register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json"
#     }
    
#     register_payload = {
#         "registerUploadRequest": {
#             "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
#             "owner": author_urn,
#             "serviceRelationships": [{
#                 "relationshipType": "OWNER",
#                 "identifier": "urn:li:userGeneratedContent"
#             }]
#         }
#     }
    
#     try:
#         response = requests.post(register_url, json=register_payload, headers=headers)
#         if response.status_code != 200:
#             print(f"LinkedIn register error: {response.text}")
#             return None
        
#         upload_data = response.json()
#         upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
#         asset_urn = upload_data['value']['asset']
        
#         # Step 2: Upload the image
#         with open(image_path, "rb") as img_file:
#             image_data = img_file.read()
        
#         upload_headers = {"Authorization": f"Bearer {token}"}
#         upload_response = requests.put(upload_url, data=image_data, headers=upload_headers)
        
#         if upload_response.status_code in [200, 201]:
#             return asset_urn
#         else:
#             print(f"LinkedIn upload error: {upload_response.text}")
        
#     except Exception as e:
#         print(f"LinkedIn image upload error: {e}")
    
#     return None


# def post_to_linkedin(image_path, caption, access_token=None, person_urn=None):
#     """
#     Posts an image with text to LinkedIn (personal profile).
#     """
#     token = access_token or LINKEDIN_ACCESS_TOKEN
#     author = person_urn or LINKEDIN_PERSON_URN
    
#     if not os.path.exists(image_path):
#         return {"error": f"Image file not found at path: {image_path}"}
    
#     # Upload the image first
#     asset_urn = upload_image_to_linkedin(image_path, author, token)
    
#     if not asset_urn:
#         return {"error": "Failed to upload image to LinkedIn"}
    
#     # Create the post
#     url = "https://api.linkedin.com/v2/ugcPosts"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json",
#         "X-Restli-Protocol-Version": "2.0.0"
#     }
    
#     payload = {
#         "author": author,
#         "lifecycleState": "PUBLISHED",
#         "specificContent": {
#             "com.linkedin.ugc.ShareContent": {
#                 "shareCommentary": {
#                     "text": caption
#                 },
#                 "shareMediaCategory": "IMAGE",
#                 "media": [{
#                     "status": "READY",
#                     "media": asset_urn
#                 }]
#             }
#         },
#         "visibility": {
#             "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
#         }
#     }
    
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         result = response.json() if response.text else {"status": response.status_code}
        
#         if response.status_code == 201:
#             result["success"] = True
#         elif "message" in result:
#             result["error"] = result["message"]
        
#         return result
#     except Exception as e:
#         return {"error": f"Error posting to LinkedIn: {str(e)}"}


# def post_to_linkedin_company(image_path, caption, company_urn, access_token=None):
#     """
#     Posts an image with text to a LinkedIn company page.
#     """
#     token = access_token or LINKEDIN_ACCESS_TOKEN
    
#     if not os.path.exists(image_path):
#         return {"error": f"Image file not found at path: {image_path}"}
    
#     # Upload the image first
#     asset_urn = upload_image_to_linkedin(image_path, company_urn, token)
    
#     if not asset_urn:
#         return {"error": "Failed to upload image to LinkedIn"}
    
#     # Create the post
#     url = "https://api.linkedin.com/v2/ugcPosts"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json",
#         "X-Restli-Protocol-Version": "2.0.0"
#     }
    
#     payload = {
#         "author": company_urn,
#         "lifecycleState": "PUBLISHED",
#         "specificContent": {
#             "com.linkedin.ugc.ShareContent": {
#                 "shareCommentary": {
#                     "text": caption
#                 },
#                 "shareMediaCategory": "IMAGE",
#                 "media": [{
#                     "status": "READY",
#                     "media": asset_urn
#                 }]
#             }
#         },
#         "visibility": {
#             "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
#         }
#     }
    
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         result = response.json() if response.text else {"status": response.status_code}
        
#         if response.status_code == 201:
#             result["success"] = True
#             result["company_urn"] = company_urn
#         elif "message" in result:
#             result["error"] = result["message"]
        
#         return result
#     except Exception as e:
#         return {"error": f"Error posting to LinkedIn company: {str(e)}"}


# def post_to_multiple_linkedin_companies(image_path, caption, company_urns=None, access_token=None):
#     """
#     Posts an image with text to multiple LinkedIn company pages.
#     """
#     urns = company_urns or LINKEDIN_COMPANY_URNS
    
#     if not urns:
#         return {"error": "No company URNs provided"}
    
#     results = []
    
#     for company_urn in urns:
#         result = post_to_linkedin_company(image_path, caption, company_urn, access_token)
#         results.append({
#             "company_urn": company_urn,
#             "result": result
#         })
#         # Add delay to avoid rate limiting
#         time.sleep(1)
    
#     return results


# # ============================================================================
# # MULTI-PLATFORM FUNCTION
# # ============================================================================

# def post_to_all_platforms(image_path, caption, platforms_config):
#     """
#     Posts to multiple social media platforms based on configuration.
    
#     Args:
#         image_path (str): Path to the image file
#         caption (str): Post text/caption
#         platforms_config (dict): Configuration for each platform
    
#     Returns:
#         dict: Results from each platform
#     """
#     results = {}
    
#     # Facebook
#     if platforms_config.get('facebook', {}).get('enabled', False):
#         fb_config = platforms_config['facebook']
#         results['facebook'] = post_to_facebook(
#             image_path,
#             caption,
#             page_access_token=fb_config.get('page_access_token'),
#             page_id=fb_config.get('page_id')
#         )
    
#     # Twitter
#     if platforms_config.get('twitter', {}).get('enabled', False):
#         tw_config = platforms_config['twitter']
#         results['twitter'] = post_to_twitter(
#             image_path,
#             caption,
#             api_key=tw_config.get('api_key'),
#             api_secret=tw_config.get('api_secret'),
#             access_token=tw_config.get('access_token'),
#             access_token_secret=tw_config.get('access_token_secret')
#         )
    
#     # LinkedIn Personal
#     if platforms_config.get('linkedin', {}).get('enabled', False):
#         li_config = platforms_config['linkedin']
        
#         if li_config.get('post_to_personal', False):
#             results['linkedin_personal'] = post_to_linkedin(
#                 image_path,
#                 caption,
#                 access_token=li_config.get('access_token'),
#                 person_urn=li_config.get('person_urn')
#             )
        
#         # LinkedIn Companies
#         if 'company_urns' in li_config and li_config['company_urns']:
#             results['linkedin_companies'] = post_to_multiple_linkedin_companies(
#                 image_path,
#                 caption,
#                 company_urns=li_config['company_urns'],
#                 access_token=li_config.get('access_token')
#             )
    
#     return results















































"""
Uploader.py - Main uploader module for all social media platforms
This file maintains backward compatibility with your existing code
Now supports loading credentials from .env file
"""

import requests
import os
from requests_oauthlib import OAuth1
import time
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# FACEBOOK CONFIGURATION
# ============================================================================
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "EAAZATpmO9h3MBP08gyAY2xKTJ85E0uBq9ZA1QtmO8HBTc9OUULrZAZBzyKtmOlEyVxHnB3r5mcSoZBH8dzyUDFOinNYjMhmxXvpiTJgrraSVfw7yn7ZAE0V7fBwJNF7dHiYJ1u9mtyv9KGb2kBWGwc9tjhEPB5eXZCukx96q9JsAbrjezZAZA6piwTTv16arMGL4wGf4xmdTxvL2tDtH6rpuq")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "486168597919158")
PAGES = []  # Can be populated with multiple pages

# ============================================================================
# TWITTER CONFIGURATION
# ============================================================================
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "gUVxEf3ySTnbpvrTmUEFazSKI")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "3LC4Xkpeodn3LBsa9QpmX6C9ZogOxX2IiFWPBNzSJhm7e6aBOX")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "1982324681622593536-3FuNaDbKl6Z6EUzInKethuSuowBmrT")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "an1FSaObPz3zNdYO2JaeUJ8fSUOnqXk6ZWJNMcQXng4eB")

# ============================================================================
# LINKEDIN CONFIGURATION
# ============================================================================
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "AQWyQ80Fce7rwfiZceHKfBdDGsdYFsBqss4sMPpnUH_E-Ua8wYOA_NhwqXXi1mfZhOHlw_egaRA25d85h8BkeyFFGPHqIezn00Lytg0uMcvBS6sJCUYmGmPW1abA3YsS-5ZQ1ObCX006HYl47noVzLyISlPuO03H931DNGuG4VUUSAi39qIhIP7ShRRi4CclwONUxFH4Z7i4VJDcJUISTwQZPeB913JPkvLIABqyz77N9sCiwjl3tqDcvCclGWEgph8Oo-SDs2Ee9yCte6Ya-Jm_WPcfK1sxTFbsyS23rzxm3y0i-MdB7-GIxHV09aMnQH_0Q1Y1ISIe0ns0gR3Ms1bJoEu3nw")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "urn:li:person:YOUR_PERSON_ID")
LINKEDIN_COMPANY_URNS = []  # List of company page URNs

# ============================================================================
# PERPLEXITY API CONFIGURATION
# ============================================================================
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")


# ============================================================================
# FACEBOOK FUNCTIONS
# ============================================================================

def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
    """
    Posts an image with caption to a Facebook page.
    Maintains backward compatibility with your existing code.
    """
    token = page_access_token or PAGE_ACCESS_TOKEN
    pid = page_id or PAGE_ID

    if not os.path.exists(image_path):
        return {"error": f"Image file not found at path: {image_path}"}

    url = f"https://graph.facebook.com/v24.0/{pid}/photos"
    payload = {"caption": caption, "access_token": token}

    try:
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files)
            result = response.json()
            
            if "error" in result:
                return {
                    "error": result["error"].get("message", "Unknown Facebook API error"),
                    "error_code": result["error"].get("code")
                }
            return result
    except Exception as e:
        return {"error": f"Error posting to Facebook: {str(e)}"}


# ============================================================================
# TWITTER FUNCTIONS
# ============================================================================

def upload_media_to_twitter(image_path, api_key=None, api_secret=None, 
                           access_token=None, access_token_secret=None):
    """
    Uploads media to Twitter and returns media_id.
    Uses chunked upload for better reliability.
    """
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return None
    
    key = api_key or TWITTER_API_KEY
    secret = api_secret or TWITTER_API_SECRET
    token = access_token or TWITTER_ACCESS_TOKEN
    token_secret = access_token_secret or TWITTER_ACCESS_TOKEN_SECRET
    
    auth = OAuth1(key, client_secret=secret, 
                  resource_owner_key=token, 
                  resource_owner_secret=token_secret)
    
    try:
        # Get file size and type
        file_size = os.path.getsize(image_path)
        mime_type = 'image/jpeg'
        
        # Determine MIME type based on extension
        if image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith('.gif'):
            mime_type = 'image/gif'
        elif image_path.lower().endswith('.webp'):
            mime_type = 'image/webp'
        
        print(f"Uploading image: size={file_size}, type={mime_type}")
        
        # INIT - Initialize upload
        init_url = "https://upload.twitter.com/1.1/media/upload.json"
        init_data = {
            'command': 'INIT',
            'total_bytes': file_size,
            'media_type': mime_type,
            'media_category': 'tweet_image'
        }
        
        init_response = requests.post(init_url, data=init_data, auth=auth)
        print(f"INIT Response: {init_response.status_code} - {init_response.text}")
        
        if init_response.status_code != 202:
            print(f"Twitter INIT failed: {init_response.text}")
            return None
        
        media_id = init_response.json().get('media_id_string')
        
        # APPEND - Upload file in chunks
        with open(image_path, 'rb') as img_file:
            segment_index = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            while True:
                chunk = img_file.read(chunk_size)
                if not chunk:
                    break
                
                append_url = "https://upload.twitter.com/1.1/media/upload.json"
                append_data = {
                    'command': 'APPEND',
                    'media_id': media_id,
                    'segment_index': segment_index
                }
                append_files = {'media': chunk}
                
                append_response = requests.post(append_url, data=append_data, 
                                               files=append_files, auth=auth)
                print(f"APPEND Response {segment_index}: {append_response.status_code}")
                
                if append_response.status_code not in [200, 201, 204]:
                    print(f"Twitter APPEND failed: {append_response.text}")
                    return None
                
                segment_index += 1
        
        # FINALIZE - Complete upload
        finalize_url = "https://upload.twitter.com/1.1/media/upload.json"
        finalize_data = {
            'command': 'FINALIZE',
            'media_id': media_id
        }
        
        finalize_response = requests.post(finalize_url, data=finalize_data, auth=auth)
        print(f"FINALIZE Response: {finalize_response.status_code} - {finalize_response.text}")
        
        if finalize_response.status_code in [200, 201]:
            result = finalize_response.json()
            
            # Check if processing is required
            processing_info = result.get('processing_info')
            if processing_info:
                state = processing_info.get('state')
                
                # Wait for processing to complete
                while state in ['pending', 'in_progress']:
                    check_after_secs = processing_info.get('check_after_secs', 1)
                    print(f"Media processing: {state}, waiting {check_after_secs}s...")
                    time.sleep(check_after_secs)
                    
                    # STATUS - Check processing status
                    status_url = "https://upload.twitter.com/1.1/media/upload.json"
                    status_params = {
                        'command': 'STATUS',
                        'media_id': media_id
                    }
                    status_response = requests.get(status_url, params=status_params, auth=auth)
                    
                    if status_response.status_code == 200:
                        status_result = status_response.json()
                        processing_info = status_result.get('processing_info', {})
                        state = processing_info.get('state', 'succeeded')
                    else:
                        break
                
                if state == 'failed':
                    error = processing_info.get('error', {})
                    print(f"Media processing failed: {error}")
                    return None
            
            return media_id
        else:
            print(f"Twitter FINALIZE failed: {finalize_response.text}")
            return None
            
    except Exception as e:
        print(f"Twitter media upload error: {e}")
        import traceback
        traceback.print_exc()
    
    return None


def post_to_twitter(image_path, caption, api_key=None, api_secret=None,
                   access_token=None, access_token_secret=None):
    """
    Posts an image with text to Twitter.
    """
    key = api_key or TWITTER_API_KEY
    secret = api_secret or TWITTER_API_SECRET
    token = access_token or TWITTER_ACCESS_TOKEN
    token_secret = access_token_secret or TWITTER_ACCESS_TOKEN_SECRET
    
    if not os.path.exists(image_path):
        return {"error": f"Image file not found at path: {image_path}"}
    
    # Upload the media first
    print("Starting Twitter media upload...")
    media_id = upload_media_to_twitter(image_path, key, secret, token, token_secret)
    
    if not media_id:
        return {"error": "Failed to upload media to Twitter. Check credentials and image file."}
    
    print(f"Media uploaded successfully. Media ID: {media_id}")
    
    # Create the tweet with the media
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(key, client_secret=secret,
                  resource_owner_key=token,
                  resource_owner_secret=token_secret)
    
    payload = {
        "text": caption[:280],  # Twitter character limit
        "media": {"media_ids": [media_id]}
    }
    
    try:
        response = requests.post(url, json=payload, auth=auth)
        print(f"Tweet Response: {response.status_code} - {response.text}")
        result = response.json()
        
        if response.status_code == 201:
            result["success"] = True
        elif "errors" in result:
            result["error"] = result["errors"][0].get("message", "Unknown Twitter error")
        elif "detail" in result:
            result["error"] = result["detail"]
        
        return result
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return {"error": f"Error posting to Twitter: {str(e)}"}


# ============================================================================
# LINKEDIN FUNCTIONS
# ============================================================================

def upload_image_to_linkedin(image_path, author_urn, access_token=None):
    """
    Uploads an image to LinkedIn and returns the asset URN.
    """
    token = access_token or LINKEDIN_ACCESS_TOKEN
    
    if not os.path.exists(image_path):
        return None
    
    # Step 1: Register the upload
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": author_urn,
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }
    
    try:
        response = requests.post(register_url, json=register_payload, headers=headers)
        if response.status_code != 200:
            print(f"LinkedIn register error: {response.text}")
            return None
        
        upload_data = response.json()
        upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_urn = upload_data['value']['asset']
        
        # Step 2: Upload the image
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
        
        upload_headers = {"Authorization": f"Bearer {token}"}
        upload_response = requests.put(upload_url, data=image_data, headers=upload_headers)
        
        if upload_response.status_code in [200, 201]:
            return asset_urn
        else:
            print(f"LinkedIn upload error: {upload_response.text}")
        
    except Exception as e:
        print(f"LinkedIn image upload error: {e}")
    
    return None


def post_to_linkedin(image_path, caption, access_token=None, person_urn=None):
    """
    Posts an image with text to LinkedIn (personal profile).
    """
    token = access_token or LINKEDIN_ACCESS_TOKEN
    author = person_urn or LINKEDIN_PERSON_URN
    
    if not os.path.exists(image_path):
        return {"error": f"Image file not found at path: {image_path}"}
    
    # Upload the image first
    asset_urn = upload_image_to_linkedin(image_path, author, token)
    
    if not asset_urn:
        return {"error": "Failed to upload image to LinkedIn"}
    
    # Create the post
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": caption
                },
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "media": asset_urn
                }]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json() if response.text else {"status": response.status_code}
        
        if response.status_code == 201:
            result["success"] = True
        elif "message" in result:
            result["error"] = result["message"]
        
        return result
    except Exception as e:
        return {"error": f"Error posting to LinkedIn: {str(e)}"}


def post_to_linkedin_company(image_path, caption, company_urn, access_token=None):
    """
    Posts an image with text to a LinkedIn company page.
    """
    token = access_token or LINKEDIN_ACCESS_TOKEN
    
    if not os.path.exists(image_path):
        return {"error": f"Image file not found at path: {image_path}"}
    
    # Upload the image first
    asset_urn = upload_image_to_linkedin(image_path, company_urn, token)
    
    if not asset_urn:
        return {"error": "Failed to upload image to LinkedIn"}
    
    # Create the post
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "author": company_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": caption
                },
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "media": asset_urn
                }]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json() if response.text else {"status": response.status_code}
        
        if response.status_code == 201:
            result["success"] = True
            result["company_urn"] = company_urn
        elif "message" in result:
            result["error"] = result["message"]
        
        return result
    except Exception as e:
        return {"error": f"Error posting to LinkedIn company: {str(e)}"}


def post_to_multiple_linkedin_companies(image_path, caption, company_urns=None, access_token=None):
    """
    Posts an image with text to multiple LinkedIn company pages.
    """
    urns = company_urns or LINKEDIN_COMPANY_URNS
    
    if not urns:
        return {"error": "No company URNs provided"}
    
    results = []
    
    for company_urn in urns:
        result = post_to_linkedin_company(image_path, caption, company_urn, access_token)
        results.append({
            "company_urn": company_urn,
            "result": result
        })
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    return results


# ============================================================================
# MULTI-PLATFORM FUNCTION
# ============================================================================

def post_to_all_platforms(image_path, caption, platforms_config):
    """
    Posts to multiple social media platforms based on configuration.
    
    Args:
        image_path (str): Path to the image file
        caption (str): Post text/caption
        platforms_config (dict): Configuration for each platform
    
    Returns:
        dict: Results from each platform
    """
    results = {}
    
    # Facebook
    if platforms_config.get('facebook', {}).get('enabled', False):
        fb_config = platforms_config['facebook']
        results['facebook'] = post_to_facebook(
            image_path,
            caption,
            page_access_token=fb_config.get('page_access_token'),
            page_id=fb_config.get('page_id')
        )
    
    # Twitter
    if platforms_config.get('twitter', {}).get('enabled', False):
        tw_config = platforms_config['twitter']
        results['twitter'] = post_to_twitter(
            image_path,
            caption,
            api_key=tw_config.get('api_key'),
            api_secret=tw_config.get('api_secret'),
            access_token=tw_config.get('access_token'),
            access_token_secret=tw_config.get('access_token_secret')
        )
    
    # LinkedIn Personal
    if platforms_config.get('linkedin', {}).get('enabled', False):
        li_config = platforms_config['linkedin']
        
        if li_config.get('post_to_personal', False):
            results['linkedin_personal'] = post_to_linkedin(
                image_path,
                caption,
                access_token=li_config.get('access_token'),
                person_urn=li_config.get('person_urn')
            )
        
        # LinkedIn Companies
        if 'company_urns' in li_config and li_config['company_urns']:
            results['linkedin_companies'] = post_to_multiple_linkedin_companies(
                image_path,
                caption,
                company_urns=li_config['company_urns'],
                access_token=li_config.get('access_token')
            )
    
    return results