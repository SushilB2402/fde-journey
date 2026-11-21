#!/usr/bin/env bash
# End-to-end check: build, run in Docker, verify the saved file, verify failure exit code.
# Run from the week4 folder:  bash e2e.sh
set -euo pipefail

# Git Bash on Windows rewrites /data in -v paths; switch that off and use a Windows-style host path.
export MSYS_NO_PATHCONV=1
if pwd -W >/dev/null 2>&1; then HOST_DIR="$(pwd -W)"; else HOST_DIR="$(pwd)"; fi

PYTHON=python
command -v python >/dev/null 2>&1 || PYTHON=python3

rm -rf output

docker build --no-cache -t api-fetcher .

docker run --rm \
  -e GITHUB_ORG=psf \
  -e PER_PAGE=10 \
  -v "${HOST_DIR}/output:/data" \
  api-fetcher

"$PYTHON" -c "import json; d=json.load(open('output/repos.json')); assert len(d) > 10, len(d); print('OK', len(d), 'repos')"

if docker run --rm \
    -e API_URL=https://httpbin.org/status/500 \
    -e MAX_RETRIES=2 \
    -e BACKOFF_BASE_SECONDS=1 \
    api-fetcher
then
    echo 'FAIL: expected a non-zero exit'
    exit 1
else
    echo 'OK: failure run exited non-zero'
fi
