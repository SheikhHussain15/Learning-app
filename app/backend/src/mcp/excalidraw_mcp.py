import json
import logging

from agents.tool import ToolContext

from agents import FunctionTool
from src.mcp.base_mcp import BaseMCPServer

logger = logging.getLogger(__name__)


class ExcalidrawMCP(BaseMCPServer):
    server_name = "excalidraw"

    def get_tools(self) -> list[FunctionTool]:
        return [
            FunctionTool(
                name="create_excalidraw_diagram",
                description="Create an Excalidraw diagram from a description",
                params_json_schema={
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "Diagram description"},
                        "format": {"type": "string", "description": "Output format (png, svg, excalidraw)"},
                    },
                    "required": ["description"],
                },
                on_invoke_tool=self._create_excalidraw_diagram,
            ),
        ]

    async def _create_excalidraw_diagram(self, context: ToolContext, args_json: str) -> str:
        args = json.loads(args_json)
        description = args["description"]
        output_format = args.get("format", "excalidraw")
        logger.info("Excalidraw MCP: create diagram '%s' (%s)", description, output_format)
        return json.dumps({
            "type": "excalidraw",
            "description": description,
            "format": output_format,
            "elements": [],
            "file": f"diagram_{hash(description)}.{output_format}",
        })
