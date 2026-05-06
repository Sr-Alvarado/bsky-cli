from atproto import Client
from bsky.config import get_credential, set_credential, get_default_alias


def get_client(alias: str | None = None) -> Client:
    if alias is None:
        alias = get_default_alias()
    if alias is None:
        raise SystemExit("No hay cuenta configurada. Ejecuta: bsky login -u HANDLE -p PASSWORD --as ALIAS")

    alias = alias.upper()
    session_str = get_credential(alias, "SESSION")
    handle = get_credential(alias, "HANDLE")
    password = get_credential(alias, "PASSWORD")

    if not handle or not password:
        raise SystemExit(f"Cuenta '{alias.lower()}' no encontrada. Ejecuta: bsky login -u HANDLE -p PASSWORD --as {alias.lower()}")

    client = Client()

    if session_str:
        try:
            client.login(session_string=session_str)
            _save_session(alias, client)
            return client
        except Exception:
            pass

    client.login(handle, password)
    _save_session(alias, client)
    return client


def _save_session(alias: str, client: Client):
    session_str = client.export_session_string()
    set_credential(alias, "SESSION", session_str)


def login_client(handle: str, password: str, alias: str) -> Client:
    client = Client()
    client.login(handle, password)
    alias = alias.upper()
    set_credential(alias, "HANDLE", handle)
    set_credential(alias, "PASSWORD", password)
    set_credential(alias, "DID", client.me.did)
    _save_session(alias, client)
    return client


def logout_client(alias: str):
    from bsky.config import delete_credential, load_env, save_env
    alias = alias.upper()
    delete_credential(alias)
    env = load_env()
    if env.get("BSKY_DEFAULT") == alias.lower():
        aliases = [k.replace("BSKY_", "").replace("_HANDLE", "").lower() for k in env.keys() if k.startswith("BSKY_") and k.endswith("_HANDLE") and k != f"BSKY_{alias}_HANDLE"]
        if aliases:
            env["BSKY_DEFAULT"] = aliases[0]
        else:
            env.pop("BSKY_DEFAULT", None)
        save_env(env)
