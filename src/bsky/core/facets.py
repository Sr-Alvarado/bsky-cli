import re


def parse_facets(client, text: str) -> list[dict]:
    text_bytes = text.encode("UTF-8")
    facets = []

    for m in parse_mentions(text_bytes):
        did = resolve_handle(client, m["handle"])
        if did:
            facets.append({
                "index": {"byteStart": m["start"], "byteEnd": m["end"]},
                "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}],
            })

    for t in parse_tags(text_bytes):
        facets.append({
            "index": {"byteStart": t["start"], "byteEnd": t["end"]},
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": t["tag"]}],
        })

    for u in parse_urls(text_bytes):
        facets.append({
            "index": {"byteStart": u["start"], "byteEnd": u["end"]},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": u["url"]}],
        })

    return facets


def parse_mentions(text_bytes: bytes) -> list[dict]:
    spans = []
    pattern = rb"(?:^|\s)(@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
    for m in re.finditer(pattern, text_bytes):
        handle = m.group(1).decode("UTF-8").lstrip("@")
        spans.append({"start": m.start(1), "end": m.end(1), "handle": handle})
    return spans


def parse_tags(text_bytes: bytes) -> list[dict]:
    spans = []
    pattern = rb"(?:^|\s)(#[^\d\s]\S*)"
    for m in re.finditer(pattern, text_bytes):
        tag = m.group(1).decode("UTF-8").strip()
        tag = re.sub(r"[^\w]+$", "", tag)
        if len(tag) > 66:
            continue
        spans.append({
            "start": m.start(1),
            "end": m.start(1) + len(tag.encode("UTF-8")),
            "tag": tag.lstrip("#"),
        })
    return spans


def parse_urls(text_bytes: bytes) -> list[dict]:
    spans = []
    pattern = rb"(?:^|\s)(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*[-a-zA-Z0-9@%_\+~#//=])?)"
    for m in re.finditer(pattern, text_bytes):
        url = m.group(1).decode("UTF-8")
        spans.append({"start": m.start(1), "end": m.end(1), "url": url})
    return spans


def resolve_handle(client, handle: str) -> str | None:
    try:
        response = client.com.atproto.identity.resolve_handle({"handle": handle})
        return response.did
    except Exception:
        return None


def has_urls(text: str) -> bool:
    return bool(re.search(r"https?://", text))


def extract_first_url(text: str) -> str | None:
    match = re.search(r"(https?://[^\s]+)", text)
    return match.group(1) if match else None
