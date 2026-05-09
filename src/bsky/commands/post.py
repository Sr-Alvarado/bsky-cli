from bsky.core.client import get_client
from bsky.core.facets import parse_facets, has_urls, extract_first_url
from bsky.core.media import upload_media, build_images_embed, build_video_embed
from bsky.core.og import fetch_og_card
from bsky.core.output import print_success, print_preview, confirm, print_error, print_info


def handle_post(text: str | None, media: list[str], alt: list[str], lang: str, alias: str, y: bool, dry_run: bool):
    media = media or []
    alt = alt or []
    if not text and not media:
        print_error("Se requiere al menos -t (texto) o -m (media)")
        return

    client = get_client(alias)
    text = text or ""
    lang_list = [lang] if lang else ["es"]

    preview_data = {"text": text, "lang": lang}
    if media:
        preview_data["media"] = media
    if alt:
        preview_data["alt"] = alt

    if dry_run:
        print_preview("post", preview_data)
        return

    if not y:
        print_preview("post", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        facets = parse_facets(client, text)
        embed = None

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
                embed = build_images_embed(images)
            elif video:
                embed = build_video_embed(video, alt_text)
        elif has_urls(text):
            url = extract_first_url(text)
            if url:
                embed = fetch_og_card(client, url)

        result = client.send_post(text, langs=lang_list, facets=facets, embed=embed)
        url = f"https://bsky.app/profile/{client.me.handle}/post/{result.uri.split('/')[-1]}"
        print_success("Publicado", url=url, at_uri=result.uri, text=text)
    except Exception as e:
        print_error(str(e))
