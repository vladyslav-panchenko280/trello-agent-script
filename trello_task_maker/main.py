#!/usr/bin/env python3
import os
import sys
import time
import json
import hashlib
import requests
import argparse
from jsonschema import validate
from dotenv import load_dotenv
load_dotenv() 

TRELLO_KEY   = os.environ["TRELLO_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]

LISTS = {
    "default": os.environ.get("TRELLO_PLANNING_LIST_ID"),
    "planning": os.environ.get("TRELLO_PLANNING_LIST_ID"),
    "today": os.environ.get("TRELLO_TODAY_LIST_ID"),
    "weekly": os.environ.get("TRELLO_WEEKLY_LIST_ID"),
    "progress": os.environ.get("TRELLO_PROGRESS_LIST_ID"),
    "done": os.environ.get("TRELLO_DONE_LIST_ID"),
}

SCHEMA = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "labels": {"type": "array", "items": {"type": "string"}},
                    "due": {"type": "string"},
                    "external_id": {"type": "string"},
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["tasks"],
}


def trello_get_cards(list_id):
    r = requests.get(
        f"https://api.trello.com/1/lists/{list_id}/cards",
        params={"key": TRELLO_KEY, "token": TRELLO_TOKEN, "fields": "id,name"},
    )
    r.raise_for_status()
    return r.json()


def already_exists(cards_index, external_id):
    marker = f"[EXT:{external_id}]"
    return marker in cards_index


def create_card(task, list_id, max_retries=5):
    marker = f"[EXT:{task.get('external_id', '')}]"
    name = f"{marker} {task['title']}".strip()
    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": list_id,
        "name": name,
        "desc": task.get("description", ""),
        "due": task.get("due", ""),
    }
    for attempt in range(max_retries):
        r = requests.post("https://api.trello.com/1/cards", params=params)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "1"))
            time.sleep(min(30, wait if wait > 0 else 1) * (attempt + 1))
            continue
        if r.status_code >= 500:
            time.sleep(2**attempt)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"Failed to create card after {max_retries} retries")


def ingest(json_payload, list_id):
    validate(instance=json_payload, schema=SCHEMA)
    existing = trello_get_cards(list_id)
    names = " || ".join(c["name"] for c in existing)
    created, skipped = [], []
    for t in json_payload["tasks"]:
        ext = (
            t.get("external_id")
            or hashlib.sha1(f"{t['title']}|{t.get('due', '')}".encode()).hexdigest()[:12]
        )
        t["external_id"] = ext
        if already_exists(names, ext):
            skipped.append(ext)
            continue
        card = create_card(t, list_id)
        created.append({"external_id": ext, "card_id": card["id"]})
    return {"created": created, "skipped": skipped}


def main():
    parser = argparse.ArgumentParser(description="CLI for creating Trello cards from JSON payload")
    parser.add_argument("--list", default="default",
                        help="which list to target (default, planning, today, weekly, progress, done)")
    parser.add_argument("--file", required=True,
                        help="path to JSON file with tasks")
    args = parser.parse_args()

    list_id = LISTS.get(args.list)
    if not list_id:
        sys.stderr.write(f"No LIST_ID configured for {args.list}\n")
        sys.exit(1)

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Failed to read JSON from {args.file}: {e}\n")
        sys.exit(1)

    result = ingest(payload, list_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cli():
    """Entry point for the CLI tool"""
    main()


if __name__ == "__main__":
    main()
