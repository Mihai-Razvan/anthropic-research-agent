import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Any, Callable, TypedDict
from anthropic.types.tool_param import ToolParam


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Any]

    def to_anthropic_tool_param(self) -> ToolParam:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }

    def run(self, **kwargs):
        self.handler() #I will better implement this .. now it's just for test

def _fetch_webpage_content(url: str) -> str:
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


fetch_webpage_content_tool: Tool = Tool(
    name="fetch_webpage_content",
    description= "Fetches and extracts the main readable text content from a webpage URL",
    input_schema= {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full URL of the webpage to fetch (must include http or https)"
            }
        },
        "required": ["url"]
    },
    handler= _fetch_webpage_content,
)

available_tools: list[Tool] = [
    fetch_webpage_content_tool
]
