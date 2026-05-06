import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bsky",
        description="Bluesky CLI - Publica en Bluesky desde la terminal",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # login
    login_parser = subparsers.add_parser("login", help="Guardar credenciales")
    login_parser.add_argument("-u", required=True, help="Handle de Bluesky")
    login_parser.add_argument("-p", required=True, help="App password")
    login_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")

    # logout
    logout_parser = subparsers.add_parser("logout", help="Borrar credenciales")
    logout_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")

    # post
    post_parser = subparsers.add_parser("post", help="Publicar post")
    post_parser.add_argument("-t", "--text", help="Texto del post")
    post_parser.add_argument("-m", "--media", action="append", help="Ruta a media (imagen/video)")
    post_parser.add_argument("--alt", action="append", help="Alt text para media")
    post_parser.add_argument("--lang", default="es", help="Idioma (default: es)")
    post_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")
    post_parser.add_argument("-y", action="store_true", help="Saltar confirmación")
    post_parser.add_argument("--dry-run", action="store_true", help="Solo preview, no publicar")

    # thread
    thread_parser = subparsers.add_parser("thread", help="Crear hilo")
    thread_parser.add_argument("-t", "--text", action="append", help="Texto del post (repetir para cada post)")
    thread_parser.add_argument("-m", "--media", action="append", help="Ruta a media")
    thread_parser.add_argument("--alt", action="append", help="Alt text para media")
    thread_parser.add_argument("--lang", default="es", help="Idioma (default: es)")
    thread_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")
    thread_parser.add_argument("-y", action="store_true", help="Saltar confirmación")
    thread_parser.add_argument("--dry-run", action="store_true", help="Solo preview, no publicar")

    # reply
    reply_parser = subparsers.add_parser("reply", help="Responder a post")
    reply_parser.add_argument("-t", "--text", help="Texto de la respuesta")
    reply_parser.add_argument("-m", "--media", action="append", help="Ruta a media")
    reply_parser.add_argument("--alt", action="append", help="Alt text para media")
    reply_parser.add_argument("--to", required=True, help="AT URI del post")
    reply_parser.add_argument("--lang", default="es", help="Idioma (default: es)")
    reply_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")
    reply_parser.add_argument("-y", action="store_true", help="Saltar confirmación")
    reply_parser.add_argument("--dry-run", action="store_true", help="Solo preview, no publicar")

    # share
    share_parser = subparsers.add_parser("share", help="Repost o quote post")
    share_parser.add_argument("-t", "--text", help="Texto para quote")
    share_parser.add_argument("-m", "--media", action="append", help="Ruta a media")
    share_parser.add_argument("--alt", action="append", help="Alt text para media")
    share_parser.add_argument("--to", required=True, help="AT URI del post")
    share_parser.add_argument("--lang", default="es", help="Idioma (default: es)")
    share_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")
    share_parser.add_argument("-y", action="store_true", help="Saltar confirmación")
    share_parser.add_argument("--dry-run", action="store_true", help="Solo preview, no publicar")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Eliminar post")
    delete_parser.add_argument("--to", required=True, help="AT URI del post")
    delete_parser.add_argument("--as", dest="alias", required=True, help="Alias de cuenta")
    delete_parser.add_argument("-y", action="store_true", help="Saltar confirmación")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "login":
        from bsky.commands.login import handle_login
        handle_login(args)
    elif args.command == "logout":
        from bsky.commands.login import handle_logout
        handle_logout(args)
    elif args.command == "post":
        from bsky.commands.post import handle_post
        handle_post(args)
    elif args.command == "thread":
        from bsky.commands.thread import handle_thread
        handle_thread(args)
    elif args.command == "reply":
        from bsky.commands.reply import handle_reply
        handle_reply(args)
    elif args.command == "share":
        from bsky.commands.share import handle_share
        handle_share(args)
    elif args.command == "delete":
        from bsky.commands.delete import handle_delete
        handle_delete(args)
