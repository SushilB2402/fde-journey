import json
import os
import sys
import time

import requests

ORG = "psf"
TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "fde-week4",
}

if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

RETRY_STATUS = {429, 500, 502, 503, 504}


def get_with_retry(url, params=None, headers=None, max_attempts=5, backoff_base=2):
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

        print(f"Attempt {attempt} failed; waiting {wait}s")
        time.sleep(wait)


def fetch_all(url, params, headers):
    items = []

    while url:
        resp = get_with_retry(
            url,
            params=params,
            headers=headers,
        )

        items.extend(resp.json())

        remaining = resp.headers.get(
            "x-ratelimit-remaining",
            "unknown"
        )

        print(
            f"Fetched {len(items)} repos so far, "
            f"rate limit remaining: {remaining}"
        )

        url = resp.links.get("next", {}).get("url")
        params = None

    return items


def main():
    repos = fetch_all(
        f"https://api.github.com/orgs/{ORG}/repos",
        {"per_page": 10},
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

    os.makedirs("output", exist_ok=True)

    with open(
        "output/repos.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(slim, f, indent=2)

    print(
        f"Saved {len(slim)} repos "
        "to output/repos.json"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
        