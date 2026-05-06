from datetime import datetime


def print_success(action: str, url: str | None = None, at_uri: str | None = None, text: str | None = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n✓ {action} {timestamp}")
    if url:
        print(f"  {url}")
    if at_uri:
        print(f"  {at_uri}")
    if text:
        display = text[:80] + "..." if len(text) > 80 else text
        print(f'  "{display}"')
    print()


def print_thread_success(posts: list[dict]):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n✓ Hilo publicado {timestamp} ({len(posts)} posts)")
    for i, post in enumerate(posts, 1):
        text = post.get("text", "")
        display = text[:60] + "..." if len(text) > 60 else text
        print(f'  {i}. "{display}"')
        if post.get("url"):
            print(f"     {post['url']}")
    print()


def print_preview(command: str, data: dict):
    print()
    if command == "post":
        print("¿Publicar?\n")
        if data.get("text"):
            print(f'  "{data["text"]}"')
        if data.get("media"):
            for m in data["media"]:
                print(f"  [media: {m}]")
        if data.get("alt"):
            for a in data["alt"]:
                print(f"  [alt: {a}]")
        print(f'  Lang: {data.get("lang", "es")}')
    elif command == "thread":
        posts = data.get("posts", [])
        print(f"¿Publicar hilo ({len(posts)} posts)?\n")
        for i, post in enumerate(posts, 1):
            text = post.get("text", "")
            display = text[:60] + "..." if len(text) > 60 else text
            if text:
                print(f'  {i}. "{display}"')
            else:
                print(f'  {i}. [solo media]')
            if post.get("media"):
                for m in post["media"]:
                    print(f"     [media: {m}]")
        print(f'  Lang: {data.get("lang", "es")}')
    elif command == "reply":
        print(f"¿Responder a: {data.get('to', '?')}?\n")
        if data.get("text"):
            print(f'  "{data["text"]}"')
        if data.get("media"):
            for m in data["media"]:
                print(f"  [media: {m}]")
        print(f'  Lang: {data.get("lang", "es")}')
    elif command == "share":
        if data.get("text"):
            print(f"¿Quote de: {data.get('to', '?')}?\n")
            print(f'  "{data["text"]}"')
        else:
            print(f"¿Repost de: {data.get('to', '?')}?\n")
        if data.get("media"):
            for m in data["media"]:
                print(f"  [media: {m}]")
        print(f'  Lang: {data.get("lang", "es")}')
    elif command == "delete":
        print(f"¿Eliminar: {data.get('to', '?')}?\n")
    print()


def confirm() -> bool:
    response = input("¿Confirmar? [y/N] ")
    return response.strip().lower() == "y"


def print_error(msg: str):
    print(f"\n✗ Error: {msg}\n")


def print_info(msg: str):
    print(f"\nℹ {msg}\n")
