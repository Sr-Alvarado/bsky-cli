from bsky.core.client import login_client, logout_client
from bsky.core.output import print_success, print_error
from bsky.config import set_default_alias, get_default_alias, list_aliases


def handle_login(handle: str, password: str, alias: str):
    try:
        client = login_client(handle, password, alias)
        if get_default_alias() is None:
            set_default_alias(alias)
        print_success(f"Login exitoso como {alias}", at_uri=f"DID: {client.me.did}")
    except Exception as e:
        print_error(f"Credenciales inválidas: {e}")


def handle_logout(alias: str):
    aliases = list_aliases()
    if alias.lower() not in aliases:
        print_error(f"Cuenta '{alias}' no encontrada")
        return
    logout_client(alias)
    print_success(f"Logout exitoso ({alias})")
