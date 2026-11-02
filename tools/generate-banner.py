#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=1.20", "pyyaml>=6"]
# ///
"""Generate a 16:9 hero banner for a uright blog post with Gemini image models on Vertex AI.

Usage:
  generate-banner.py POST.md [--scene "what to draw"] [-n 3] [--out-dir DIR]
  generate-banner.py --title "Title" --scene "..." --out-dir DIR

Credentials: --key PATH, or GOOGLE_APPLICATION_CREDENTIALS (a service-account JSON).
The project id is read from the key file unless --project is given.
"""
import argparse
import json
import os
import pathlib
import re
import sys
import time

import yaml
from google import genai
from google.genai import errors, types

STYLE = (
    "Wide 16:9 hero banner for a developer tech blog. Modern, polished digital illustration: "
    "deep navy-to-purple background with subtle glowing network lines and particles, "
    "crisp flat-3D icons and UI panels, cyan and violet accent lighting, high contrast. "
    "A bold title in clean white sans-serif capital letters, perfectly spelled, set in a rounded "
    "gradient banner bar along the bottom third. No watermarks, no extra text besides what is specified."
)


def front_matter(path: pathlib.Path) -> dict:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post", nargs="?", help="post markdown file (title/slug read from it)")
    ap.add_argument("--title", help="text to render on the banner (default: post title)")
    ap.add_argument("--scene", default="", help="what the illustration should show")
    ap.add_argument("-n", type=int, default=1, help="number of variants")
    ap.add_argument("--out-dir", help="default: assets/img/<post-slug>/ next to the post")
    ap.add_argument("--name", default="hero", help="output file stem (default: hero)")
    ap.add_argument("--model", default="gemini-2.5-flash-image")
    ap.add_argument("--location", default="us-central1")  # "global" often 429s for image models
    ap.add_argument("--key", default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    ap.add_argument("--project")
    a = ap.parse_args()

    if not a.key or not pathlib.Path(a.key).expanduser().is_file():
        sys.exit("error: pass --key or set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON")
    key = pathlib.Path(a.key).expanduser()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(key)
    project = a.project or json.loads(key.read_text())["project_id"]

    title, out_dir = a.title, a.out_dir
    if a.post:
        post = pathlib.Path(a.post)
        fm = front_matter(post)
        title = title or fm.get("title")
        if not out_dir:
            out_dir = post.resolve().parent.parent / "assets" / "img" / post.stem
    if not title or not out_dir:
        sys.exit("error: need a post file, or --title and --out-dir")
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    prompt = f'{STYLE}\nBanner title text: "{title}".\nIllustration: {a.scene or "a visual metaphor for the title"}'
    client = genai.Client(vertexai=True, project=project, location=a.location)
    cfg = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
    )
    for i in range(1, a.n + 1):
        for attempt in range(5):
            try:
                resp = client.models.generate_content(model=a.model, contents=prompt, config=cfg)
                break
            except errors.ClientError as e:
                if e.code != 429 or attempt == 4:
                    raise
                wait = 10 * 2**attempt
                print(f"variant {i}: 429 quota, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
        parts = [p for c in resp.candidates or [] for p in (c.content.parts if c.content else [])]
        img = next((p.inline_data for p in parts if p.inline_data), None)
        if not img:
            print(f"variant {i}: no image returned ({resp.candidates[0].finish_reason if resp.candidates else 'no candidates'})", file=sys.stderr)
            continue
        ext = "png" if "png" in (img.mime_type or "") else "jpeg"
        path = out / (f"{a.name}.{ext}" if a.n == 1 else f"{a.name}-{i}.{ext}")
        path.write_bytes(img.data)
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
