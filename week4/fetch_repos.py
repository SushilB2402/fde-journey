import json
import os
import sys
import time

import requests

GITHUB_ORG = os.environ.get("GITHUB_ORG", "psf")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
PER_PAGE = int(os.environ.get("PER_PAGE") or "30")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES") or "5")
BACKOFF_BASE_SECONDS = int(os.environ.get("BACKOFF_BASE_SECONDS") or "2")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "output/repos.json")
API_URL = os.environ.get("API_URL", "")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "fde-week4",
}

if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

RETRY_STATUS = {429, 500, 502, 503, 504}


def get_with_retry(
    url,
    params=None,
    headers=None,
    max_attempts=5,
    backoff_base=2,
):
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10,
            )
        except (requests.ConnectionError, requests.Timeout):
            resp = None

        if resp is not None and resp.status_code not in RETRY_STATUS:
            resp.raise_for_status()
            return resp

        if attempt == max_attempts:
            raise RuntimeError(
                f"Gave up after {max_attempts} attempts: {url}"
            )

        wait = backoff_base ** attempt

        if (
            resp is not None
            and resp.headers.get("Retry-After", "").isdigit()
        ):
            wait = int(resp.headers["Retry-After"])

        print(
            f"Attempt {attempt} failed; waiting {wait}s",
            flush=True,
        )

        time.sleep(wait)


def fetch_all(url, params, headers):
    items = []

    while url:
        resp = get_with_retry(
            url,
            params=params,
            headers=headers,
            max_attempts=MAX_RETRIES,
            backoff_base=BACKOFF_BASE_SECONDS,
        )

        items.extend(resp.json())

        remaining = resp.headers.get(
            "x-ratelimit-remaining",
            "unknown",
        )

        print(
            f"Fetched {len(items)} repos so far, "
            f"rate limit remaining: {remaining}",
            flush=True,
        )

        url = resp.links.get("next", {}).get("url")
        params = None

    return items


def main():
    if not GITHUB_ORG and not API_URL:
        raise ValueError(
            "GITHUB_ORG must not be empty"
        )

    if not 1 <= PER_PAGE <= 100:
        raise ValueError(
            "PER_PAGE must be between 1 and 100"
        )

    url = (
        API_URL
        if API_URL
        else f"https://api.github.com/orgs/{GITHUB_ORG}/repos"
    )

    repos = fetch_all(
        url,
        {"per_page": PER_PAGE},
        headers,
    )

    slim = [
        {
            "name": r["name"],
            "stars": r["stargazers_count"],
            "language": r["language"],
            "url": r["html_url"],
        }
        for r in repos
    ]

    output_dir = os.path.dirname(OUTPUT_FILE)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(slim, f, indent=2)

    print(
        f"Saved {len(slim)} repos to {OUTPUT_FILE}",
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)
        