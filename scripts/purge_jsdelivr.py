import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen


PURGE_ORIGIN = "https://purge.jsdelivr.net"
CDN_ORIGIN = "https://cdn.jsdelivr.net"
DAT_FILES = ("dat/geoip.dat", "dat/geosite.dat")


def download(url):
    with urlopen(url, timeout=15) as response:
        return response.read()


def purge(path):
    result = json.loads(download(PURGE_ORIGIN + path))
    if result.get("id") and result.get("status") not in {"finished", "failed"}:
        status_url = f"{PURGE_ORIGIN}/status/{quote(result['id'], safe='')}"
        for _ in range(5):
            time.sleep(2)
            result = json.loads(download(status_url))
            if result.get("status") in {"finished", "failed"}:
                break

    details = result.get("paths", {}).get(path, {})
    providers = details.get("providers", {})
    if details.get("throttled"):
        raise RuntimeError("jsDelivr rate limit reached")
    if result.get("status") != "finished" or not providers or any(
        status is not True for status in providers.values()
    ):
        raise RuntimeError(f"jsDelivr did not confirm purge: {result}")


def refresh(path, expected):
    purge(path)
    if download(CDN_ORIGIN + path) == expected:
        return

    # The jsDelivr origin can briefly retain an older revision of a branch.
    print(f"{path}: CDN still serves an older file, retrying in 90 seconds", flush=True)
    time.sleep(90)
    purge(path)
    if download(CDN_ORIGIN + path) != expected:
        raise RuntimeError("CDN file still differs from GitHub main after purge")


def main():
    repository = os.environ["GITHUB_REPOSITORY"]
    root = Path(__file__).resolve().parents[1]
    failed = False
    for name in DAT_FILES:
        path = f"/gh/{repository}@main/{name}"
        try:
            refresh(path, (root / name).read_bytes())
        except (OSError, RuntimeError, ValueError) as error:
            print(f"{name}: {error}", file=sys.stderr)
            failed = True
        else:
            print(f"{name}: cache purged, CDN file matches GitHub main")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
