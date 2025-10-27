# main.py 
import os
import re
import json 
from fastapi import (
    FastAPI, UploadFile, File, Form, Request, 
    HTTPException, Response
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List as PydanticList, Optional
import tempfile
from urllib.parse import quote
import base64
from datetime import datetime

# At the top of main.py with other imports
# from Data import extract_all_pages, extract_pages_for_client, get_pages_and_instagram

# Import your services
from ai_service import get_caption_perplexity
import requests

# Facebook posting function
def post_to_facebook(image_path, caption, page_access_token=None, page_id=None):
    """Posts an image with caption to a Facebook page."""
    if not os.path.exists(image_path):
        return {"error": f"Image file not found at path: {image_path}"}
    
    url = f"https://graph.facebook.com/v24.0/{page_id}/photos"
    payload = {"caption": caption, "access_token": page_access_token}
    
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

# --- Pydantic Models ---
class Page(BaseModel):
    name: str
    id: str

class TwitterConfig(BaseModel):
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str

class LinkedInConfig(BaseModel):
    access_token: str
    person_urn: Optional[str] = None
    company_urns: PydanticList[str] = []

class ConfigData(BaseModel):
    companyName: str
    accessToken: Optional[str] = None
    pagesList: PydanticList[Page] = []
    twitterConfig: Optional[TwitterConfig] = None
    linkedinConfig: Optional[LinkedInConfig] = None

class Post(BaseModel):
    id: int
    client_name: str
    scheduled_date: str
    platform: str  # Instagram, Twitter, Facebook, LinkedIn
    content: str
    status: str  # Scheduled, Published

# --- App Setup (ONLY ONE INSTANCE) ---
app = FastAPI(title="Perplexity Image Captioning & Config")

# --- Static & Template Setup ---
templates = Jinja2Templates(directory="templates")

# --- Helper Functions ---
def sanitize_filename(name):
    """Takes a string and returns a safe filename."""
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    return safe_name

def load_client_config(client_name):
    """Load client configuration from the saved config file."""
    try:
        folder_name = "client_configs"
        filename = f"{sanitize_filename(client_name)}.py"
        filepath = os.path.join(folder_name, filename)
        
        if not os.path.exists(filepath):
            # Load from Uploader.py dynamically
            try:
                from Uploader import (
                    PAGE_ACCESS_TOKEN, PAGES,
                    TWITTER_API_KEY, TWITTER_API_SECRET,
                    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
                    LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN
                )
                return {
                    "access_token": PAGE_ACCESS_TOKEN,
                    "pages": PAGES,
                    "twitter": {
                        "api_key": TWITTER_API_KEY,
                        "api_secret": TWITTER_API_SECRET,
                        "access_token": TWITTER_ACCESS_TOKEN,
                        "access_token_secret": TWITTER_ACCESS_TOKEN_SECRET
                    },
                    "linkedin": {
                        "access_token": LINKEDIN_ACCESS_TOKEN,
                        "person_urn": LINKEDIN_PERSON_URN,
                        "company_urns": []
                    }
                }
            except ImportError:
                return None
        
        # Read and execute the config file
        config_vars = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            exec(f.read(), config_vars)
        
        config = {
            "access_token": config_vars.get("PAGE_ACCESS_TOKEN"),
            "pages": config_vars.get("PAGES", [])
        }
        
        # Add Twitter config if available
        if all(key in config_vars for key in ["TWITTER_API_KEY", "TWITTER_API_SECRET", 
                                               "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]):
            config["twitter"] = {
                "api_key": config_vars["TWITTER_API_KEY"],
                "api_secret": config_vars["TWITTER_API_SECRET"],
                "access_token": config_vars["TWITTER_ACCESS_TOKEN"],
                "access_token_secret": config_vars["TWITTER_ACCESS_TOKEN_SECRET"]
            }
        
        # Add LinkedIn config if available
        if config_vars.get("LINKEDIN_ACCESS_TOKEN"):
            config["linkedin"] = {
                "access_token": config_vars["LINKEDIN_ACCESS_TOKEN"],
                "person_urn": config_vars.get("LINKEDIN_PERSON_URN"),
                "company_urns": config_vars.get("LINKEDIN_COMPANY_URNS", [])
            }
        
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

# --- Routes ---

@app.get("/")
def root():
    """Redirect root to the main index page"""
    return RedirectResponse(url="/index")

@app.get("/index", response_class=HTMLResponse)
def index_page(request: Request):
    """Serves the main caption generator page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/config", response_class=HTMLResponse)
def config_creator_page(request: Request):
    """Serves the client configuration creator page."""
    return templates.TemplateResponse("init.html", {"request": request})

@app.get("/Dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    """Serves the dashboard page."""
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.get("/posts", response_class=HTMLResponse)
async def get_posts(request: Request):
    """Serves the scheduler page with posts."""
    # Fetch posts from your database
    # posts = await fetch_posts_from_db()
    return templates.TemplateResponse("scheduler.html", {
        "request": request,
        # "posts": posts
    })

@app.get("/posts/create", response_class=HTMLResponse)
async def create_post_page(request: Request):
    """Serves the create post page."""
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/generate_caption")
async def generate_caption(
    image: UploadFile = File(...),
    platform: str = Form(...),
    client_name: str = Form(...),
    auto_post: bool = Form(False),
    page_id: Optional[str] = Form(None)
):
    try:
        # Read the image
        image_bytes = await image.read()
        
        # Generate caption
        raw_caption = get_caption_perplexity(image_bytes, platform, client_name)
        
        # Advanced caption cleaning
        caption = raw_caption
        
        # Remove common AI meta-text patterns
        meta_patterns = [
            r"Here'?s?\s+(?:a|an)\s+(?:professional|engaging|creative)?\s*(?:caption|post).*?:+\s*",
            r"---+\s*",
            r"\*\*Note:?\*\*.*?(?:\n|$)",
            r"This caption.*?(?:\n|$)",
            r"Feel free.*?(?:\n|$)",
            r"You can.*?(?:\n|$)",
        ]
        
        for pattern in meta_patterns:
            caption = re.sub(pattern, "", caption, flags=re.IGNORECASE)
        
        # Remove citation markers [1], [2][3], etc.
        caption = re.split(r"\[\d+\](?:\[\d+\])*", caption)[0].strip()
        
        # Remove excessive asterisks (markdown bold markers)
        caption = re.sub(r'\*\*([^*]+)\*\*', r'\1', caption)
        
        # Clean up multiple newlines
        caption = re.sub(r'\n{3,}', '\n\n', caption)
        
        # Format caption with hashtags
        parts = caption.split("#")
        main_text = parts[0].strip()
        hashtags = "#".join(parts[1:]).strip()
        formatted_caption = f"{main_text}\n\n#{hashtags}" if hashtags else main_text
        
        # Final cleanup
        formatted_caption = formatted_caption.strip()

        response_data = {
            "platform": platform,
            "client_name": client_name,
            "caption": formatted_caption
        }

        # If auto_post is enabled, post to the selected platform
        if auto_post:
            # Load client config
            client_config = load_client_config(client_name)
            
            if not client_config:
                response_data["post_error"] = "Client configuration not found. Please create config first."
            else:
                # Save image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_file.write(image_bytes)
                    temp_image_path = temp_file.name
                
                try:
                    # Post based on platform
                    if platform.lower() == "facebook":
                        # Determine which page to post to
                        target_page_id = page_id
                        if not target_page_id and client_config["pages"]:
                            target_page_id = client_config["pages"][0]["id"]
                        
                        # Import from Uploader
                        from Uploader import post_to_facebook as fb_post
                        
                        post_result = fb_post(
                            image_path=temp_image_path,
                            caption=formatted_caption,
                            page_access_token=client_config["access_token"],
                            page_id=target_page_id
                        )
                        
                        if "error" in post_result:
                            response_data["post_error"] = post_result["error"]
                            response_data["post_success"] = False
                        else:
                            response_data["post_success"] = True
                            response_data["post_id"] = post_result.get("id")
                            response_data["post_message"] = "Successfully posted to Facebook!"
                    
                    elif platform.lower() == "twitter":
                        if "twitter" not in client_config:
                            response_data["post_error"] = "Twitter configuration not found for this client."
                            response_data["post_success"] = False
                        else:
                            # Import from Uploader
                            from Uploader import post_to_twitter
                            
                            twitter_config = client_config["twitter"]
                            post_result = post_to_twitter(
                                image_path=temp_image_path,
                                caption=formatted_caption,
                                api_key=twitter_config["api_key"],
                                api_secret=twitter_config["api_secret"],
                                access_token=twitter_config["access_token"],
                                access_token_secret=twitter_config["access_token_secret"]
                            )
                            
                            if "error" in post_result:
                                response_data["post_error"] = post_result["error"]
                                response_data["post_success"] = False
                            else:
                                response_data["post_success"] = True
                                response_data["post_id"] = post_result.get("data", {}).get("id")
                                response_data["post_message"] = "Successfully posted to Twitter!"
                    
                    elif platform.lower() == "linkedin":
                        if "linkedin" not in client_config:
                            response_data["post_error"] = "LinkedIn configuration not found for this client."
                            response_data["post_success"] = False
                        else:
                            # Import from Uploader
                            from Uploader import post_to_linkedin, post_to_linkedin_company
                            
                            linkedin_config = client_config["linkedin"]
                            
                            # Check if posting to company page or personal profile
                            company_urns = linkedin_config.get("company_urns", [])
                            person_urn = linkedin_config.get("person_urn")
                            
                            # Priority: Company page first, then personal profile
                            if company_urns and company_urns[0]:
                                # Post to company page
                                print(f"Posting to LinkedIn company page: {company_urns[0]}")
                                post_result = post_to_linkedin_company(
                                    image_path=temp_image_path,
                                    caption=formatted_caption,
                                    company_urn=company_urns[0],
                                    access_token=linkedin_config["access_token"]
                                )
                                post_type = "company page"
                            elif person_urn:
                                # Post to personal profile
                                print(f"Posting to LinkedIn personal profile: {person_urn}")
                                post_result = post_to_linkedin(
                                    image_path=temp_image_path,
                                    caption=formatted_caption,
                                    access_token=linkedin_config["access_token"],
                                    person_urn=person_urn
                                )
                                post_type = "personal profile"
                            else:
                                post_result = {"error": "No LinkedIn URN configured (neither personal nor company)"}
                                post_type = "unknown"
                            
                            if "error" in post_result:
                                response_data["post_error"] = post_result["error"]
                                response_data["post_success"] = False
                            else:
                                response_data["post_success"] = True
                                response_data["post_id"] = post_result.get("id")
                                response_data["post_message"] = f"Successfully posted to LinkedIn ({post_type})!"
                    
                    else:
                        response_data["post_error"] = f"Auto-posting not yet supported for {platform}"
                        response_data["post_success"] = False
                
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save-config")
async def save_config(data: ConfigData):
    """Receives data from the config.html form and saves the file."""
    try:
        file_content = f"# Configuration file for: {data.companyName}\n\n"
        file_content += f"COMPANY_NAME = \"{data.companyName}\"\n"
        
        # Facebook config
        if data.accessToken:
            file_content += f"PAGE_ACCESS_TOKEN = \"{data.accessToken}\"\n\n"
        
        if data.pagesList:
            file_content += "PAGES = [\n"
            for page in data.pagesList:
                file_content += f"    {{\"name\": \"{page.name}\", \"id\": \"{page.id}\"}},\n"
            file_content += "]\n\n"
        
        # Twitter config
        if data.twitterConfig:
            file_content += f"TWITTER_API_KEY = \"{data.twitterConfig.api_key}\"\n"
            file_content += f"TWITTER_API_SECRET = \"{data.twitterConfig.api_secret}\"\n"
            file_content += f"TWITTER_ACCESS_TOKEN = \"{data.twitterConfig.access_token}\"\n"
            file_content += f"TWITTER_ACCESS_TOKEN_SECRET = \"{data.twitterConfig.access_token_secret}\"\n\n"
        
        # LinkedIn config
        if data.linkedinConfig:
            file_content += f"LINKEDIN_ACCESS_TOKEN = \"{data.linkedinConfig.access_token}\"\n"
            if data.linkedinConfig.person_urn:
                file_content += f"LINKEDIN_PERSON_URN = \"{data.linkedinConfig.person_urn}\"\n"
            if data.linkedinConfig.company_urns:
                file_content += "LINKEDIN_COMPANY_URNS = [\n"
                for urn in data.linkedinConfig.company_urns:
                    file_content += f"    \"{urn}\",\n"
                file_content += "]\n"
        
        folder_name = "client_configs"
        filename = f"{sanitize_filename(data.companyName)}.py"
        filepath = os.path.join(folder_name, filename)

        os.makedirs(folder_name, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        return {"success": True, "message": f"Config saved to {filepath}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-client-pages/{client_name}")
async def get_client_pages(client_name: str):
    """Get available pages for a client."""
    try:
        client_config = load_client_config(client_name)
        if not client_config:
            raise HTTPException(status_code=404, detail="Client config not found")
        
        return {"pages": client_config["pages"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/prepare-linkedin-share")
async def prepare_linkedin_share(
    image: UploadFile = File(...),
    caption: str = Form(...)
):
    """
    Prepare caption and provide LinkedIn share URL
    User can then share to personal or company page via LinkedIn UI
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image_bytes = await image.read()
            temp_file.write(image_bytes)
            temp_path = temp_file.name
        
        # Create a shareable link
        share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={quote('https://yourwebsite.com')}"
        
        # For text-only sharing
        text_share_url = f"https://www.linkedin.com/feed/?shareActive=true&text={quote(caption)}"
        
        return {
            "success": True,
            "caption": caption,
            "share_url": text_share_url,
            "image_path": temp_path,
            "instructions": "Click the share button to open LinkedIn. You can then select company page or personal profile."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download-temp-image/{filename}")
async def download_temp_image(filename: str):
    """Allow downloading temporary image for manual upload"""
    try:
        temp_path = f"/tmp/{filename}"
        
        if os.path.exists(temp_path):
            with open(temp_path, "rb") as f:
                image_data = f.read()
            
            return Response(
                content=image_data,
                media_type="image/jpeg",
                headers={
                    "Content-Disposition": f"attachment; filename=linkedin_post.jpg"
                }
            )
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
