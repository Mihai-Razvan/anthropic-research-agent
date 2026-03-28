import requests
from bs4 import BeautifulSoup


def fetch_webpage_content(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "img", "header", "footer", "nav"]):
        tag.decompose()

    parts: list[str] = []

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    if title:
        parts.append(f"Title: {title}")

    description = soup.find("meta", attrs={"name": "description"})
    if description and description.get("content"):
        parts.append(f"Description: {description['content'].strip()}")

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    content = "\n".join(line for line in lines if line)

    if content:
        parts.append("Content:")
        parts.append(content)

    return "\n\n".join(parts)