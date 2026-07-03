#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

PYPI_JSON_URL_TEMPLATE = "https://pypi.org/pypi/{package_name}/json"
PYPI_UPLOAD_URL = "https://upload.pypi.org/legacy/"

EXIT_VALIDATION_ERROR = 1
EXIT_PYPI_QUERY_ERROR = 2

TOKEN_USERNAME = "__token__"
TOKEN_PREFIX = "pypi-"


class PyPIQueryError(RuntimeError):
    """Raised when PyPI cannot be reached or returns an unexpected response."""


def require_non_empty(name: str, value: str | None) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{name} is not set or empty.")
    return value.strip()


def validate_credential_shape(username: str, password: str) -> None:
    if username == TOKEN_USERNAME and not password.startswith(TOKEN_PREFIX):
        raise ValueError(
            f"When TWINE_USERNAME is '{TOKEN_USERNAME}', TWINE_PASSWORD must be a PyPI API token "
            f"starting with '{TOKEN_PREFIX}'."
        )


def probe_pypi_json_api(package_name: str) -> None:
    url = PYPI_JSON_URL_TEMPLATE.format(package_name=package_name)

    print(f"Checking PyPI JSON API reachability: {url}")

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(
                f"OK: PyPI JSON API is reachable (package '{package_name}' is not published yet)."
            )
            return
        raise PyPIQueryError(f"Failed to query PyPI JSON API: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise PyPIQueryError(f"Failed to query PyPI JSON API: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise PyPIQueryError("Failed to query PyPI JSON API: invalid JSON response") from exc

    print(f"OK: PyPI JSON API is reachable for package '{package_name}'.")


def probe_upload_endpoint(username: str, password: str) -> None:
    print(f"Checking PyPI upload endpoint reachability: {PYPI_UPLOAD_URL}")

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode("ascii")
    request = urllib.request.Request(
        PYPI_UPLOAD_URL,
        method="GET",
        headers={"Authorization": f"Basic {credentials}"},
    )

    try:
        with urllib.request.urlopen(request, timeout=20):
            print("OK: PyPI upload endpoint is reachable.")
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403}:
            raise ValueError(
                f"PyPI upload credentials were rejected (HTTP {exc.code})."
            ) from exc
        if exc.code == 405:
            print("OK: PyPI upload endpoint is reachable.")
            return
        if exc.code < 500:
            raise PyPIQueryError(
                f"PyPI upload endpoint returned unexpected client error: HTTP {exc.code}"
            ) from exc
        raise PyPIQueryError(f"Failed to reach PyPI upload endpoint: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise PyPIQueryError(f"Failed to reach PyPI upload endpoint: {exc.reason}") from exc


def check_pypi_credentials(package_name: str, username: str, password: str) -> None:
    validate_credential_shape(username, password)
    probe_pypi_json_api(package_name=package_name)
    probe_upload_endpoint(username=username, password=password)
    print(
        "NOTE: Full upload authorization is confirmed during twine upload. "
        "Credential configuration and endpoint reachability checks passed."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify PyPI reachability and upload credential configuration."
    )
    parser.add_argument("--package-name", required=True)
    parser.add_argument(
        "--username",
        default=os.environ.get("TWINE_USERNAME"),
        help="PyPI username (default: TWINE_USERNAME environment variable).",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("TWINE_PASSWORD"),
        help="PyPI password or API token (default: TWINE_PASSWORD environment variable).",
    )

    args = parser.parse_args()

    try:
        username = require_non_empty("TWINE_USERNAME", args.username)
        password = require_non_empty("TWINE_PASSWORD", args.password)
        check_pypi_credentials(
            package_name=args.package_name,
            username=username,
            password=password,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_VALIDATION_ERROR
    except PyPIQueryError as exc:
        print(f"PYPI QUERY ERROR: {exc}", file=sys.stderr)
        return EXIT_PYPI_QUERY_ERROR

    print(f"OK: PyPI connectivity and credential configuration verified for user '{username}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
