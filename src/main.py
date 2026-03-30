from dotenv import load_dotenv
import yaml
from pathlib import Path
from typing import Dict
from client import AnthropicClient
from agent_loop import loop
from context.context_manager import ContextManager
from tools.tools_factory import build_tools
from tools.tool_registry import ToolRegistry


PROJECT_DIR = Path(__file__).resolve().parent.parent

"""Loads the config yaml"""
def load_config(config_path: Path) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

"""Body of the entry point"""
def main() -> None:
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
    tool_registry = ToolRegistry(tools=build_tools())
    loop(client=client, ctx=ctx, tool_registry=tool_registry)

if __name__ == "__main__":
    main()