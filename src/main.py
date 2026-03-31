import asyncio
from dotenv import load_dotenv
import yaml
from pathlib import Path
from typing import Dict
from client import AnthropicClient
from agent_loop import loop
from context.context_manager import ContextManager
from src.tools.tool import Tool, MCPTool
from tools.tools_factory import build_static_tools, build_mcp_tools
from tools.tool_registry import ToolRegistry
from mcp_logic.mcp_client import MCPClient
from mcp import Tool as MCPFrameworkTool

PROJECT_DIR = Path(__file__).resolve().parent.parent

"""Loads the config yaml"""
def load_config(config_path: Path) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

"""Body of the entry point"""
async def main() -> None:
    load_dotenv()
    config_path = PROJECT_DIR / "config.yaml"
    config = load_config(config_path)

    client = AnthropicClient(
        model_name=config["model_name"],
        max_tokens=config.get("max_tokens", 1024),
        max_retries=config.get("max_retries", 3),
        base_delay=config.get("base_delay", 1.0),
        max_delay=config.get("max_delay", 60.0)
    )
    
    ctx = ContextManager()

    mcp_client = MCPClient()
    await mcp_client.connect_to_server("/home/mihai/Projects/Playground/MCP-Server/main.py")
    mcp_server_tools: list[MCPFrameworkTool] = await mcp_client.list_tools()

    static_tools: list[Tool] = build_static_tools()
    mcp_tools: list[MCPTool] = build_mcp_tools(mcp_tools=mcp_server_tools)
    tool_registry = ToolRegistry(static_tools=static_tools, mcp_tools=mcp_tools)

    await loop(
        client=client,
        ctx=ctx,
        tool_registry=tool_registry,
        mcp_client=mcp_client
    )

if __name__ == "__main__":
    asyncio.run(main())