import requests
from bs4 import BeautifulSoup


def fetch_og_card(client, url: str) -> dict | None:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("meta", property="og:title")
    desc_tag = soup.find("meta", property="og:description")
    img_tag = soup.find("meta", property="og:image")

    title = title_tag["content"] if title_tag and title_tag.get("content") else url
    description = desc_tag["content"] if desc_tag and desc_tag.get("content") else ""

    card = {"uri": url, "title": title, "description": description}

    if img_tag and img_tag.get("content"):
        img_url = img_tag["content"]
        if "://" not in img_url:
            img_url = url + img_url
        try:
            img_resp = requests.get(img_url, timeout=10)
            img_resp.raise_for_status()
            content_type = img_resp.headers.get("content-type", "image/jpeg")
            if not content_type.startswith("image/"):
                content_type = "image/jpeg"
            blob = client.upload_blob(img_resp.content)
            card["thumb"] = blob.blob
        except Exception:
            pass

    return {"$type": "app.bsky.embed.external", "external": card}
