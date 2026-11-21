import json

import pytest
import requests

import fetch_repos as fr


class FakeResponse:
    def __init__(self, status=200, json_data=None, headers=None, links=None):
        self.status_code = status
        self._json = json_data or []
        self.headers = headers or {}
        self.links = links or {}

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code), response=self)


def patch_get(monkeypatch, responses):
    """Make requests.get return the given responses in order; record sleeps."""
    it = iter(responses)
    sleeps = []
    monkeypatch.setattr(fr.requests, "get", lambda *a, **k: next(it))
    monkeypatch.setattr(fr.time, "sleep", sleeps.append)
    return sleeps


# ---------- the five required tests ----------

def test_retries_500_then_succeeds(monkeypatch):
    sleeps = patch_get(
        monkeypatch,
        [FakeResponse(500), FakeResponse(500), FakeResponse(200, [{"name": "a"}])],
    )
    resp = fr.get_with_retry("http://example.test")
    assert resp.status_code == 200
    assert sleeps == [2, 4]  # exponential backoff with the default base of 2


def test_honours_retry_after_on_429(monkeypatch):
    sleeps = patch_get(
        monkeypatch,
        [FakeResponse(429, headers={"Retry-After": "7"}), FakeResponse(200, [{"name": "a"}])],
    )
    fr.get_with_retry("http://example.test")
    assert sleeps == [7]


def test_gives_up_after_max_attempts(monkeypatch):
    patch_get(monkeypatch, [FakeResponse(500), FakeResponse(500), FakeResponse(500)])
    with pytest.raises(RuntimeError):
        fr.get_with_retry("http://example.test", max_attempts=3)


def test_404_is_not_retried(monkeypatch):
    sleeps = patch_get(monkeypatch, [FakeResponse(404)])
    with pytest.raises(requests.HTTPError):
        fr.get_with_retry("http://example.test")
    assert sleeps == []  # no waiting means no retry


def test_fetch_all_follows_next_links(monkeypatch):
    responses = iter(
        [
            FakeResponse(200, [{"name": "a"}], links={"next": {"url": "page2"}}),
            FakeResponse(200, [{"name": "b"}]),
        ]
    )
    calls = []

    def fake(url, params=None, headers=None, **k):
        calls.append((url, params))
        return next(responses)

    monkeypatch.setattr(fr, "get_with_retry", fake)
    repos = fr.fetch_all("page1", {"per_page": 5}, {})
    assert len(repos) == 2
    # first request carries params; the next URL already contains them
    assert calls == [("page1", {"per_page": 5}), ("page2", None)]


# ---------- edge cases ----------

def test_401_is_not_retried(monkeypatch):
    sleeps = patch_get(monkeypatch, [FakeResponse(401)])
    with pytest.raises(requests.HTTPError):
        fr.get_with_retry("http://example.test")
    assert sleeps == []


def test_invalid_per_page_is_rejected(monkeypatch):
    monkeypatch.setattr(fr, "PER_PAGE", 0)
    with pytest.raises(ValueError):
        fr.main()


def test_empty_org_saves_empty_list(monkeypatch, tmp_path):
    out = tmp_path / "sub" / "repos.json"
    monkeypatch.setattr(fr, "OUTPUT_FILE", str(out))
    monkeypatch.setattr(fr, "fetch_all", lambda *a, **k: [])
    fr.main()
    assert json.loads(out.read_text(encoding="utf-8")) == []


# ---------- GitHub rate-limit (403) handling ----------

def test_403_rate_limit_reports_reset_time_and_is_not_retried(monkeypatch):
    sleeps = patch_get(
        monkeypatch,
        [
            FakeResponse(
                403,
                headers={
                    "x-ratelimit-remaining": "0",
                    "x-ratelimit-reset": "1700000000",
                },
            )
        ],
    )
    with pytest.raises(RuntimeError) as exc:
        fr.get_with_retry("http://example.test")
    assert "rate limit" in str(exc.value).lower()
    assert "2023-11-14 22:13:20 UTC" in str(exc.value)
    assert sleeps == []  # not retried


def test_403_rate_limit_without_reset_header_still_clear(monkeypatch):
    patch_get(
        monkeypatch,
        [FakeResponse(403, headers={"x-ratelimit-remaining": "0"})],
    )
    with pytest.raises(RuntimeError) as exc:
        fr.get_with_retry("http://example.test")
    assert "rate limit exceeded" in str(exc.value).lower()


def test_403_without_rate_limit_is_a_normal_http_error(monkeypatch):
    patch_get(
        monkeypatch,
        [FakeResponse(403, headers={"x-ratelimit-remaining": "42"})],
    )
    with pytest.raises(requests.HTTPError):
        fr.get_with_retry("http://example.test")
