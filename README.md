# bsky-cli

CLI para publicar en Bluesky desde la terminal.

## Instalación

```bash
git clone <repo-url> && cd bsky-cli
uv sync
```

## Uso

### Login

```bash
bsky login -u miusuario.bsky.social -p app-password-xxxx --as personal
```

### Post simple

```bash
bsky post -t "Hola mundo" --as personal
```

### Post con media

```bash
bsky post -t "Con foto" -m foto.jpg --as personal
bsky post -t "Con video" -m video.mp4 --as personal
```

### Post solo media

```bash
bsky post -m foto.jpg --as personal
```

### Hilo

```bash
bsky thread -t "Post 1" -t "Post 2" -t "Post 3" --as personal
```

### Hilo con media

```bash
bsky thread -t "Post 1" -m foto.jpg -t "Post 2" -t "Post 3" -m video.mp4 --as personal
```

### Reply

```bash
bsky reply -t "Mi respuesta" --to at://did:plc:xxx/app.bsky.feed.post/abc --as personal
```

### Repost

```bash
bsky share --to at://did:plc:xxx/app.bsky.feed.post/abc --as personal
```

### Quote

```bash
bsky share -t "Mi opinión" --to at://did:plc:xxx/app.bsky.feed.post/abc --as personal
```

### Eliminar post

```bash
bsky delete --to at://did:plc:xxx/app.bsky.feed.post/abc --as personal
```

### Logout

```bash
bsky logout --as personal
```

## Flags

| Flag | Descripción |
|------|-------------|
| `-t, --text` | Texto del post |
| `-m, --media` | Ruta a imagen/video |
| `--alt` | Alt text para media |
| `--lang` | Idioma (default: es) |
| `--as` | Alias de cuenta (obligatorio) |
| `-y` | Saltar confirmación |
| `--dry-run` | Solo preview, no publicar |

## Multicuenta

```bash
bsky login -u personal.bsky.social -p pass1 --as personal
bsky login -u bot.bsky.social -p pass2 --as bot

bsky post -t "Desde personal" --as personal
bsky post -t "Desde bot" --as bot
```

## Features

- Facets automáticos: menciones (@usuario), hashtags (#tag), links
- OG link cards: previews automáticos para URLs
- Media: imágenes (jpg, png, webp, gif) y video (mp4)
- Preview y confirmación antes de publicar
- Dry-run para verificar sin publicar
- Session persistente con refresh automático
- Multicuenta con aliases

## Credenciales

Las credenciales se guardan en `~/.config/bsky/.env` (chmod 600).

Contenido por cuenta:

```
BSKY_PERSONAL_HANDLE=miusuario.bsky.social
BSKY_PERSONAL_PASSWORD=app-password-xxxx
BSKY_PERSONAL_DID=did:plc:abc123
BSKY_PERSONAL_SESSION=handle:::did:::accessJwt:::refreshJwt:::pds
BSKY_DEFAULT=personal
```

## Límites

- Texto: 3000 chars máx
- Imágenes: 4 por post, ~2MB c/u
- Video: 1 por post, 100MB máx, formato mp4

## Ejemplos

```bash
# Post con mención y hashtag
bsky post -t "Hola @usuario.bsky.social #bsky-cli" --as personal

# Post con link (genera OG card automáticamente)
bsky post -t "Mira esto https://bsky.app" --as personal

# Quote con imagen
bsky share -t "Increíble" -m foto.jpg --to at://... --as personal

# Hilo con media
bsky thread -t "Parte 1" -m img1.jpg -t "Parte 2" -t "Parte 3" -m img2.jpg --as personal
```

## Desarrollo

```bash
uv sync
uv run bsky --help
```

## Licencia

MIT
