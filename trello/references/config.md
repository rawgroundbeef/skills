# Trello Configuration

Use environment variables for short-lived sessions:

```bash
export TRELLO_API_KEY="..."
export TRELLO_TOKEN="..."
export TRELLO_BOARD="https://trello.com/b/BOARD_SHORT_LINK/board-name"
```

For persistent local setup, create `~/.config/codex/trello.json`:

```json
{
  "api_key": "your-api-key",
  "token": "your-token",
  "default_board": "main",
  "boards": {
    "main": "https://trello.com/b/BOARD_SHORT_LINK/board-name"
  }
}
```

Rules:

- Keep this config outside repos and skills.
- Prefer board aliases for repeat boards.
- A board value may be a full board URL, a board short link, or a board id.
- A card value may be a full card URL, a card short link, a card id, or an exact card name when `--board` is available.
- If multiple cards share the same name, use the Trello card URL or id.
