import json


def handle_webhook(request):
    payload = json.loads(request.body)
    request_type = request.headers.get("X-GitHub-Event")
    if request_type == "ping":
        return "pong"
    elif request_type == "pull_request":
        return handle_pr(payload)
    elif request_type == "issues":
        return handle_issue(payload)


def handle_pr(payload):
    user = payload["sender"]["login"]
    action = payload["action"]
    if action == "opened":
        action = f"pr_{action}"
    elif action == "closed":
        if payload["pull_request"]["merged"]:
            action = "pr_merged"
        else:
            action = "pr_closed"
    elif action == "reopened":
        action = "pr_reopened"
    return {"user": user, "action": action}


def handle_issue(payload):
    user = payload["sender"]["login"]
    action = payload["action"]
    if action == "opened":
        action = "issue_opened"
    elif action == "closed":
        if payload["issue"]["state_reason"] == "completed":
            action = "issue_completed"
        elif payload["issue"]["state_reason"] == "not_planned":
            action = "issue_not_planned"
    return {"user": user, "action": action}
