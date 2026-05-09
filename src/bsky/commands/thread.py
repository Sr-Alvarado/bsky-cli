from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_thread_success, print_preview, confirm, print_error, print_info
from bsky.core.text import unescape


def handle_thread(text: list[str], media: list[str], alt: list[str], lang: str, alias: str, y: bool, dry_run: bool):
    text = text or []
    media = media or []
    alt = alt or []
    text = [unescape(t) for t in text]
    if not text:
        print_error("Se requiere al menos un -t para cada post del hilo")
        return

    client = get_client(alias)
    lang_list = [lang] if lang else ["es"]

    posts = _parse_thread_args(text, media, alt)

    if not posts:
        print_error("No se encontraron posts para el hilo")
        return

    preview_data = {"posts": posts, "lang": lang}

    if dry_run:
        print_preview("thread", preview_data)
        return

    if not y:
        print_preview("thread", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        results = []
        root = None
        parent = None

        for post_data in posts:
            post_text = post_data.get("text", "")
            facets = parse_facets(client, post_text)
            embed = _build_embed(client, post_data)

            if root is None:
                result = client.send_post(post_text, langs=lang_list, facets=facets, embed=embed)
                root = {"uri": result.uri, "cid": result.cid}
                parent = root
            else:
                reply_to = {"root": root, "parent": parent}
                result = client.send_post(post_text, langs=lang_list, facets=facets, embed=embed, reply_to=reply_to)
                parent = {"uri": result.uri, "cid": result.cid}

            url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
            results.append({"text": post_text, "url": url, "uri": result.uri})

        print_thread_success(results)
    except Exception as e:
        print_error(str(e))


def _parse_thread_args(texts: list[str], media_list: list[str], alt_list: list[str]) -> list[dict]:
    posts = []
    for t in texts:
        posts.append({"text": t, "media": [], "alt": []})

    media_index = 0
    alt_idx = 0
    for post in posts:
        if media_index < len(media_list):
            post["media"].append(media_list[media_index])
            media_index += 1
            if alt_idx < len(alt_list):
                post["alt"].append(alt_list[alt_idx])
                alt_idx += 1

    return posts


def _build_embed(client, post_data: dict) -> dict | None:
    media_list = post_data.get("media", [])
    alt_list = post_data.get("alt", [])
    text = post_data.get("text", "")

    if media_list:
        images = []
        video = None
        alt_index = 0

        for filepath in media_list:
            result = upload_media(client, filepath)
            if result["type"] == "image":
                alt_text = ""
                if alt_index < len(alt_list):
                    alt_text = alt_list[alt_index]
                    alt_index += 1
                images.append({"blob": result["blob"], "alt": alt_text})
            elif result["type"] == "video":
                video = result
                alt_text = ""
                if alt_index < len(alt_list):
                    alt_text = alt_list[alt_index]
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
