import sys
from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_thread_success, print_preview, confirm, print_error, print_info


def handle_thread(args):
    if not args.text:
        print_error("Se requiere al menos un -t para cada post del hilo")
        return

    client = get_client(args.alias)
    lang = [args.lang] if args.lang else ["es"]

    posts = _parse_thread_args(args)

    if not posts:
        print_error("No se encontraron posts para el hilo")
        return

    preview_data = {"posts": posts, "lang": args.lang}

    if args.dry_run:
        print_preview("thread", preview_data)
        return

    if not args.y:
        print_preview("thread", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        results = []
        root = None
        parent = None

        for post_data in posts:
            text = post_data.get("text", "")
            facets = parse_facets(client, text)
            embed = _build_embed(client, post_data)

            if root is None:
                result = client.send_post(text, langs=lang, facets=facets, embed=embed)
                root = {"uri": result.uri, "cid": result.cid}
                parent = root
            else:
                reply_to = {"root": root, "parent": parent}
                result = client.send_post(text, langs=lang, facets=facets, embed=embed, reply_to=reply_to)
                parent = {"uri": result.uri, "cid": result.cid}

            url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
            results.append({"text": text, "url": url, "uri": result.uri})

        print_thread_success(results)
    except Exception as e:
        print_error(str(e))


def _parse_thread_args(args) -> list[dict]:
    posts = []
    current_post = {"text": None, "media": [], "alt": []}
    alt_index = 0

    texts = args.text if isinstance(args.text, list) else [args.text]
    media_list = args.media if args.media else []
    alt_list = args.alt if args.alt else []

    media_per_post = []
    current_media = []

    for arg_media in media_list:
        current_media.append(arg_media)

    for i, text in enumerate(texts):
        post = {"text": text, "media": [], "alt": []}
        posts.append(post)

    media_index = 0
    alt_idx = 0
    for i, post in enumerate(posts):
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
