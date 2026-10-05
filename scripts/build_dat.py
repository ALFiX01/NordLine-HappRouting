#!/usr/bin/env python3
"""Build Xray/Happ GeoIPList and GeoSiteList from sectioned TXT (Python 3.10+).

Wire schema: https://github.com/XTLS/Xray-core/blob/main/common/geodata/geodat.proto
Only Python's standard library is required.
"""
import ipaddress
from pathlib import Path
import re
import tempfile


def varint(value):
    result = bytearray()
    while value > 127:
        result.append((value & 127) | 128)
        value >>= 7
    result.append(value)
    return bytes(result)


def field(number, value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    if isinstance(value, bytes):
        return varint(number * 8 + 2) + varint(len(value)) + value
    return varint(number * 8) + varint(value) if value else b""


def convert(path, kind):
    groups = {}
    current = None
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            if line.startswith("[") and line.endswith("]"):
                current = line[1:-1].upper()
                if not re.fullmatch(r"[A-Z0-9_-]+", current) or current in groups:
                    raise ValueError("invalid or duplicate category")
                groups[current] = []
                continue
            if current is None:
                raise ValueError("rule outside a category")
            if kind == "geoip":
                network = ipaddress.ip_network(line, strict=False)
                rule = field(1, network.network_address.packed) + field(2, network.prefixlen)
            else:
                prefix, separator, value = line.partition(":")
                types = {"plain": 0, "regex": 1, "domain": 2, "full": 3}
                if not separator or prefix not in types or not value.strip():
                    raise ValueError("expected plain:, regex:, domain: or full: rule")
                if "@" in value or any(c.isspace() for c in value):
                    raise ValueError("attributes and whitespace in rules are unsupported")
                rule = field(1, types[prefix]) + field(2, value)
            groups[current].append(field(2, rule))
        except ValueError as error:
            raise ValueError(f"{path}:{number}: {error}") from error
    if not groups or any(not rules for rules in groups.values()):
        raise ValueError(f"{path}: missing or empty category")
    return b"".join(field(1, field(1, code) + b"".join(rules)) for code, rules in groups.items())


def build(root):
    source = root / "txt"
    paths = sorted(source.glob("*.txt"))
    if not paths:
        raise ValueError(f"{source}: no TXT files")
    outputs = {}
    for path in paths:
        # Keep file names explicit: GeoIP and GeoSite use different schemas.
        if path.stem not in {"geoip", "geosite"}:
            raise ValueError(f"{path}: expected geoip.txt or geosite.txt")
        outputs[path.with_suffix(".dat").name] = convert(path, path.stem)
    destination = root / "dat"
    destination.mkdir(exist_ok=True)
    # Validate and stage every file before replacing any existing DAT.
    with tempfile.TemporaryDirectory(dir=destination) as staging:
        for name, data in outputs.items():
            (Path(staging) / name).write_bytes(data)
        for name in outputs:
            (Path(staging) / name).replace(destination / name)
            print(f"Built dat/{name}: {len(outputs[name])} bytes")


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1])
