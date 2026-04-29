import os
from github import Github

# Use the built-in GitHub Token provided by GitHub Actions
token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')

g = Github(token)
repo = g.get_repo(repo_name)

# Find all open issues
issues = repo.get_issues(state='open')

for issue in issues:
    # Check if the bot has already commented to avoid loops
    comments = issue.get_comments()
    if not any(comment.user.login == "github-actions[bot]" for comment in comments):
        print(f"Processing issue: {issue.title}")
        issue.create_comment("Hello! I am your GitHub Agent. I have seen your issue and recorded it.")
      
