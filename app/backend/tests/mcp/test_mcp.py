import json
import pytest
from types import SimpleNamespace
from src.mcp.google_drive_mcp import GoogleDriveMCP
from src.mcp.notion_mcp import NotionMCP
from src.mcp.tavily_mcp import TavilyMCP
from src.mcp.excalidraw_mcp import ExcalidrawMCP


@pytest.fixture
def mock_context():
    return SimpleNamespace()


class TestGoogleDriveMCP:
    @pytest.fixture
    def mcp(self):
        return GoogleDriveMCP()

    def test_server_name(self, mcp):
        assert mcp.server_name == "google_drive"

    def test_get_tools(self, mcp):
        tools = mcp.get_tools()
        assert len(tools) == 2
        assert tools[0].name == "read_drive_file"
        assert tools[1].name == "list_drive_files"

    @pytest.mark.asyncio
    async def test_read_drive_file(self, mcp, mock_context):
        result = await mcp._read_drive_file(mock_context, json.dumps({"file_id": "file-123"}))
        assert "file-123" in result

    @pytest.mark.asyncio
    async def test_list_drive_files(self, mcp, mock_context):
        result = await mcp._list_drive_files(mock_context, json.dumps({}))
        assert result is not None


class TestNotionMCP:
    @pytest.fixture
    def mcp(self):
        return NotionMCP()

    def test_server_name(self, mcp):
        assert mcp.server_name == "notion"

    def test_get_tools(self, mcp):
        tools = mcp.get_tools()
        assert len(tools) == 2
        tool_names = [t.name for t in tools]
        assert "read_notion_page" in tool_names
        assert "query_notion_database" in tool_names

    @pytest.mark.asyncio
    async def test_read_notion_page(self, mcp, mock_context):
        result = await mcp._read_notion_page(mock_context, json.dumps({"page_id": "page-456"}))
        assert "page-456" in result

    @pytest.mark.asyncio
    async def test_query_notion_database(self, mcp, mock_context):
        result = await mcp._query_notion_database(mock_context, json.dumps({"database_id": "db-789"}))
        assert result is not None


class TestTavilyMCP:
    @pytest.fixture
    def mcp(self):
        return TavilyMCP()

    def test_server_name(self, mcp):
        assert mcp.server_name == "tavily"

    def test_get_tools(self, mcp):
        tools = mcp.get_tools()
        assert len(tools) == 1
        assert tools[0].name == "web_search"

    @pytest.mark.asyncio
    async def test_web_search(self, mcp, mock_context):
        result = await mcp._web_search(mock_context, json.dumps({"query": "test query"}))
        assert "test query" in result


class TestExcalidrawMCP:
    @pytest.fixture
    def mcp(self):
        return ExcalidrawMCP()

    def test_server_name(self, mcp):
        assert mcp.server_name == "excalidraw"

    def test_get_tools(self, mcp):
        tools = mcp.get_tools()
        assert len(tools) == 1
        assert tools[0].name == "create_excalidraw_diagram"

    @pytest.mark.asyncio
    async def test_create_diagram(self, mcp, mock_context):
        result = await mcp._create_excalidraw_diagram(mock_context, json.dumps({"description": "Flowchart of API", "format": "svg"}))
        assert "Flowchart of API" in result
        assert "svg" in result
