from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_success, print_preview, confirm, print_error, print_info


def handle_share(args):
    client = get_client(args.alias)
    text = args.text or ""
    lang = [args.lang] if args.lang else ["es"]

    if text:
        preview_data = {"text": text, "lang": args.lang, "to": args.to}
    else:
        preview_data = {"lang": args.lang, "to": args.to}
    if args.media:
        preview_data["media"] = args.media
    if args.alt:
        preview_data["alt"] = args.alt

    if args.dry_run:
        print_preview("share", preview_data)
        return

    if not args.y:
        print_preview("share", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        ref = _get_record_ref(client, args.to)

        if not text:
            result = client.com.atproto.repo.create_record({
                "repo": client.me.did,
                "collection": "app.bsky.feed.repost",
                "record": {
                    "$type": "app.bsky.feed.repost",
                    "subject": ref,
                    "createdAt": _now_iso(),
                },
            })
            url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
            print_success("Reposteado", url=url, at_uri=result.uri)
        else:
            facets = parse_facets(client, text)
            embed = _build_quote_embed(client, args, ref, text)

            result = client.send_post(text, langs=lang, facets=facets, embed=embed)
            url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
            print_success("Quote publicado", url=url, at_uri=result.uri, text=text)
    except Exception as e:
        print_error(str(e))


def _get_record_ref(client, at_uri: str) -> dict:
    parts = at_uri.replace("at://", "").split("/")
    repo = parts[0]
    collection = parts[1]
    rkey = parts[2]
    record = client.com.atproto.repo.get_record({"repo": repo, "collection": collection, "rkey": rkey})
    return {"uri": record.uri, "cid": record.cid}


def _build_quote_embed(client, args, ref: dict, text: str) -> dict:
    record_embed = {"$type": "app.bsky.embed.record", "record": ref}

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
            media_embed = build_images_embed(images)
        elif video:
            media_embed = build_video_embed(video, alt_text)
        else:
            return record_embed

        return {
            "$type": "app.bsky.embed.recordWithMedia",
            "record": record_embed,
            "media": media_embed,
        }

    return record_embed


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
