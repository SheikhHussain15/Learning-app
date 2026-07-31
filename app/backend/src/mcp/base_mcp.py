from abc import ABC, abstractmethod

from agents import FunctionTool


class BaseMCPServer(ABC):
    server_name: str

    @abstractmethod
    def get_tools(self) -> list[FunctionTool]:
        ...
