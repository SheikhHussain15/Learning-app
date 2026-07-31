import json
import logging

from agents.tool import ToolContext

from agents import FunctionTool
from src.mcp.base_mcp import BaseMCPServer

logger = logging.getLogger(__name__)


class TavilyMCP(BaseMCPServer):
    server_name = "tavily"

    def get_tools(self) -> list[FunctionTool]:
        return [
            FunctionTool(
                name="web_search",
                description="Search the web using Tavily",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "description": "Maximum results to return"},
                    },
                    "required": ["query"],
                },
                on_invoke_tool=self._web_search,
            ),
        ]

    async def _web_search(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        query = args["query"]
        max_results = args.get("max_results", 5)
        logger.info("Tavily MCP: search '%s' (max_results=%d)", query, max_results)
        return json.dumps([{"title": f"Simulated result for {query}", "url": "https://example.com", "content": "Simulated content"}])
