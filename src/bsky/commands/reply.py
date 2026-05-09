from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_success, print_preview, confirm, print_error, print_info
from bsky.core.text import unescape


def handle_reply(text: str | None, media: list[str], alt: list[str], to: str, lang: str, alias: str, y: bool, dry_run: bool):
    media = media or []
    alt = alt or []
    text = unescape(text)
    if not text and not media:
        print_error("Se requiere al menos -t (texto) o -m (media)")
        return

    client = get_client(alias)
    lang_list = [lang] if lang else ["es"]

    preview_data = {"text": text, "lang": lang, "to": to}
    if media:
        preview_data["media"] = media
    if alt:
        preview_data["alt"] = alt

    if dry_run:
        print_preview("reply", preview_data)
        return

    if not y:
        print_preview("reply", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        parent = _get_record_ref(client, to)
        root = _get_root(client, to, parent)

        facets = parse_facets(client, text)
        embed = _build_embed(client, media, alt, text)

        reply_to = {"root": root, "parent": parent}
        result = client.send_post(text, langs=lang_list, facets=facets, embed=embed, reply_to=reply_to)
        url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
        print_success("Reply publicado", url=url, at_uri=result.uri, text=text)
    except Exception as e:
        print_error(str(e))


def _get_record_ref(client, at_uri: str) -> dict:
    parts = at_uri.replace("at://", "").split("/")
    repo = parts[0]
    collection = parts[1]
    rkey = parts[2]
    record = client.com.atproto.repo.get_record({"repo": repo, "collection": collection, "rkey": rkey})
    return {"uri": record.uri, "cid": record.cid}


def _get_root(client, at_uri: str, parent: dict) -> dict:
    parts = at_uri.replace("at://", "").split("/")
    repo = parts[0]
    collection = parts[1]
    rkey = parts[2]
    record = client.com.atproto.repo.get_record({"repo": repo, "collection": collection, "rkey": rkey})
    if record.value.reply:
        return record.value.reply.root
    return parent


def _build_embed(client, media: list[str], alt: list[str], text: str) -> dict | None:
    if media:
        images = []
        video = None
        alt_index = 0

        for filepath in media:
            result = upload_media(client, filepath)
            if result["type"] == "image":
                alt_text = ""
                if alt_index < len(alt):
                    alt_text = alt[alt_index]
                    alt_index += 1
                images.append({"blob": result["blob"], "alt": alt_text})
            elif result["type"] == "video":
                video = result
                alt_text = ""
                if alt_index < len(alt):
                    alt_text = alt[alt_index]
                break

        if images:
            return build_images_embed(images)
        elif video:
            return build_video_embed(video, alt_text)
    elif has_urls(text):
        url = extract_first_url(text)
        if url:
            return fetch_og_card(client, url)

    return None
