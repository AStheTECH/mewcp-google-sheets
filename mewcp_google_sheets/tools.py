import logging
from datetime import datetime, timedelta
from typing import List
from pydantic import Field

from fastmcp import FastMCP

from .schemas import (
    BatchUpdateSpreadsheetRequest,
    CreateSpreadSheetResponse,
    ApiObjectResponse
)
from .service import get_service

logger = logging.getLogger("calendar-mcp-server")


class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)

@mcp.tool(
    name="spreadsheets_batch_update",
    description="Applies one or more updates to the spreadsheet."
)
def spreadsheets_batch_update(spreadsheetId: str = Field("", description="The spreadsheet to apply the updates to.")) -> None:
    pass


