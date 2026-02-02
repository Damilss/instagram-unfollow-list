"""Instagram non-followers checker.

Reads followers.json and following.json from an Instagram data export and
outputs the accounts you follow who don't follow you back as a CSV file."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


DEFAULT_FOLLOWERS_FILE = "followers.json"
DEFAULT_FOLLOWING_FILE = "following.json"
OUTPUT_FILE = "not_following_back.csv"


def _extract_candidates(data: Any) -> list[dict[str, Any]]:
    """Return a list of dict items that likely contain usernames."""
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if isinstance(data, dict):
        common_keys = (
            "relationships_following",
            "relationships_followers",
            "following",
            "followers",
        )
        for key in common_keys:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

        # Fallback: first list-valued field in the dict
        for value in data.values():
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def _normalize_username(username: str) -> str:
    """Normalize usernames for reliable comparison."""
    return username.strip().lstrip("@").lower()


def load_usernames(path: Path) -> set[str]:
    """Extract usernames from an Instagram export JSON file.

    Supports common export shapes:
      - list of objects with `string_list_data`
      - dict containing a list under keys like `relationships_following`"""
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates = _extract_candidates(data)

    usernames: set[str] = set()

    for item in candidates:
        string_list_data = item.get("string_list_data")
        if isinstance(string_list_data, list) and string_list_data:
            first = string_list_data[0]
            if isinstance(first, dict):
                value = first.get("value")
                if isinstance(value, str) and value.strip():
                    usernames.add(_normalize_username(value))
                    continue

        for key in ("username", "value"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                usernames.add(_normalize_username(value))
                break

    return usernames


def write_csv(path: Path, usernames: list[str]) -> None:
    """Write usernames to a CSV file with a header."""
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["username"])
        for username in usernames:
            writer.writerow([username])


def main() -> None:
    followers_path = Path(DEFAULT_FOLLOWERS_FILE)
    following_path = Path(DEFAULT_FOLLOWING_FILE)

    if not followers_path.exists():
        raise SystemExit(
            f"Missing {DEFAULT_FOLLOWERS_FILE}. Put it next to this script."
        )
    if not following_path.exists():
        raise SystemExit(
            f"Missing {DEFAULT_FOLLOWING_FILE}. Put it next to this script."
        )

    followers = load_usernames(followers_path)
    following = load_usernames(following_path)

    not_following_back = sorted(following - followers)

    print(f"Following: {len(following)}")
    print(f"Followers: {len(followers)}")
    print(f"Not following you back: {len(not_following_back)}\n")

    for username in not_following_back:
        print(username)

    write_csv(Path(OUTPUT_FILE), not_following_back)
    print(f"\nSaved → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
