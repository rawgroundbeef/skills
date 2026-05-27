---
name: trello
description: Work with Trello boards through the Trello REST API. Use when the user asks Codex to inspect or update Trello boards, lists, cards, labels, comments, attachments, checklists, kanban workflows, or asks to configure a board URL/id and API credentials for repeatable board operations.
---

# Trello

Use this skill to work with Trello as a lightweight workflow database. Prefer the bundled CLI for repeatable operations and raw `curl` only when the CLI is missing a needed endpoint.

## Configuration

Read `references/config.md` when setting up or debugging credentials.

The bundled CLI reads credentials from either:

- Environment: `TRELLO_API_KEY`, `TRELLO_TOKEN`, optional `TRELLO_BOARD`
- Config file: `~/.config/codex/trello.json`, `~/.trello-codex.json`, or `TRELLO_CONFIG`

Never commit API keys or tokens to a skill, repo, Trello card, or final response. Do not print full authenticated URLs.

## Workflow

1. Resolve the board from the user's board URL/id, a configured alias, or `default_board`.
2. Inspect before mutating:
   - `python scripts/trello.py board`
   - `python scripts/trello.py lists`
   - `python scripts/trello.py cards --list "Inbox"`
3. Make the smallest board change needed:
   - Create cards for new work.
   - Move cards between lists when status changes.
   - Add comments for durable context.
   - Attach files that should not be lost.
4. Verify after every mutation by reading the changed card/list.
5. In the final response, summarize the board-level effect without exposing credentials or private data.

When an operation could overwrite or remove meaningful user data, ask first. Archiving a card is safer than deleting.

## CLI Quick Reference

Run commands from this skill directory, or use an absolute path to `scripts/trello.py`.

```bash
python scripts/trello.py board
python scripts/trello.py lists
python scripts/trello.py cards --list "Inbox"
python scripts/trello.py card "https://trello.com/c/abc123"
python scripts/trello.py create-card --list "Inbox" --name "New task" --desc "Context and acceptance criteria."
python scripts/trello.py move-card --card "New task" --list "Done"
python scripts/trello.py comment --card "New task" --text "Completed on 2026-05-27."
python scripts/trello.py attach --card "New task" --file "/path/to/file.pdf"
python scripts/trello.py add-checklist --card "New task" --name "Checklist" --item "First step" --item "Second step"
```

Pass `--board <url-or-id-or-alias>` when the user specifies a non-default board.

## Board Engagement Pattern

For workflow boards, first learn the board's taxonomy:

```bash
python scripts/trello.py lists
python scripts/trello.py labels
python scripts/trello.py cards --list "Inbox"
```

Infer list meaning from names, but confirm before creating new lists or changing the workflow. Preserve the user's existing card description format when creating or updating cards.

## Direct API Fallback

If the CLI does not cover the needed endpoint, use Trello REST API endpoints directly. Prefer `key` and `token` from environment or config, keep tokens out of logs, and verify with a read request after mutation.
