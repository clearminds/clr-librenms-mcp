"""REST client for LibreNMS API v0."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class LibreNMSClient:
    """LibreNMS REST API client with token-based auth.

    Uses X-Auth-Token header for all requests.
    Handles pagination via count/offset when needed.
    """

    def __init__(self, url: str, token: str) -> None:
        self.base_url = url.rstrip("/")
        self.token = token

        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=30.0,
            headers={"X-Auth-Token": self.token},
        )

        # Verify connection
        resp = self._http.get("/api/v0/system")
        resp.raise_for_status()
        info = resp.json()
        logger.info(
            "Connected to LibreNMS %s",
            info.get("system", [{}])[0].get("local_ver", "unknown"),
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def get(
        self, path: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """GET request to LibreNMS API.

        Args:
            path: API path (e.g. "/api/v0/devices").
            params: Optional query parameters.

        Returns the parsed JSON response body.
        """
        resp = self._http.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    def put(self, path: str, data: Any = None) -> tuple[int, Any]:
        """PUT request. Returns (status_code, response_body)."""
        resp = self._http.put(path, json=data or {})
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        return resp.status_code, body
