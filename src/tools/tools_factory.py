from .tool import Tool
from .tools import fetch_webpage_content


def _build_fetch_webpage_content_tool() -> Tool:
    return Tool(
        name="fetch_webpage_content",
        description="Fetches and extracts the main readable text content from a webpage URL",
        input_schema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL of the webpage to fetch (must include http or https)"
                }
            },
            "required": ["url"]
        },
        handler=fetch_webpage_content
    )

def build_tools() -> list[Tool]:
    return [
        _build_fetch_webpage_content_tool()
    ]