#!/usr/bin/env python3
"""Pull one conversation out of a Claude data export, on your own machine.

Usage
-----
    # list conversations whose title or text contains a phrase
    python tools/extract_conversation.py EXPORT --search "virtual photons" --list

    # write the first match to a Markdown file
    python tools/extract_conversation.py EXPORT --search "virtual photons" -o docs/transcript/full.md

EXPORT can be the downloaded .zip, the unzipped folder, or conversations.json.
Use --pick N to choose a different match from the --list output.

Notes
-----
* Needs only Python 3 (no extra packages). Nothing is sent anywhere.
* Written without seeing a real export file, so it reads the format defensively:
  it looks for a list of conversations, each with a list of messages, and takes
  each message's text from a "text" field or from "text"-type content blocks.
  If it can't find messages, run with --debug and it prints the keys it saw.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


def load_conversations(path: Path):
    if path.is_dir():
        candidates = sorted(path.rglob("conversations.json"))
        if not candidates:
            sys.exit(f"No conversations.json found under {path}")
        data = json.loads(candidates[0].read_text(encoding="utf-8"))
    elif path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith("conversations.json")]
            if not names:
                sys.exit(f"No conversations.json inside {path}")
            data = json.loads(z.read(names[0]).decode("utf-8"))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("conversations", "chats", "data"):
            if isinstance(data.get(key), list):
                return data[key]
        return [data]
    return data


def messages_of(conv: dict) -> list[dict]:
    for key in ("chat_messages", "messages", "turns"):
        if isinstance(conv.get(key), list):
            return conv[key]
    return []


def text_of(msg: dict) -> str:
    parts = []
    content = msg.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text" and block.get("text"):
                parts.append(block["text"])
    elif isinstance(content, str) and content.strip():
        parts.append(content)
    if not parts and isinstance(msg.get("text"), str):
        parts.append(msg["text"])
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def speaker_of(msg: dict) -> str:
    who = str(msg.get("sender") or msg.get("role") or "unknown").lower()
    return {"human": "You", "user": "You", "assistant": "Claude"}.get(who, who)


def title_of(conv: dict) -> str:
    return str(conv.get("name") or conv.get("title") or "(untitled)")


def matches(conv: dict, phrase: str | None) -> bool:
    if not phrase:
        return True
    p = phrase.lower()
    if p in title_of(conv).lower():
        return True
    return any(p in text_of(m).lower() for m in messages_of(conv))


def to_markdown(conv: dict) -> str:
    lines = [f"# {title_of(conv)}", ""]
    for k in ("created_at", "updated_at", "uuid", "id"):
        if conv.get(k):
            lines.append(f"- {k}: {conv[k]}")
    lines.append("")
    for msg in messages_of(conv):
        stamp = msg.get("created_at") or msg.get("timestamp") or ""
        lines += [f"## {speaker_of(msg)}" + (f" ({stamp})" if stamp else ""), "", text_of(msg), ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path, help="export .zip, unzipped folder, or conversations.json")
    ap.add_argument("--search", help="phrase to find in the title or messages (case-insensitive)")
    ap.add_argument("--list", action="store_true", help="list matching conversations and stop")
    ap.add_argument("--pick", type=int, default=1, help="which match to write (1 = first)")
    ap.add_argument("-o", "--output", type=Path, help="Markdown file to write (default: print)")
    ap.add_argument("--debug", action="store_true", help="print the keys found in the export")
    args = ap.parse_args()

    convs = [c for c in load_conversations(args.export) if isinstance(c, dict)]
    if args.debug and convs:
        print("conversation keys:", sorted(convs[0].keys()), file=sys.stderr)
        msgs = messages_of(convs[0])
        if msgs:
            print("message keys:", sorted(msgs[0].keys()), file=sys.stderr)

    found = [c for c in convs if matches(c, args.search)]
    if args.list or not found:
        print(f"{len(found)} matching conversation(s) of {len(convs)}:")
        for i, c in enumerate(found, 1):
            print(f"  {i}. {title_of(c)}  [{len(messages_of(c))} messages]  {c.get('created_at', '')}")
        return
    if not 1 <= args.pick <= len(found):
        sys.exit(f"--pick must be between 1 and {len(found)}")

    md = to_markdown(found[args.pick - 1])
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(md, encoding="utf-8")
        print(f"Wrote {args.output} ({len(messages_of(found[args.pick - 1]))} messages)")
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
