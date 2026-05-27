#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API_ROOT = "https://api.trello.com/1"


def main():
    parser = argparse.ArgumentParser(description="Small Trello API helper for Codex skills.")
    parser.add_argument("--config", help="Path to trello.json config")
    parser.add_argument("--board", help="Board id, short link, URL, or configured alias")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("board", help="Show the resolved board")
    sub.add_parser("lists", help="List board lists")
    sub.add_parser("labels", help="List board labels")

    cards = sub.add_parser("cards", help="List cards on the board")
    cards.add_argument("--list", dest="list_ref", help="Filter by list id or exact list name")
    cards.add_argument("--all", action="store_true", help="Include closed cards")

    card = sub.add_parser("card", help="Show one card")
    card.add_argument("card")
    card.add_argument("--actions", action="store_true", help="Include comment actions")
    card.add_argument("--attachments", action="store_true", help="Include attachments")

    create = sub.add_parser("create-card", help="Create a card")
    create.add_argument("--list", dest="list_ref", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--desc", default="")
    create.add_argument("--pos", default="bottom")
    create.add_argument("--due")
    create.add_argument("--labels", help="Comma-separated label ids")

    move = sub.add_parser("move-card", help="Move a card to a list")
    move.add_argument("--card", required=True)
    move.add_argument("--list", dest="list_ref", required=True)

    comment = sub.add_parser("comment", help="Add a comment to a card")
    comment.add_argument("--card", required=True)
    comment.add_argument("--text", required=True)

    attach = sub.add_parser("attach", help="Attach a local file to a card")
    attach.add_argument("--card", required=True)
    attach.add_argument("--file", required=True)
    attach.add_argument("--name")

    archive = sub.add_parser("archive", help="Archive a card")
    archive.add_argument("--card", required=True)

    checklist = sub.add_parser("add-checklist", help="Add a checklist and optional items")
    checklist.add_argument("--card", required=True)
    checklist.add_argument("--name", required=True)
    checklist.add_argument("--item", action="append", default=[])

    args = parser.parse_args()
    config = load_config(args.config)
    client = TrelloClient(config)
    board_ref = resolve_board_ref(args.board, config)

    if args.command == "board":
        output(client.board(board_ref), args)
    elif args.command == "lists":
        output(client.lists(board_ref), args)
    elif args.command == "labels":
        output(client.labels(board_ref), args)
    elif args.command == "cards":
        cards_out = client.cards(board_ref, include_closed=args.all)
        if args.list_ref:
            list_obj = resolve_list(client, board_ref, args.list_ref)
            cards_out = [card for card in cards_out if card.get("idList") == list_obj["id"]]
        output(cards_out, args)
    elif args.command == "card":
        card_obj = resolve_card(client, board_ref, args.card)
        fields = "name,url,desc,idList,closed,due,dateLastActivity,labels"
        params = {"fields": fields}
        if args.actions:
            params["actions"] = "commentCard"
        if args.attachments:
            params["attachments"] = "true"
        output(client.get(f"/cards/{card_obj['id']}", params), args)
    elif args.command == "create-card":
        list_obj = resolve_list(client, board_ref, args.list_ref)
        data = {
            "idList": list_obj["id"],
            "name": args.name,
            "desc": args.desc,
            "pos": args.pos,
        }
        if args.due:
            data["due"] = args.due
        if args.labels:
            data["idLabels"] = args.labels
        output(client.post("/cards", data), args)
    elif args.command == "move-card":
        card_obj = resolve_card(client, board_ref, args.card)
        list_obj = resolve_list(client, board_ref, args.list_ref)
        output(client.put(f"/cards/{card_obj['id']}", {"idList": list_obj["id"]}), args)
    elif args.command == "comment":
        card_obj = resolve_card(client, board_ref, args.card)
        output(client.post(f"/cards/{card_obj['id']}/actions/comments", {"text": args.text}), args)
    elif args.command == "attach":
        card_obj = resolve_card(client, board_ref, args.card)
        output(client.attach(card_obj["id"], args.file, args.name), args)
    elif args.command == "archive":
        card_obj = resolve_card(client, board_ref, args.card)
        output(client.put(f"/cards/{card_obj['id']}", {"closed": "true"}), args)
    elif args.command == "add-checklist":
        card_obj = resolve_card(client, board_ref, args.card)
        checklist_obj = client.post(f"/cards/{card_obj['id']}/checklists", {"name": args.name})
        for item in args.item:
            client.post(f"/checklists/{checklist_obj['id']}/checkItems", {"name": item, "pos": "bottom"})
        output(client.get(f"/checklists/{checklist_obj['id']}"), args)


class TrelloClient:
    def __init__(self, config):
        self.key = config.get("api_key") or os.environ.get("TRELLO_API_KEY")
        self.token = config.get("token") or os.environ.get("TRELLO_TOKEN")
        if not self.key or not self.token:
            raise SystemExit(
                "Missing Trello credentials. Set TRELLO_API_KEY/TRELLO_TOKEN or configure ~/.config/codex/trello.json."
            )

    def board(self, board_ref):
        return self.get(f"/boards/{board_ref}", {"fields": "id,name,url,shortLink,desc,closed"})

    def lists(self, board_ref):
        return self.get(f"/boards/{board_ref}/lists", {"fields": "id,name,closed,pos"})

    def labels(self, board_ref):
        return self.get(f"/boards/{board_ref}/labels", {"fields": "id,name,color"})

    def cards(self, board_ref, include_closed=False):
        return self.get(
            f"/boards/{board_ref}/cards",
            {
                "fields": "id,name,url,idList,closed,due,dateLastActivity,desc",
                "filter": "all" if include_closed else "open",
            },
        )

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, data=None):
        return self.request("POST", path, data=data or {})

    def put(self, path, data=None):
        return self.request("PUT", path, data=data or {})

    def request(self, method, path, params=None, data=None):
        params = dict(params or {})
        params.update({"key": self.key, "token": self.token})
        url = API_ROOT + path
        body = None
        headers = {"Accept": "application/json"}

        if method == "GET":
            url = url + "?" + urllib.parse.urlencode(params)
        else:
            data = dict(data or {})
            data.update(params)
            body = urllib.parse.urlencode(data).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        return read_json(req)

    def attach(self, card_id, file_path, name=None):
        path = Path(file_path).expanduser()
        if not path.exists():
            raise SystemExit(f"Attachment file not found: {path}")

        fields = {
            "key": self.key,
            "token": self.token,
        }
        if name:
            fields["name"] = name

        boundary = "----codex-trello-" + uuid.uuid4().hex
        parts = []
        for key, value in fields.items():
            parts.append(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                    f"{value}\r\n"
                ).encode("utf-8")
            )

        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        file_header = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
        closing = f"\r\n--{boundary}--\r\n".encode("utf-8")
        body = b"".join(parts) + file_header + path.read_bytes() + closing

        req = urllib.request.Request(
            API_ROOT + f"/cards/{card_id}/attachments",
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        return read_json(req)


def load_config(config_path=None):
    config = {}
    paths = []
    for entry in [
        config_path,
        os.environ.get("TRELLO_CONFIG"),
        str(Path.home() / ".config" / "codex" / "trello.json"),
        str(Path.home() / ".trello-codex.json"),
    ]:
        if entry:
            paths.append(Path(entry).expanduser())

    for path in paths:
        if path.exists():
            with path.open("r", encoding="utf-8") as fh:
                config.update(json.load(fh))
            break

    if os.environ.get("TRELLO_API_KEY"):
        config["api_key"] = os.environ["TRELLO_API_KEY"]
    if os.environ.get("TRELLO_TOKEN"):
        config["token"] = os.environ["TRELLO_TOKEN"]
    if os.environ.get("TRELLO_BOARD"):
        config["default_board"] = os.environ["TRELLO_BOARD"]
    return config


def resolve_board_ref(board_arg, config):
    ref = board_arg or config.get("default_board")
    boards = config.get("boards") or {}
    if ref in boards:
        ref = boards[ref]
    if not ref:
        raise SystemExit("Missing board. Pass --board or configure default_board/TRELLO_BOARD.")
    return parse_trello_ref(ref, kind="b")


def resolve_list(client, board_ref, list_ref):
    lists = client.lists(board_ref)
    lowered = list_ref.casefold()
    matches = [
        item
        for item in lists
        if item["id"] == list_ref or item["name"].casefold() == lowered
    ]
    if not matches:
        names = ", ".join(item["name"] for item in lists)
        raise SystemExit(f"List not found: {list_ref}. Available lists: {names}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple lists matched {list_ref}; use the list id.")
    return matches[0]


def resolve_card(client, board_ref, card_ref):
    ref = parse_trello_ref(card_ref, kind="c")
    try:
        return client.get(f"/cards/{ref}", {"fields": "id,name,url,idList"})
    except SystemExit:
        pass

    cards = client.cards(board_ref, include_closed=True)
    lowered = card_ref.casefold()
    matches = [
        item
        for item in cards
        if item["id"] == card_ref or item["name"].casefold() == lowered or item["url"] == card_ref
    ]
    if not matches:
        raise SystemExit(f"Card not found: {card_ref}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple cards matched {card_ref}; use the card URL or id.")
    return matches[0]


def parse_trello_ref(value, kind):
    value = str(value).strip()
    parsed = urllib.parse.urlparse(value)
    if parsed.netloc.endswith("trello.com"):
        parts = [part for part in parsed.path.split("/") if part]
        if kind in parts:
            index = parts.index(kind)
            if len(parts) > index + 1:
                return parts[index + 1]
    return value


def read_json(req):
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Trello API error {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Trello API connection error: {exc.reason}") from exc


def output(value, args):
    if args.compact:
        print(json.dumps(value, separators=(",", ":")))
    else:
        print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
