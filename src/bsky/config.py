import os
from pathlib import Path
from dotenv import dotenv_values

CONFIG_DIR = Path.home() / ".config" / "bsky"
ENV_FILE = CONFIG_DIR / ".env"


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not ENV_FILE.exists():
        ENV_FILE.touch()
        ENV_FILE.chmod(0o600)


def load_env() -> dict:
    ensure_config_dir()
    return dotenv_values(ENV_FILE)


def save_env(data: dict):
    ensure_config_dir()
    lines = [f"{k}={v}" for k, v in data.items()]
    ENV_FILE.write_text("\n".join(lines) + "\n")
    ENV_FILE.chmod(0o600)


def get_credential(alias: str, key: str) -> str | None:
    env = load_env()
    return env.get(f"BSKY_{alias.upper()}_{key.upper()}")


def set_credential(alias: str, key: str, value: str):
    env = load_env()
    env[f"BSKY_{alias.upper()}_{key.upper()}"] = value
    save_env(env)


def delete_credential(alias: str):
    env = load_env()
    prefix = f"BSKY_{alias.upper()}_"
    env = {k: v for k, v in env.items() if not k.startswith(prefix)}
    save_env(env)


def get_default_alias() -> str | None:
    env = load_env()
    return env.get("BSKY_DEFAULT")


def set_default_alias(alias: str):
    env = load_env()
    env["BSKY_DEFAULT"] = alias
    save_env(env)


def list_aliases() -> list[str]:
    env = load_env()
    aliases = set()
    for key in env.keys():
        if key.startswith("BSKY_") and key.endswith("_HANDLE"):
            alias = key.replace("BSKY_", "").replace("_HANDLE", "").lower()
            aliases.add(alias)
    return sorted(aliases)
