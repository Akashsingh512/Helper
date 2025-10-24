import tkinter as tk
from tkinter import messagebox
import os
import re

def sanitize_filename(name):
    """
    Takes a string and returns a safe filename.
    Replaces spaces with underscores and removes most special characters.
    """
    # Remove invalid characters
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()
    # Replace spaces and hyphens with a single underscore
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    return safe_name

def save_config():
    """
    Get all data from the UI fields and save it to a .py file.
    """
    # 1. Get data from the input fields
    company_name = entry_company.get()
    page_name = entry_page_name.get()
    page_id = entry_page_id.get()
    # Get token from the Text widget (which is multi-line)
    page_token = text_token.get("1.0", "end-1c").strip() # "end-1c" strips the trailing newline

    # 2. Validate input
    if not company_name or not page_name or not page_id or not page_token:
        messagebox.showerror("Error", "All fields are required!")
        return

    # 3. Define folder and filename
    folder_name = "client_configs"
    safe_company_name = sanitize_filename(company_name)
    filename = f"{safe_company_name}.py"
    filepath = os.path.join(folder_name, filename)

    # 4. Create the folder if it doesn't exist
    try:
        os.makedirs(folder_name, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not create directory: {e}")
        return

    # 5. Create the content to be saved
    file_content = f"""# Configuration file for: {company_name}
# Page Name: {page_name}

PAGE_ID = "{page_id}"
PAGE_ACCESS_TOKEN = "{page_token}"
"""

    # 6. Write the file
    try:
        with open(filepath, "w") as f:
            f.write(file_content)
        
        # Show success and clear the form
        messagebox.showinfo("Success", f"Configuration saved to:\n{filepath}")
        entry_company.delete(0, "end")
        entry_page_name.delete(0, "end")
        entry_page_id.delete(0, "end")
        text_token.delete("1.0", "end")
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")


# --- Set up the main UI Window ---
root = tk.Tk()
root.title("Client Page Configuration Saver")

# Create a frame for the form
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# --- UI Elements ---

# Company Name
label_company = tk.Label(frame, text="Client Company Name:")
label_company.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_company = tk.Entry(frame, width=50)
entry_company.grid(row=0, column=1, padx=5, pady=5)

# Page Name
label_page_name = tk.Label(frame, text="Page Name:")
label_page_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_page_name = tk.Entry(frame, width=50)
entry_page_name.grid(row=1, column=1, padx=5, pady=5)

# Page ID
label_page_id = tk.Label(frame, text="Page ID:")
label_page_id.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_page_id = tk.Entry(frame, width=50)
entry_page_id.grid(row=2, column=1, padx=5, pady=5)

# Page Access Token
label_token = tk.Label(frame, text="Page Access Token:")
label_token.grid(row=3, column=0, padx=5, pady=5, sticky="ne") # "ne" = North-East
# Using a Text widget for the token, as it can be very long
text_token = tk.Text(frame, width=50, height=6)
text_token.grid(row=3, column=1, padx=5, pady=5)

# Save Button
save_button = tk.Button(frame, text="Save Configuration", command=save_config, bg="#4CAF50", fg="white", width=20, height=2)
save_button.grid(row=4, column=1, padx=5, pady=15, sticky="e")

# Start the UI event loop
root.mainloop()