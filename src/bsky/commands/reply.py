from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_success, print_preview, confirm, print_error, print_info


def handle_reply(args):
    if not args.text and not args.media:
        print_error("Se requiere al menos -t (texto) o -m (media)")
        return

    client = get_client(args.alias)
    text = args.text or ""
    lang = [args.lang] if args.lang else ["es"]

    preview_data = {"text": text, "lang": args.lang, "to": args.to}
    if args.media:
        preview_data["media"] = args.media
    if args.alt:
        preview_data["alt"] = args.alt

    if args.dry_run:
        print_preview("reply", preview_data)
        return

    if not args.y:
        print_preview("reply", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        parent = _get_record_ref(client, args.to)
        root = _get_root(client, args.to, parent)

        facets = parse_facets(client, text)
        embed = _build_embed(client, args, text)

        reply_to = {"root": root, "parent": parent}
        result = client.send_post(text, langs=lang, facets=facets, embed=embed, reply_to=reply_to)
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


def _build_embed(client, args, text: str) -> dict | None:
    if args.media:
        images = []
        video = None
        alt_index = 0

        for filepath in args.media:
            result = upload_media(client, filepath)
            if result["type"] == "image":
                alt_text = ""
                if args.alt and alt_index < len(args.alt):
                    alt_text = args.alt[alt_index]
                    alt_index += 1
                images.append({"blob": result["blob"], "alt": alt_text})
            elif result["type"] == "video":
                video = result
                alt_text = ""
                if args.alt and alt_index < len(args.alt):
                    alt_text = args.alt[alt_index]
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
