# GitHub Repo Fetcher

A Python application that retrieves all public repositories for a GitHub organisation and saves the results to a JSON file.

The application:

- Follows GitHub pagination automatically
- Retries temporary failures (429 and 5xx responses)
- Supports environment-based configuration
- Runs locally or inside Docker
- Saves output as structured JSON

By default it fetches repositories from the `psf` organisation.

---

# Prerequisites

## Docker (recommended)

- Docker Desktop installed and running

## Local Python (optional)

Only required for running the script outside Docker or running the tests.

- Python 3.12 or newer

---

# Quick Start (Docker)

Run all commands from the project root.

## 1. Build the image

```powershell
docker build -t api-fetcher .
```

Typical image size:

```text
~195 MB
```

This is well below the project target of 250 MB.

---

## 2. Create a configuration file

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

The default values work without modification.

`.env` is ignored by Git and excluded from the Docker image.

---

## 3. Run the container

PowerShell:

```powershell
docker run --rm --env-file .env -v "${PWD}/output:/data" api-fetcher
```

Linux/macOS:

```bash
docker run --rm --env-file .env -v "$(pwd)/output:/data" api-fetcher
```

Example output:

```text
Fetched 30 repos so far, rate limit remaining: 59
Fetched 44 repos so far, rate limit remaining: 58
Saved 44 repos to /data/repos.json
```

The result appears on your computer at:

```text
output/repos.json
```

The `-v` option maps the host folder to `/data` inside the container.

Without `-v`, the file is written inside the container and disappears when the container exits.

> On Windows, run Docker commands from PowerShell. Git Bash may rewrite the volume path supplied to `-v`, preventing `output/repos.json` from appearing on the host machine.

---

## Run a Different Organisation

Override variables for a single run:

```powershell
docker run --rm --env-file .env -e GITHUB_ORG=python -v "${PWD}/output:/data" api-fetcher
```

This overwrites `output/repos.json` with the newly fetched results.

---

# Configuration

All settings are supplied through environment variables.

| Variable | Default | Purpose |
|----------|----------|----------|
| GITHUB_ORG | psf | Organisation whose repositories are fetched |
| GITHUB_TOKEN | empty | Optional GitHub token for higher rate limits |
| PER_PAGE | 30 | Repositories requested per page (1-100) |
| MAX_RETRIES | 5 | Maximum attempts per request (including the first) |
| BACKOFF_BASE_SECONDS | 2 | Wait before the next attempt is base ** attempt seconds (2, 4, 8, 16 by default) |
| OUTPUT_FILE | output/repos.json locally, /data/repos.json in Docker | Output file path |
| API_URL | empty | Override URL used for testing |

## Notes

GitHub allows:

- 60 requests per hour without authentication
- Higher limits when using a token

To use a token, add:

```text
GITHUB_TOKEN=your_token
```

to `.env`.

The `.env` file is ignored by Git and excluded from the Docker image.

Never commit a token to source control.

---

# Output Format

The output file contains a JSON array.

Example:

```json
[
  {
    "name": "fundraiser-public",
    "stars": 0,
    "language": null,
    "url": "https://github.com/psf/fundraiser-public"
  }
]
```

The actual file contains one entry per repository in the selected organisation.

---

# Error Handling

## Pagination

The script follows GitHub's pagination links automatically until no additional pages remain.

## Automatically Retried

The following conditions are retried:

- HTTP 429
- HTTP 500
- HTTP 502
- HTTP 503
- HTTP 504
- Connection errors
- Timeout errors

## Not Retried

The following fail immediately:

- HTTP 401
- HTTP 403
- HTTP 404
- Other client-side errors

## Failure Behaviour

On failure the script:

- Prints an error message
- Exits with status code `1`

Example:

```powershell
docker run --rm `
-e API_URL=https://httpbin.org/status/500 `
-e MAX_RETRIES=3 `
-e BACKOFF_BASE_SECONDS=1 `
api-fetcher
```

Output:

```text
Attempt 1 failed; waiting 1s
Attempt 2 failed; waiting 1s
ERROR: Gave up after 3 attempts: https://httpbin.org/status/500
```

Verify the exit code:

```powershell
echo $LASTEXITCODE
```

Expected:

```text
1
```

---

# Running Without Docker

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python fetch_repos.py
```

Output is saved to:

```text
output/repos.json
```

Linux/macOS activation:

```bash
source .venv/bin/activate
```

---

# Running Tests

Install development dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run the test suite:

```powershell
python -m pytest -q
```

Expected:

```text
8 passed
```

The tests:

- Use fake responses
- Do not call GitHub
- Execute in under a second

Always run tests from the project root.

---

# Empty Folder Behaviour

The `output` directory may be empty before the first run.

The application automatically creates:

```text
output/repos.json
```

when a run completes successfully.

---

# Troubleshooting

| Problem | Cause / Resolution |
|----------|-------------------|
| output/repos.json does not appear | The `-v` option is missing, or `OUTPUT_FILE` was overridden incorrectly |
| Output is written inside the container only | Volume mapping is missing |
| ERROR: 429 or 403 | GitHub rate limit reached |
| ERROR: 401 | Token is invalid or expired |
| ERROR: 404 | Organisation does not exist |
| ERROR: PER_PAGE must be between 1 and 100 | Invalid configuration value |
| Docker command not found | Ensure Docker Desktop is installed and running |

---

# Project Structure

```text
.
├── fetch_repos.py
├── Dockerfile
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .dockerignore
├── tests/
│   └── test_fetch_repos.py
└── output/
    └── repos.json (created when the application runs)
```

---

# Docker Image

Built from:

```dockerfile
python:3.12-slim
```

Typical image size:

```text
~195 MB
```

---

# Deliverables

## Deliverable 1

Configurable GitHub repository fetcher featuring:

- Environment-variable configuration
- Pagination support
- Validation
- Retry handling
- JSON output

## Deliverable 2

Containerised application featuring:

- Docker image
- External configuration
- Volume-mounted output
- Correct error handling
- Non-zero exit codes on failure

## Deliverable 3

Project documentation contained in this README.

---