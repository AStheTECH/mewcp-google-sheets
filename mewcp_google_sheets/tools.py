import logging
from datetime import datetime, timedelta
from typing import List
from pydantic import Field

from fastmcp import FastMCP

from schemas import (
    Spreadsheet,
    DeveloperMetadata
)

from models import (
    BatchUpdateSpreadsheetRequest,
    CreateSpreadSheetResponse,
    ToolError,
    GetSpreadsheetQueryParams,
    GetByDataFilterRequestBody,
    SearchDeveloperMetadataRequestBody,
    SearchDeveloperMetadataResponse
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
def spreadsheets_batch_update(spreadsheetId: str = Field(..., description="The spreadsheet to apply the updates to."), body: BatchUpdateSpreadsheetRequest = Field(..., description="The request body for batch updating a spreadsheet.")) -> CreateSpreadSheetResponse | ToolError:
    try:
        response = get_service().spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body = body).execute()
        return response
    except Exception as exc:
        logger.error(f"error while batch updating: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="create_spreadsheet",
    description="Creates a spreadsheet, returning the newly created spreadsheet."
)
def create_spreadsheet(body: Spreadsheet = Field(..., description="The request body contains an instance of Spreadsheet")) -> Spreadsheet | ToolError:
    try:
        response = get_service().spreadsheets().create(body=body).execute()
        return response
    except Exception as exc:
        logger.error(f"error while creating a spreadsheet: {exc}", exc_info=True)
        return {"error": str(exc)}


@mcp.tool(
    name="get_spreadsheet",
    description="Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID."
)
def get_spreadsheet(spreadsheetId: str = Field(..., description="The spreadsheet to request."), queryParams: GetSpreadsheetQueryParams = Field(..., description="Query Parameters")) -> Spreadsheet | ToolError:
    try:
        response = get_service().spreadsheets().get(spreadsheetId=spreadsheetId, params=queryParams).execute()
        return response
    except Exception as exc:
        logger.error(f"error while getting a spreadsheet: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="getByDataFilter_spreadsheet",
    description="Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID.This method differs from spreadsheets.get in that it allows selecting which subsets of spreadsheet data to return by specifying a dataFilters parameter. Multiple DataFilters can be specified. Specifying one or more data filters returns the portions of the spreadsheet that intersect ranges matched by any of the filters."
)
def getByDataFilter_spreadsheet(spreadsheetId: str = Field(..., description="The spreadsheet to request."), body = GetByDataFilterRequestBody) -> Spreadsheet | ToolError:
    try:
        response = get_service().spreadsheets().getByDataFilter(spreadsheetId = spreadsheetId, body = body).execute()
        return response
    except Exception as exc:
        logger.error(f"error while getting the spreadsheet by data filter: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="get_developerMetadata",
    description="Returns the developer metadata with the specified ID. The caller must specify the spreadsheet ID and the developer metadata's unique metadataId"
)
def get_developerMetadata(spreadsheetId: str = Field(..., description="The spreadsheet to request."), metadataId : str = Field(..., description="The ID of the developer metadata to retrieve.")) -> DeveloperMetadata | ToolError:
    try:
        response = get_service().spreadsheets().getByDataFilter(spreadsheetId = spreadsheetId, metadataId= metadataId).execute()
        return response
    except Exception as exc:
        logger.error(f"error while getting the developer metadata: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="search_developerMetadata",
    description="Returns all developer metadata matching the specified DataFilter"
)
def search_developerMetadata(spreadsheetId: str = Field(..., description="The ID of the spreadsheet to retrieve metadata from."), params: SearchDeveloperMetadataRequestBody = Field(..., description="Search Developer Metadata Request Body")) -> SearchDeveloperMetadataResponse | ToolError:
    try:
        response = get_service().spreadsheets().developerMetadata().search(spreadsheetId = spreadsheetId, body = params).execute()
        return response
    except Exception as exc:
        logger.error(f"error while searching the developer metadata: {exc}", exc_info=True)
        return {"error": str(exc)}
