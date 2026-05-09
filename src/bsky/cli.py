import typer

from bsky.commands.login import handle_login, handle_logout
from bsky.commands.post import handle_post
from bsky.commands.thread import handle_thread
from bsky.commands.reply import handle_reply
from bsky.commands.share import handle_share
from bsky.commands.delete import handle_delete

app = typer.Typer(help="Bluesky CLI - Publica en Bluesky desde la terminal", no_args_is_help=True)


@app.command()
def login(
    handle: str = typer.Option(..., "-u", help="Handle de Bluesky"),
    password: str = typer.Option(..., "-p", help="App password"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
):
    handle_login(handle, password, alias)


@app.command()
def logout(
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
):
    handle_logout(alias)


@app.command()
def post(
    text: str | None = typer.Option(None, "-t", "--text", help="Texto del post"),
    media: list[str] = typer.Option(None, "-m", "--media", help="Ruta a media"),
    alt: list[str] = typer.Option(None, "--alt", help="Alt text para media"),
    lang: str = typer.Option("es", "--lang", help="Idioma"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
    y: bool = typer.Option(False, "-y", help="Saltar confirmación"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Solo preview"),
):
    handle_post(text, media or [], alt or [], lang, alias, y, dry_run)


@app.command()
def thread(
    text: list[str] = typer.Option(None, "-t", "--text", help="Texto por post"),
    media: list[str] = typer.Option(None, "-m", "--media", help="Ruta a media"),
    alt: list[str] = typer.Option(None, "--alt", help="Alt text"),
    lang: str = typer.Option("es", "--lang", help="Idioma"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
    y: bool = typer.Option(False, "-y", help="Saltar confirmación"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Solo preview"),
):
    handle_thread(text or [], media or [], alt or [], lang, alias, y, dry_run)


@app.command()
def reply(
    text: str | None = typer.Option(None, "-t", "--text", help="Texto de respuesta"),
    media: list[str] = typer.Option(None, "-m", "--media", help="Ruta a media"),
    alt: list[str] = typer.Option(None, "--alt", help="Alt text"),
    to: str = typer.Option(..., "--to", help="AT URI del post"),
    lang: str = typer.Option("es", "--lang", help="Idioma"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
    y: bool = typer.Option(False, "-y", help="Saltar confirmación"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Solo preview"),
):
    handle_reply(text, media or [], alt or [], to, lang, alias, y, dry_run)


@app.command()
def share(
    text: str | None = typer.Option(None, "-t", "--text", help="Texto para quote"),
    media: list[str] = typer.Option(None, "-m", "--media", help="Ruta a media"),
    alt: list[str] = typer.Option(None, "--alt", help="Alt text"),
    to: str = typer.Option(..., "--to", help="AT URI del post"),
    lang: str = typer.Option("es", "--lang", help="Idioma"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
    y: bool = typer.Option(False, "-y", help="Saltar confirmación"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Solo preview"),
):
    handle_share(text, media or [], alt or [], to, lang, alias, y, dry_run)


@app.command()
def delete(
    to: str = typer.Option(..., "--to", help="AT URI del post"),
    alias: str = typer.Option(..., "--as", help="Alias de cuenta"),
    y: bool = typer.Option(False, "-y", help="Saltar confirmación"),
):
    handle_delete(to, alias, y)


def main():
    app()
