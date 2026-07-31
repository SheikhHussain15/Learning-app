import json
import logging

from agents.tool import ToolContext

from agents import FunctionTool
from src.mcp.base_mcp import BaseMCPServer

logger = logging.getLogger(__name__)


class NotionMCP(BaseMCPServer):
    server_name = "notion"

    def get_tools(self) -> list[FunctionTool]:
        return [
            FunctionTool(
                name="read_notion_page",
                description="Read a Notion page by page ID",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "Notion page ID"},
                    },
                    "required": ["page_id"],
                },
                on_invoke_tool=self._read_notion_page,
            ),
            FunctionTool(
                name="query_notion_database",
                description="Query a Notion database",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "database_id": {"type": "string", "description": "Notion database ID"},
                        "filter": {"type": "object", "description": "Optional filter criteria"},
                    },
                    "required": ["database_id"],
                },
                on_invoke_tool=self._query_notion_database,
            ),
        ]

    async def _read_notion_page(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        page_id = args["page_id"]
        logger.info("Notion MCP: read page %s", page_id)
        return f"Simulated content of Notion page {page_id}"

    async def _query_notion_database(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        database_id = args["database_id"]
        logger.info("Notion MCP: query database %s", database_id)
        return "[]"
