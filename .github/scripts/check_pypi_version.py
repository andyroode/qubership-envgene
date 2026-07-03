#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

from packaging.version import InvalidVersion, Version


STRICT_SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)


def validate_strict_semver(version: str) -> Version:
    if not STRICT_SEMVER_RE.fullmatch(version):
        raise ValueError(
            "Version must be strict semver: X.Y.Z. "
            "Examples: 0.1.0, 1.0.0, 2.3.4. "
            "Not allowed: v1.0.0, 1.0, 1.0.0-rc1, 1.0.0+build, 01.0.0"
        )

    return Version(version)


def fetch_pypi_releases(package_name: str) -> dict:
    url = f"https://pypi.org/pypi/{package_name}/json"

    print(f"Checking PyPI package: {package_name}")
    print(f"PyPI URL: {url}")

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(f"OK: package '{package_name}' does not exist on PyPI yet. First release is allowed.")
            return {}
        raise RuntimeError(f"Failed to query PyPI: HTTP {exc.code}") from exc

    releases = payload.get("releases", {})

    if not isinstance(releases, dict):
        raise RuntimeError("Unexpected PyPI response: 'releases' field is missing or invalid.")

    return releases


def get_latest_pypi_version(releases: dict) -> Version | None:
    parsed_versions: list[Version] = []

    for raw_version in releases.keys():
        try:
            parsed_versions.append(Version(raw_version))
        except InvalidVersion:
            print(f"WARNING: skipping invalid existing PyPI version: {raw_version}")

    if not parsed_versions:
        return None

    return max(parsed_versions)


def check_candidate_version(package_name: str, candidate_raw: str) -> None:
    candidate = validate_strict_semver(candidate_raw)

    print(f"Candidate version: {candidate}")

    releases = fetch_pypi_releases(package_name)
    latest = get_latest_pypi_version(releases)

    if latest is None:
        print(f"OK: no existing releases found for '{package_name}'. Version '{candidate}' is allowed.")
        return

    print(f"Latest PyPI version: {latest}")

    if candidate <= latest:
        raise ValueError(
            f"Candidate version '{candidate}' must be greater than latest PyPI version '{latest}'."
        )

    print(f"OK: candidate version '{candidate}' is greater than latest PyPI version '{latest}'.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate release version and ensure it is greater than the latest PyPI release."
    )
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--version", required=True)

    args = parser.parse_args()

    try:
        check_candidate_version(
            package_name=args.package_name,
            candidate_raw=args.version,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())