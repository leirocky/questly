"""Download the MuseScore General soundfont used by the score (any OS).

Fetches Ubuntu's musescore-general-soundfont 0.2.1 package and extracts
MuseScore_General_Full.sf3 into .cache/soundfonts/MuseScore_General.sf3 — the same file
/usr/share/sounds/sf3/MuseScore_General.sf3 points to on Ubuntu. Needs the `zstandard` package.
Usage: python3 tools/fetch_soundfont.py
"""
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

URL = ("http://archive.ubuntu.com/ubuntu/pool/universe/m/musescore-general-soundfont/"
       "musescore-general-soundfont_0.2.1-1_all.deb")
MEMBER = "usr/share/sounds/sf3/MuseScore_General_Full.sf3"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".cache" / "soundfonts" / "MuseScore_General.sf3"


def ar_members(data):
    """Yield (name, bytes) from a Debian .deb (ar archive)."""
    assert data[:8] == b"!<arch>\n", "not an ar archive"
    pos = 8
    while pos + 60 <= len(data):
        head = data[pos:pos + 60]
        name = head[:16].decode().strip().rstrip("/")
        size = int(head[48:58].decode().strip())
        yield name, data[pos + 60:pos + 60 + size]
        pos += 60 + size + (size % 2)


def main():
    if OUT.exists() and OUT.stat().st_size > 50_000_000:
        print(f"soundfont present: {OUT}")
        return
    import zstandard

    print("downloading MuseScore General soundfont package ...")
    with urllib.request.urlopen(URL) as r:
        deb = r.read()
    data = next(blob for name, blob in ar_members(deb) if name.startswith("data.tar"))
    tar_bytes = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(data)).read()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tf:
        member = next(m for m in tf.getmembers() if m.name.lstrip("./") == MEMBER)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(tf.extractfile(member).read())
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    sys.exit(main())
