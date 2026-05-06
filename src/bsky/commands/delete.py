from bsky.core.client import get_client
from bsky.core.output import print_success, print_preview, confirm, print_error, print_info


def handle_delete(args):
    client = get_client(args.alias)

    preview_data = {"to": args.to}

    if not args.y:
        print_preview("delete", preview_data)
        if not confirm():
            print_info("Cancelado")
            return

    try:
        parts = args.to.replace("at://", "").split("/")
        repo = parts[0]
        collection = parts[1]
        rkey = parts[2]

        client.com.atproto.repo.delete_record({
            "repo": repo,
            "collection": collection,
            "rkey": rkey,
        })
        print_success("Eliminado", at_uri=args.to)
    except Exception as e:
        print_error(str(e))
