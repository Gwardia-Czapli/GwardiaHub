from enum import Enum, auto
import hashlib
import hmac
import json

from gwardia_hub.settings import env

from django.core.handlers.wsgi import WSGIRequest


class PR(Enum):
    OPENED = auto()
    CLOSED = auto()
    MERGED = auto()
    REOPENED = auto()


class Issue(Enum):
    OPENED = auto()
    COMPLETED = auto()
    NOT_PLANNED = auto()


def handle_webhook(request: WSGIRequest):
    payload = json.loads(request.body)
    correct = verify_secret(
        env("GH_WEBHOOK_SECRET"), request.body, request.headers["X-Hub-Signature-256"]
    )
    if not correct:
        print("Invalid signature")
        return
    request_type = request.headers["X-GitHub-Event"]
    user = payload["sender"]["login"]
    action = payload["action"]
    if request_type == "pull_request":
        action = handle_pr(payload, action)
    elif request_type == "issues":
        action = handle_issue(payload, action)
    else:
        return
    # TODO: Implement adding to db
    print(user, action)


def handle_pr(payload, action):
    if action == "opened":
        action = PR.OPENED
    elif action == "closed":
        if ["pull_request"]["merged"]:
            action = PR.MERGED
        else:
            action = PR.CLOSED
    elif action == "reopened":
        action = PR.REOPENED
    return action


def handle_issue(payload, action):
    if action == "opened":
        action = Issue.OPENED
    elif action == "closed":
        state_reason = payload["issue"]["state_reason"]
        if state_reason == "completed":
            action = Issue.COMPLETED
        elif state_reason == "not_planned":
            action = Issue.NOT_PLANNED
    return action


def verify_secret(secret, payload, signature_header):
    hash_object = hmac.new(
        secret.encode("utf-8"), msg=payload, digestmod=hashlib.sha256
    )
    expected_signature = f"sha256={hash_object.hexdigest()}"
    return hmac.compare_digest(expected_signature, signature_header)
