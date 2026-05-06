from bsky.core.client import login_client, logout_client
from bsky.core.output import print_success, print_error
from bsky.config import set_default_alias, get_default_alias, list_aliases


def handle_login(args):
    try:
        client = login_client(args.u, args.p, args.alias)
        if get_default_alias() is None:
            set_default_alias(args.alias)
        print_success(f"Login exitoso como {args.alias}", at_uri=f"DID: {client.me.did}")
    except Exception as e:
        print_error(f"Credenciales inválidas: {e}")


def handle_logout(args):
    aliases = list_aliases()
    if args.alias.lower() not in aliases:
        print_error(f"Cuenta '{args.alias}' no encontrada")
        return
    logout_client(args.alias)
    print_success(f"Logout exitoso ({args.alias})")
