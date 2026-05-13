from fastapi import APIRouter, Request
from app.services.github_service import get_pr_files
from app.services.ai_review_service import analyze_code_patch

router = APIRouter()

@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")

    pr = payload.get("pull_request", {})

    title = pr.get("title")
    author = pr.get("user", {}).get("login")
    pr_url = pr.get("html_url")
    pr_number = pr.get("number")

    repo_data = payload.get("repository", {})
    owner = repo_data.get("owner", {}).get("login")
    repo_name = repo_data.get("name")

    print("\n=== Pull Request Event ===")
    print(f"Action: {action}")
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"PR URL: {pr_url}")

    print("\nFetching PR files...")

    files = get_pr_files(owner, repo_name, pr_number)

    for file in files:
        print("\n-------------------")
        print("File:", file.get("filename"))
        print("Status:", file.get("status"))
        print("Additions:", file.get("additions"))
        print("Deletions:", file.get("deletions"))
        print("\nPatch:")
        print(file.get("patch"))
        patch = file.get("patch", "")

        review = analyze_code_patch(patch)

        print("\n=== AI Review ===")
        print(review)

    return {
        "message": "PR processed successfully"
    }