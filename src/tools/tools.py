import requests
from pathlib import Path
from bs4 import BeautifulSoup


def fetch_url(**kwargs) -> str:
    url: str = kwargs["url"]

    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        return str(e)

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


def read_file(**kwargs) -> str:
    path = Path(kwargs["path"])

    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return str(e)


def list_files(**kwargs) -> str:
    path = Path(kwargs.get("path", "."))

    try:
        entries = sorted(item.name for item in path.iterdir())
    except Exception as e:
        return str(e)

    return "\n".join(entries)


def create_file(**kwargs) -> str:
    path = Path(kwargs["path"])
    content = kwargs.get("content", "")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        return str(e)

    return f"Created file: {path}"


def edit_file(**kwargs) -> str:
    path = Path(kwargs["path"])
    content = kwargs["content"]

    if not path.exists():
        return f"File does not exist: {path}"

    if not path.is_file():
        return f"Path is not a file: {path}"

    try:
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        return str(e)

    return f"Updated file: {path}"