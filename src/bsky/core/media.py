import os
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4"}


def detect_media_type(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    elif ext in VIDEO_EXTENSIONS:
        return "video"
    else:
        raise ValueError(f"Formato no soportado: {ext}")


def validate_media(filepath: str, media_type: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

    size = os.path.getsize(filepath)

    if media_type == "image":
        max_size = 2 * 1024 * 1024
        if size > max_size:
            raise ValueError(f"Imagen muy grande: {size / 1024 / 1024:.1f}MB (máx 2MB)")
    elif media_type == "video":
        max_size = 100 * 1024 * 1024
        if size > max_size:
            raise ValueError(f"Video muy grande: {size / 1024 / 1024:.1f}MB (máx 100MB)")


def upload_media(client, filepath: str) -> dict:
    media_type = detect_media_type(filepath)
    validate_media(filepath, media_type)

    with open(filepath, "rb") as f:
        data = f.read()

    blob = client.upload_blob(data)
    return {"type": media_type, "blob": blob}


def build_images_embed(images: list[dict]) -> dict:
    return {
        "$type": "app.bsky.embed.images",
        "images": [
            {
                "alt": img.get("alt", ""),
                "image": img["blob"].blob,
            }
            for img in images
        ],
    }


def build_video_embed(video: dict, alt: str = "") -> dict:
    return {
        "$type": "app.bsky.embed.video",
        "video": video["blob"].blob,
        "alt": alt,
    }
