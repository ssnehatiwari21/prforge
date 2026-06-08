import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_pr_files(owner, repo, pr_number):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url, headers=headers)

    print("GET PR FILES:", response.status_code)

    return response.json()


def get_pr_comments(owner, repo, pr_number):

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    response = requests.get(url, headers=headers)

    print("GET COMMENTS:", response.status_code)

    return response.json()


def post_pr_comment(owner, repo, pr_number, comment):

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    response = requests.post(
        url,
        headers=headers,
        json={
            "body": comment
        }
    )

    print("\n========== GITHUB COMMENT ==========")
    print("Status:", response.status_code)
    print(response.text)

    return response.json()


def get_rate_limit():

    url = "https://api.github.com/rate_limit"

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code == 200:
        return response.json().get("rate", {})

    return {}


def get_repo_info(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()