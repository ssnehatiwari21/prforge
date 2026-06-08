from fastapi import APIRouter, Request

from app.services.github_service import (
    get_pr_files,
    post_pr_comment
)

from app.services.ai_review_service import (
    analyze_code_patch,
    answer_pr_question
)

from app.database import SessionLocal
from app.models import Review, PRComment

router = APIRouter()


@router.post("/github")
async def github_webhook(request: Request):

    event = request.headers.get("X-GitHub-Event")

    print("\n========== PR WEBHOOK ==========")
    print("GitHub Event:", event)

    if event == "ping":
        return {
            "message": "Webhook connected successfully"
        }

    payload = await request.json()

    action = payload.get("action")

    print("Action:", action)

    if action not in ["opened", "synchronize"]:
        return {
            "message": f"Ignored action: {action}"
        }

    pr = payload.get("pull_request", {})

    title = pr.get("title")
    author = pr.get("user", {}).get("login")
    pr_number = pr.get("number")

    repo_data = payload.get("repository", {})

    owner = repo_data.get("owner", {}).get("login")
    repo_name = repo_data.get("name")

    print(f"Reviewing PR #{pr_number} in {owner}/{repo_name}")

    files = get_pr_files(
        owner,
        repo_name,
        pr_number
    )

    all_reviews = []

    db = SessionLocal()

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch", "")

        if not patch:
            continue

        print(f"Analyzing: {filename}")

        review = analyze_code_patch(patch)

        all_reviews.append(
            f"## {filename}\n\n{review}"
        )

        db.add(
            Review(
                pr_number=pr_number,
                title=title,
                repo=repo_name,
                author=author,
                status="warning",
                review_comment=review
            )
        )

    db.commit()
    db.close()

    final_review = "\n\n".join(all_reviews)

    if final_review.strip():

        print("\n========== POSTING REVIEW ==========")

        post_pr_comment(
            owner,
            repo_name,
            pr_number,
            final_review
        )

    return {
        "message": "PR processed successfully"
    }


@router.post("/github/comments")
async def github_comment_webhook(request: Request):

    github_event = request.headers.get("X-GitHub-Event")

    print("\n========== COMMENT WEBHOOK ==========")
    print("GitHub Event:", github_event)

    if github_event != "issue_comment":
        return {
            "message": "Ignored event"
        }

    payload = await request.json()

    sender = payload.get("sender", {})

    # Ignore bot comments
    if sender.get("login", "").lower() == "prforge" or sender.get("type") == "Bot":
        return {
            "message": "Ignoring bot comment"
        }

    comment_data = payload.get("comment", {})
    comment_body = comment_data.get("body", "")

    print("Comment Body:", comment_body)

    # Bot must be mentioned
    if "@prforge" not in comment_body.lower():
        return {
            "message": "No bot mention"
        }

    IGNORE_PHRASES = [
        "okay thanks",
        "ok thanks",
        "thank you",
        "thanks",
        "👍",
        "got it",
        "noted",
        "sure",
        "okay",
        "ok",
        "great",
        "cool",
        "perfect"
    ]

    if any(
        phrase in comment_body.lower()
        for phrase in IGNORE_PHRASES
    ):
        return {
            "message": "Acknowledgement ignored"
        }

    issue = payload.get("issue", {})
    repo_data = payload.get("repository", {})

    owner = repo_data.get("owner", {}).get("login")
    repo_name = repo_data.get("name")

    pr_number = issue.get("number")

    commenter = sender.get(
        "login",
        "someone"
    )

    print(
        f"Question received from {commenter} on PR #{pr_number}"
    )

    pr_files = get_pr_files(
        owner,
        repo_name,
        pr_number
    )

    file_summaries = "\n".join(
        f"### {f.get('filename')}\n{f.get('patch', '')}"
        for f in pr_files
        if f.get("patch")
    )

    db = SessionLocal()

    # Save user message
    db.add(
        PRComment(
            pr_number=pr_number,
            repo=repo_name,
            role="user",
            message=comment_body
        )
    )

    db.commit()

    # Load conversation history
    history = (
        db.query(PRComment)
        .filter_by(
            pr_number=pr_number,
            repo=repo_name
        )
        .order_by(PRComment.created_at)
        .all()
    )

    print("History Messages:", len(history))
    print("Generating AI response...")

    ai_reply = answer_pr_question(
        history=history,
        pr_files=file_summaries,
        commenter=commenter
    )

    print("\n========== AI REPLY ==========")
    print(ai_reply)

    # Save assistant reply
    db.add(
        PRComment(
            pr_number=pr_number,
            repo=repo_name,
            role="assistant",
            message=ai_reply
        )
    )

    db.commit()
    db.close()

    print("\n========== POSTING COMMENT ==========")

    post_pr_comment(
        owner,
        repo_name,
        pr_number,
        ai_reply
    )

    return {
        "message": "Reply posted successfully"
    }