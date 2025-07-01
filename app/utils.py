import json
import os

DRAFTS_FILE = "app/storage/drafts.json"

def save_draft(scenario, transcript, email):
    os.makedirs(os.path.dirname(DRAFTS_FILE), exist_ok=True)

    if not os.path.exists(DRAFTS_FILE):
        with open(DRAFTS_FILE, "w") as f:
            json.dump([], f)

    with open(DRAFTS_FILE, "r") as f:
        drafts = json.load(f)

    drafts.append({
        "scenario": scenario,
        "transcript": transcript,
        "email": email
    })

    with open(DRAFTS_FILE, "w") as f:
        json.dump(drafts, f, indent=2)

def get_drafts():
    if not os.path.exists(DRAFTS_FILE):
        return []

    with open(DRAFTS_FILE, "r") as f:
        return json.load(f)
