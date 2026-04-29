import os
import google.generativeai as genai
from github import Github

# 1. Setup GitHub and Gemini
# These variables are pulled from your GitHub Secrets
token = os.getenv('GITHUB_TOKEN')
gemini_key = os.getenv('GEMINI_API_KEY')
repo_name = os.getenv('GITHUB_REPOSITORY')

# Authenticate
g = Github(token)
repo = g.get_repo(repo_name)
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Find and respond to new issues
issues = repo.get_issues(state='open')

for issue in issues:
    # Get all comments on this issue
    comments = issue.get_comments()
    
    # Check if the bot has already replied
    if not any(comment.user.login == "github-actions[bot]" for comment in comments):
        print(f"OMNI-ULTRA is thinking about: {issue.title}")
        
        # Create a prompt for Gemini
        prompt = (
            f"You are the OMNI-ULTRA AI Agent. Respond to this issue professionally.\n"
            f"Issue Title: {issue.title}\n"
            f"Issue Description: {issue.body}"
        )
        
        # Generate the AI response
        try:
            response = model.generate_content(prompt)
            reply_text = response.text
        except Exception as e:
            reply_text = "I encountered an error while processing this request."

        # Post the comment back to GitHub
        issue.create_comment(f"### 🤖 OMNI-ULTRA AI Response\n\n{reply_text}")
