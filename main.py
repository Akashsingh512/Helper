import os
import re
from fastapi import (
    FastAPI, UploadFile, File, Form, Request, 
    HTTPException
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List as PydanticList
import tempfile

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

# --- Pydantic Models for /save-config ---
class Page(BaseModel):
    name: str
    id: str

class ConfigData(BaseModel):
    companyName: str
    accessToken: str
    pagesList: PydanticList[Page]

# --- App Setup ---
app = FastAPI(title="Perplexity Image Captioning & Config")

# --- Static & Template Setup ---
templates = Jinja2Templates(directory="templates")

def sanitize_filename(name):
    """Takes a string and returns a safe filename."""
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    return safe_name

# def load_client_config(client_name):
#     """Load client configuration from the saved config file."""
#     try:
#         folder_name = "client_configs"
#         filename = f"{sanitize_filename(client_name)}.py"
#         filepath = os.path.join(folder_name, filename)
        
#         if not os.path.exists(filepath):
#             # Try to load from Uploader.py as fallback
#             try:
#                 from Uploader import PAGE_ACCESS_TOKEN, PAGE_ID
#                 return {
#                     "access_token": PAGE_ACCESS_TOKEN,
#                     "pages": [{"name": "Default Page", "id": PAGE_ID}]
#                 }
#             except ImportError:
#                 return None
        
#         # Read and execute the config file
#         config_vars = {}
#         with open(filepath, 'r', encoding='utf-8') as f:
#             exec(f.read(), config_vars)
        
#         return {
#             "access_token": config_vars.get("PAGE_ACCESS_TOKEN"),
#             "pages": config_vars.get("PAGES", [])
#         }
#     except Exception as e:
#         print(f"Error loading config: {e}")
#         return None


def load_client_config(client_name):
    """Load client configuration from the saved config file."""
    try:
        folder_name = "client_configs"
        filename = f"{sanitize_filename(client_name)}.py"
        filepath = os.path.join(folder_name, filename)
        
        if not os.path.exists(filepath):
            # Load from Uploader.py dynamically
            try:
                from Uploader import PAGE_ACCESS_TOKEN, PAGES
                return {
                    "access_token": PAGE_ACCESS_TOKEN,
                    "pages": PAGES  # use all pages from Uploader.py
                }
            except ImportError:
                return None
        
        # Read and execute the config file
        config_vars = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            exec(f.read(), config_vars)
        
        return {
            "access_token": config_vars.get("PAGE_ACCESS_TOKEN"),
            "pages": config_vars.get("PAGES", [])
        }
    except Exception as e:
        print(f"Error loading config: {e}")
        return None



# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serves the main caption generator page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/config", response_class=HTMLResponse)
def config_creator_page(request: Request):
    """Serves the client configuration creator page."""
    return templates.TemplateResponse("init.html", {"request": request})

@app.post("/generate_caption")
async def generate_caption(
    image: UploadFile = File(...),
    platform: str = Form(...),
    client_name: str = Form(...),
    auto_post: bool = Form(False),  # New parameter
    page_id: str = Form(None)  # Optional: specific page to post to
):
    try:
        # Read the image
        image_bytes = await image.read()
        
        # Generate caption
        caption = get_caption_perplexity(image_bytes, platform, client_name)

        # Format caption
        clean_caption = re.split(r"\[\d+\](?:\[\d+\])*", caption)[0].strip()
        parts = clean_caption.split("#")
        main_text = parts[0].strip()
        hashtags = "#".join(parts[1:]).strip()
        formatted_caption = f"{main_text}\n\n#{hashtags}" if hashtags else main_text

        response_data = {
            "platform": platform,
            "client_name": client_name,
            "caption": formatted_caption
        }

        # If auto_post is enabled, post to Facebook
        if auto_post and platform.lower() == "facebook":
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
                    # Determine which page to post to
                    target_page_id = page_id
                    if not target_page_id and client_config["pages"]:
                        # Use first page if no specific page selected
                        target_page_id = client_config["pages"][0]["id"]
                    
                    # Post to Facebook
                    post_result = post_to_facebook(
                        image_path=temp_image_path,
                        caption=formatted_caption,
                        page_access_token=client_config["access_token"],
                        page_id=target_page_id
                    )
                    
                    # Add post result to response
                    if "error" in post_result:
                        response_data["post_error"] = post_result["error"]
                        response_data["post_success"] = False
                    else:
                        response_data["post_success"] = True
                        response_data["post_id"] = post_result.get("id")
                        response_data["post_message"] = "Successfully posted to Facebook!"
                
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
        file_content += f"PAGE_ACCESS_TOKEN = \"{data.accessToken}\"\n\n"
        file_content += "PAGES = [\n"
        for page in data.pagesList:
            file_content += f"    {{\"name\": \"{page.name}\", \"id\": \"{page.id}\"}},\n"
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