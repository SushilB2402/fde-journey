# GitHub Repo Fetcher

A small Python script that lists every public repository of a GitHub organisation and saves them to a JSON file. It follows pagination, retries when the API answers 429 or 5xx, and runs in a Docker container configured by environment variables.

By default it fetches the `psf` organisation (44 repositories).

## Prerequisites

- Docker Desktop (running)
- Python 3.12 or newer, only if you want to run it without Docker or run the tests

## Quick start (Docker)

All commands run from this folder.

**1. Build the image**

```powershell
docker build -t api-fetcher .
```

**2. Create your settings file**

```powershell
Copy-Item .env.example .env
```

(macOS, Linux: `cp .env.example .env`.) The defaults work as they are. `.env` is ignored by Git and excluded from the image, so it is safe to put a token in it.

**3. Run it**

PowerShell:

```powershell
docker run --rm --env-file .env -v "${PWD}/output:/data" api-fetcher
```

macOS, Linux:

```bash
docker run --rm --env-file .env -v "$(pwd)/output:/data" api-fetcher
```

On Windows use PowerShell for this command. Git Bash rewrites the `-v` path and the file will not appear.

Expected output:

```
Fetched 30 repos so far, rate limit remaining: 59
Fetched 44 repos so far, rate limit remaining: 58
Saved 44 repos to /data/repos.json
```

The result is on your computer at `output/repos.json`. The `-v` option maps that folder to `/data` inside the container. Without it the file is written inside the container and disappears when it exits.

To fetch another organisation, override a variable for one run:

```powershell
docker run --rm --env-file .env -e GITHUB_ORG=python -v "${PWD}/output:/data" api-fetcher
```

## Configuration

Set these as environment variables (in `.env` or with `-e NAME=value`).

| Variable | Default | Meaning |
|---|---|---|
| `GITHUB_ORG` | `psf` | Organisation to fetch |
| `GITHUB_TOKEN` | empty | Optional. Raises the limit from 60 to 5000 requests per hour |
| `PER_PAGE` | `30` | Repos per request, 1 to 100 |
| `MAX_RETRIES` | `5` | Attempts per request before giving up |
| `BACKOFF_BASE_SECONDS` | `2` | Base of the wait between attempts (2, 4, 8, 16 seconds) |
| `OUTPUT_FILE` | `output/repos.json` locally, `/data/repos.json` in Docker | Where to save the result. Leave it alone in Docker, because the Dockerfile sets it to match the volume |
| `API_URL` | empty | Fetch this URL instead of the GitHub organisation URL (used for testing) |

Never commit a token. Put it only in `.env` or pass it with `-e GITHUB_TOKEN=...` for one run.

## Output

`output/repos.json` is a list with one entry per repository:

```json
{
  "name": "fundraiser-public",
  "stars": 0,
  "language": null,
  "url": "https://github.com/psf/fundraiser-public"
}
```

## Error handling

- **Pagination:** follows the `Link: rel="next"` header until there are no more pages.
- **Retried:** HTTP 429, 500, 502, 503 and 504, plus connection errors and timeouts. Waits grow with each attempt, and a `Retry-After` header is honoured.
- **Not retried:** other 4xx errors such as 401 and 404 fail at once.
- **Failure:** prints `ERROR: ...` and exits with code 1. Success exits with 0.

Try it:

```powershell
docker run --rm -e API_URL=https://httpbin.org/status/500 -e MAX_RETRIES=3 -e BACKOFF_BASE_SECONDS=1 api-fetcher
echo $LASTEXITCODE
```

This prints the retry messages, then the error, and `1`.

## Run without Docker

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python fetch_repos.py
```

(macOS, Linux: `source .venv/bin/activate`.) The file is saved to `output/repos.json`.

## Tests

```powershell
pip install -r requirements-dev.txt
python -m pytest -q
```

Expected: `8 passed`. The tests use fake responses and make no real API calls. Run them from this folder, not from inside `tests/`.

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `output/repos.json` does not appear | The `-v` option is missing, or `OUTPUT_FILE` was changed in `.env`. Remove that line and use the full run command |
| `ERROR: 403` or `429` straight away | Rate limit reached (60 per hour without a token). Wait, or set `GITHUB_TOKEN` |
| `ERROR: 401` | The token is wrong or expired. Create a new one |
| `ERROR: 404` | `GITHUB_ORG` does not exist |
| `docker: command not found` in WSL | Run Docker commands from PowerShell |

## Files

| File | Purpose |
|---|---|
| `fetch_repos.py` | The script |
| `Dockerfile` | Builds the image (Python 3.12 slim) |
| `.dockerignore` | Keeps `.env`, `.git` and output out of the image |
| `.env.example` | Template for `.env` |
| `requirements.txt` | Runtime dependency (`requests`) |
| `requirements-dev.txt` | Adds `pytest` |
| `tests/` | Unit tests |
