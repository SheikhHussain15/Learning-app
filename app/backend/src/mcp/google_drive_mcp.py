import json
import logging

from agents.tool import ToolContext

from agents import FunctionTool
from src.mcp.base_mcp import BaseMCPServer

logger = logging.getLogger(__name__)


class GoogleDriveMCP(BaseMCPServer):
    server_name = "google_drive"

    def get_tools(self) -> list[FunctionTool]:
        return [
            FunctionTool(
                name="read_drive_file",
                description="Read a file from Google Drive by file ID",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "Google Drive file ID"},
                    },
                    "required": ["file_id"],
                },
                on_invoke_tool=self._read_drive_file,
            ),
            FunctionTool(
                name="list_drive_files",
                description="List files in Google Drive",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Optional search query"},
                        "page_size": {"type": "integer", "description": "Number of files to return"},
                    },
                    "required": [],
                },
                on_invoke_tool=self._list_drive_files,
            ),
        ]

    async def _read_drive_file(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        file_id = args["file_id"]
        logger.info("Google Drive MCP: read file %s", file_id)
        return f"Simulated content of Google Drive file {file_id}"

    async def _list_drive_files(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        query = args.get("query", "")
        page_size = args.get("page_size", 10)
        logger.info("Google Drive MCP: list files (query=%s, page_size=%d)", query, page_size)
        return "[]"
