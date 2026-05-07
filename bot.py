
import os
import requests
import base64

# Use GitHub Secrets for your PAT in GitHub Actions
GITHUB_TOKEN = os.getenv('MY_GITHUB_PAT') 
USERNAME = "harinathvadla-ship-it"

def build_new_app(app_name, prompt):
    # 1. Ask Gemini/AI to generate HTML code based on the prompt
    # (Simplified for this example)
    generated_html = f"<html><body><h1>{app_name}</h1><p>{prompt}</p></body></html>"
    
    # 2. Create the new Repository
    repo_url = "https://api.github.com/user/repos"
    repo_data = {"name": app_name, "auto_init": True}
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    requests.post(repo_url, json=repo_data, headers=headers)

    # 3. Push index.html to the new repo
    file_url = f"https://api.api.github.com/repos/{USERNAME}/{app_name}/contents/index.html"
    content_encoded = base64.b64encode(generated_html.encode()).decode()
    
    file_data = {
        "message": "Agent created this app",
        "content": content_encoded
    }
    
    response = requests.put(file_url, json=file_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Success! App live at: https://{USERNAME}.github.io/{app_name}/")
